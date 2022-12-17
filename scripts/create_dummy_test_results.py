

import requests
import json
import random
from datetime import datetime, timedelta



""""
example_payload 
{
    "startDateTime":"2022-12-15 00:00:00",
    "endDateTime":"2022-12-15 03:00:05",
    "numberOfTestCasesPassed": 58,
    "numberOfTestCasesFailed": 7,
    "testGroupName": "regresss fe Smoke 102",
    "resultStatus": "FAIL"

}

"""


url = "http://staging.automationdashboard.supersqa.com/postResult"
url = "http://127.0.0.1:9098/postResult"

statuses = ['PASS', 'FAIL']
jobs = ['FE Regression', 'BE Regression', 'Order API Smoke', 'Customer API Smoke', 'My Account Page Smoke', 'Login Page Smoke', 'Login Page Regression']
for job in jobs:
    for i in range(25):
        passed_ct = random.randint(0, 100)
        failed_pct = 100 - passed_ct

        start_date = datetime.now()
        end_date = start_date + timedelta(minutes=random.randint(40, 45))

        payload = json.dumps({
            "startDateTime": start_date.strftime("%Y-%m-%d %H:%M:%S"),
            "endDateTime": end_date.strftime("%Y-%m-%d %H:%M:%S"),
            "numberOfTestCasesPassed": passed_ct,
            "numberOfTestCasesFailed": failed_pct,
            "testGroupName": job,
            "resultStatus": random.choice(statuses)
        })
        headers = {
            'Content-Type': 'application/json'
        }
        print(payload)
        print('**************')
        response = requests.request("POST", url, headers=headers, data=payload)

    print(f"Job: {job}")

# print(response.text)
