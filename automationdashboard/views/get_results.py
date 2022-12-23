from automationdashboard.src.test_results_processor import TestResultsProcessor
from flask import jsonify, request

from automationdashboard import app


@app.route('/getResultByGroupName', methods=["GET"])
def get_result():
    """
    Endpoint to create a post record.
    Takes the payload of hte POST call, and saves is as a .json file.
    It does not do any validation.

    Example payload:
        {"testGroupName": "FE Regression"}
        or with more filters
        {"testGroupName": "FE Regression", "startDateTime": "2022-12-16 22:00:41", "endDateTime": "2022-12-22 22:00:41"}

    :return: List of reports.
        Example:[
                    {
                        "created_date": "Fri, 16 Dec 2022 22:00:41 GMT",
                        "end_time": "2022-12-16 22:44:41",
                        "id": 1,
                        "modified_date": "Fri, 16 Dec 2022 22:00:41 GMT",
                        "number_of_failed_tests": 43,
                        "number_of_passed_tests": 57,
                        "result_status": "FAIL",
                        "start_time": "2022-12-16 22:00:41",
                        "test_group_name": "FE Regression"
                    },
                    {
                        "created_date": "Fri, 16 Dec 2022 22:00:41 GMT",
                        "end_time": "2022-12-16 22:44:41",
                        "id": 2,
                        "modified_date": "Fri, 16 Dec 2022 22:00:41 GMT",
                        "number_of_failed_tests": 1,
                        "number_of_passed_tests": 99,
                        "result_status": "PASS",
                        "start_time": "2022-12-16 22:00:41",
                        "test_group_name": "FE Regression"
                    }
                ]
    """

    app.logger.info("Getting test results from db")

    request_data = request.json

    app.logger.debug(f"Request parameters: {request_data}")

    results_processor = TestResultsProcessor()
    test_group_name = request_data["testGroupName"]
    start_time = request_data.get("startDateTime")
    end_time = request_data.get("endDateTime")
    data = results_processor.get_test_result_by_group_name(test_group_name=test_group_name, start_time=start_time, end_time=end_time)

    return jsonify(data)

