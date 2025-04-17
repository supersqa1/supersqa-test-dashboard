from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pathlib import Path
from pydantic import BaseModel
from datetime import datetime
from typing import List
import json

app = FastAPI(title="Automation Dashboard")

# Mount static files
static_path = Path(__file__).parent / "static"
static_path.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# In-memory storage for demo
test_results = []

class TestResult(BaseModel):
    startDateTime: str
    endDateTime: str
    numberOfTestCasesPassed: int
    numberOfTestCasesFailed: int
    testGroupName: str
    resultStatus: str

def calculate_pass_rate(passed: int, failed: int) -> float:
    """Calculate pass rate percentage"""
    total = passed + failed
    return round((passed / total) * 100, 1) if total > 0 else 0.0

@app.get("/")
async def dashboard(request: Request):
    """Main dashboard view"""
    # Process test results for display
    suite_stats = {}
    for result in test_results:
        name = result.testGroupName
        current_time = datetime.strptime(result.startDateTime, "%Y-%m-%d %H:%M:%S")
        
        if name not in suite_stats or current_time > suite_stats[name]['last_run']:
            suite_stats[name] = {
                'name': name,
                'status': result.resultStatus,
                'pass_rate': calculate_pass_rate(result.numberOfTestCasesPassed, result.numberOfTestCasesFailed),
                'last_run': current_time,
                'passed': result.numberOfTestCasesPassed,
                'failed': result.numberOfTestCasesFailed
            }

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "page_title": "Automation Dashboard",
            "suites": list(suite_stats.values())
        }
    )

@app.get("/api/stats", response_class=HTMLResponse)
async def get_stats(request: Request):
    """Get dashboard statistics"""
    if not test_results:
        stats = {
            "total_suites": 0,
            "passing_suites": 0,
            "failing_suites": 0,
            "total_tests": 0,
            "pass_rate": 0
        }
    else:
        # Get latest result for each suite
        latest_results = {}
        for result in test_results:
            name = result.testGroupName
            current_time = datetime.strptime(result.startDateTime, "%Y-%m-%d %H:%M:%S")
            if name not in latest_results or current_time > datetime.strptime(latest_results[name].startDateTime, "%Y-%m-%d %H:%M:%S"):
                latest_results[name] = result

        # Calculate statistics
        passing_suites = sum(1 for r in latest_results.values() if r.resultStatus == "PASS")
        total_passed = sum(r.numberOfTestCasesPassed for r in test_results)
        total_failed = sum(r.numberOfTestCasesFailed for r in test_results)
        
        stats = {
            "total_suites": len(latest_results),
            "passing_suites": passing_suites,
            "failing_suites": len(latest_results) - passing_suites,
            "total_tests": total_passed + total_failed,
            "pass_rate": calculate_pass_rate(total_passed, total_failed)
        }
    
    return templates.TemplateResponse(
        "stats.html",
        {
            "request": request,
            **stats
        }
    ).body

@app.get("/api/suite/{suite_id}")
async def get_suite_details(suite_id: str):
    """Get detailed information for a test suite"""
    suite_results = [r for r in test_results if r.testGroupName == suite_id]
    if not suite_results:
        return {"error": "Suite not found"}
    
    # Sort by date
    suite_results.sort(key=lambda x: datetime.strptime(x.startDateTime, "%Y-%m-%d %H:%M:%S"))
    latest = suite_results[-1]
    
    # Calculate pass rates for history - using individual run results
    history = []
    for result in suite_results[-10:]:  # Only keep last 10 runs
        history.append({
            "date": result.startDateTime,
            "pass_rate": calculate_pass_rate(result.numberOfTestCasesPassed, result.numberOfTestCasesFailed)
        })
    
    return {
        "id": suite_id,
        "name": latest.testGroupName,
        "status": latest.resultStatus,
        "last_run": latest.startDateTime,
        "pass_rate": calculate_pass_rate(latest.numberOfTestCasesPassed, latest.numberOfTestCasesFailed),
        "execution_time": "30 mins",
        "history": history,
        "passed": latest.numberOfTestCasesPassed,
        "failed": latest.numberOfTestCasesFailed
    }

@app.post("/postResult")
async def post_result(result: TestResult):
    """Post a new test result"""
    test_results.append(result)
    return {"status": "success"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000) 