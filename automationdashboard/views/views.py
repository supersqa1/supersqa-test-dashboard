from automationdashboard import app
from datetime import datetime
from flask import render_template, jsonify
from automationdashboard.src.test_results_processor import TestResultsProcessor
import json

def parse_json_safely(data):
    """Safely parse JSON data, handling both string and dict inputs"""
    if isinstance(data, str):
        try:
            return json.loads(data)
        except json.JSONDecodeError:
            return None
    return data

def safe_int(value, default=0):
    """Safely convert value to int"""
    try:
        return int(float(value))
    except (ValueError, TypeError):
        return default

def safe_float(value, default=0.0):
    """Safely convert value to float"""
    try:
        return float(value)
    except (ValueError, TypeError):
        return default

def get_status_and_color(pass_rate):
    """Get status and color based on pass rate thresholds"""
    if pass_rate == 100:
        return 'PASS', 'green'
    elif pass_rate >= 90:
        return 'WARN', 'yellow'
    else:
        return 'FAIL', 'red'

def parse_suite_data(suite_dict):
    """Parse test suite data into a consistent format"""
    try:
        # The data comes as a dict with a single key-value pair
        # where the key is the suite name and value is the suite data
        if not isinstance(suite_dict, dict):
            print(f"Invalid suite data type: {type(suite_dict)}")
            return None
        
        # Get the first (and only) key-value pair
        name, data = next(iter(suite_dict.items()))
        
        # Extract runs data and basic info
        runs = data.get('runs', [])
        if not runs:
            print(f"No runs found for suite {name}")
            return None
            
        # Get the latest run
        latest_run = runs[-1] if runs else {}
        
        # Get test counts from the latest run
        passed = safe_int(latest_run.get('number_of_passed_tests', 0))
        failed = safe_int(latest_run.get('number_of_failed_tests', 0))
        total_tests = passed + failed
        
        # Calculate pass rate from actual test counts
        pass_rate = (passed / total_tests * 100) if total_tests > 0 else 0.0
        status, color = get_status_and_color(pass_rate)
        
        # Format history from runs
        history = []
        for run in sorted(runs[-10:], key=lambda x: x.get('start_time', '')):
            run_passed = safe_int(run.get('number_of_passed_tests', 0))
            run_failed = safe_int(run.get('number_of_failed_tests', 0))
            run_total = run_passed + run_failed
            if run_total > 0:
                run_pass_rate = (run_passed / run_total) * 100
            else:
                run_pass_rate = 0.0
                
            run_status, run_color = get_status_and_color(run_pass_rate)
            history.append({
                'date': str(run.get('start_time', '')),
                'pass_rate': run_pass_rate,
                'color': run_color
            })

        return {
            'name': name,
            'status': status,
            'color': color,
            'pass_rate': pass_rate,
            'last_run': latest_run.get('start_time', ''),
            'passed': passed,
            'failed': failed,
            'total_tests': total_tests,
            'execution_time': '30 minutes',
            'history': history
        }
    except Exception as e:
        print(f"Error parsing suite data: {e}, for suite: {suite_dict}")
        return None

def process_test_results():
    """Process test results and return formatted data"""
    results_processor = TestResultsProcessor()
    raw_results = results_processor.get_all_results_formatted()
    
    print(f"Raw results structure: {type(raw_results)}")  # Debug print
    if raw_results:
        print(f"First group structure: {type(raw_results[0])}")
        if raw_results[0]:
            print(f"First suite structure: {type(raw_results[0][0])}")
    
    formatted_suites = []
    # Raw results is a list of lists of dicts
    for result_group in raw_results:
        for suite_dict in result_group:
            suite_data = parse_suite_data(suite_dict)
            if suite_data:
                formatted_suites.append(suite_data)
    
    print(f"Formatted suites: {formatted_suites}")  # Debug print
    
    # Calculate summary stats
    total_suites = len(formatted_suites)
    passing_suites = sum(1 for suite in formatted_suites if suite['status'] == 'PASS')
    failing_suites = total_suites - passing_suites
    
    total_tests = sum(suite['total_tests'] for suite in formatted_suites)
    total_passed = sum(suite['passed'] for suite in formatted_suites)
    
    stats = {
        'total_suites': total_suites,
        'passing_suites': passing_suites,
        'failing_suites': failing_suites,
        'total_tests': total_tests,
        'overall_pass_rate': (total_passed / total_tests * 100) if total_tests > 0 else 0.0
    }
    
    print(f"Stats: {stats}")  # Debug print
    
    return formatted_suites, stats

