from flask import jsonify, request

from automationdashboard import app
from automationdashboard.src.test_results import TestResults




@app.route('/postResult', methods=["POST"])
def post_result():
    """
    Endpoint to create a post record.
    Takes the payload of hte POST call, and saves is as a .json file.
    It does not do any validation.
    :return: same data as the request (json)
    """

    data = request.get_json()

    results_helper = TestResults()
    results_helper.store_report_in_file(data)
    results_helper.get_all_reports_in_directory()

    return jsonify(data)

