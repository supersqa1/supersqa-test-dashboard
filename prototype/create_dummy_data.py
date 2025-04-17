import requests
import json
import random
from datetime import datetime, timedelta

url = "http://127.0.0.1:8000/postResult"  # Note: Using port 8000 for our prototype

statuses = ['PASS', 'FAIL']
jobs = [
    'FE Regression',
    'BE Regression',
    'Order API Smoke',
    'Customer API Smoke',
    'My Account Page Smoke',
    'Login Page Smoke',
    'Login Page Regression'
]

# Create test results for each job
for job in jobs:
    for i in range(25):  # 25 results per job
        passed_ct = random.randint(0, 100)
        failed_ct = random.randint(0, 100 - passed_ct)  # Ensure total doesn't exceed 100

        # Create timestamps with some variation
        start_date = datetime.now() - timedelta(days=random.randint(0, 30))
        end_date = start_date + timedelta(minutes=random.randint(25, 35))

        payload = {
            "startDateTime": start_date.strftime("%Y-%m-%d %H:%M:%S"),
            "endDateTime": end_date.strftime("%Y-%m-%d %H:%M:%S"),
            "numberOfTestCasesPassed": passed_ct,
            "numberOfTestCasesFailed": failed_ct,
            "testGroupName": job,
            "resultStatus": "PASS" if passed_ct > failed_ct else "FAIL"
        }

        try:
            response = requests.post(url, json=payload)
            print(f"Posted result for {job}: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error posting result for {job}: {e}")

print("Finished creating dummy data!") 