@app.route('/')
def home():
    """Home page with dashboard"""
    suites, stats = process_test_results()
    return render_template('dashboard.html', stats=stats, suites=suites)

@app.route('/api/stats')
def get_stats():
    """Get dashboard statistics for HTMX updates"""
    _, stats = process_test_results()
    return render_template('stats.html', stats=stats)

@app.route('/api/suite/<suite_id>')
def get_suite(suite_id):
    """Get test suite details for HTMX updates"""
    suites, _ = process_test_results()
    
    suite_data = next(
        (suite for suite in suites if suite['name'] == suite_id),
        None
    )
    
    if not suite_data:
        return jsonify({'error': 'Suite not found'})
    
    # Return HTML for HTMX update
    return render_template('suite_card.html', suite=suite_data)

@app.route('/api/suite/<suite_id>/status')
def get_suite_status(suite_id):
    """Get test suite status for HTMX updates"""
    suites, _ = process_test_results()
    suite_data = next((suite for suite in suites if suite['name'] == suite_id), None)
    
    if not suite_data:
        return 'UNKNOWN'
    
    status_classes = {
        'PASS': 'bg-green-100 text-green-800',
        'WARN': 'bg-yellow-100 text-yellow-800',
        'FAIL': 'bg-red-100 text-red-800'
    }
    status_class = status_classes.get(suite_data['status'], 'bg-gray-100 text-gray-800')
    return f'<span class="px-2 py-1 rounded text-sm {status_class}">{suite_data["status"]}</span>'

@app.route('/api/suite/<suite_id>/stats')
def get_suite_stats(suite_id):
    """Get test suite stats for HTMX updates"""
    suites, _ = process_test_results()
    suite_data = next((suite for suite in suites if suite['name'] == suite_id), None)
    
    if not suite_data:
        return '0.0%'
    
    return f'{suite_data["pass_rate"]:.1f}%'

@app.route('/api/suite/<suite_id>/progress')
def get_suite_progress(suite_id):
    """Get test suite progress bar for HTMX updates"""
    suites, _ = process_test_results()
    suite_data = next((suite for suite in suites if suite['name'] == suite_id), None)
    
    if not suite_data:
        return '<div class="h-2 rounded-full" style="width: 0%"></div>'
    
    color_classes = {
        'PASS': 'bg-green-500',
        'WARN': 'bg-yellow-500',
        'FAIL': 'bg-red-500'
    }
    color_class = color_classes.get(suite_data['status'], 'bg-gray-500')
    return f'<div class="h-2 rounded-full {color_class}" style="width: {suite_data["pass_rate"]}%"></div>'

@app.route('/api/suite/<suite_id>/details')
def get_suite_details(suite_id):
    """Get test suite details for HTMX updates"""
    suites, _ = process_test_results()
    suite_data = next((suite for suite in suites if suite['name'] == suite_id), None)
    
    if not suite_data:
        return 'No data available'
    
    return f'Last Run: {suite_data["last_run"]}<br>{suite_data["passed"]}/{suite_data["total_tests"]} Tests Passed'

@app.route('/api/suite/<suite_id>/history')
def get_suite_history(suite_id):
    """Get test suite history for chart updates"""
    suites, _ = process_test_results()
    suite_data = next((suite for suite in suites if suite['name'] == suite_id), None)
    
    if not suite_data:
        return jsonify({'history': [], 'status': 'UNKNOWN'})
    
    return jsonify({
        'history': suite_data['history'],
        'status': suite_data['status']
    })

@app.route('/api/suite/<suite_id>/failed')
def get_suite_failed(suite_id):
    """Get failed tests count for HTMX updates"""
    suites, _ = process_test_results()
    suite_data = next((suite for suite in suites if suite['name'] == suite_id), None)
    
    if not suite_data:
        return '0'
    
    return str(suite_data['failed'])

@app.route('/api/suite/<suite_id>/passed')
def get_suite_passed(suite_id):
    """Get passed tests count for HTMX updates"""
    suites, _ = process_test_results()
    suite_data = next((suite for suite in suites if suite['name'] == suite_id), None)
    
    if not suite_data:
        return '0'
    
    return str(suite_data['passed'])

