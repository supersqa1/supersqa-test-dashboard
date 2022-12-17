from flask import jsonify, request

from automationdashboard import app
from automationdashboard.src.test_result import TestResult
from automationdashboard.src.test_results_processor import TestResultsProcessor




@app.route('/postResult', methods=["POST"])
def post_result():
    """
    Endpoint to create a post record.
    Takes the payload of hte POST call, and saves is as a .json file.
    It does not do any validation.
    :return: same data as the request (json)
    """

    data = request.get_json()

    try:

        tr = TestResult(
            start_time=data['startDateTime'],
            end_time=data['endDateTime'],
            number_of_passed_tests=data['numberOfTestCasesPassed'],
            number_of_failed_tests=data['numberOfTestCasesFailed'],
            test_group_name=data['testGroupName'],
            result_status=data['resultStatus']
        )


    except KeyError as e:
        return jsonify({"error": f"Missing the '{e.args[0]}' key from payload."}), 400
    except ValueError as e:
        return jsonify({"error": e.args}), 400

        import pdb; pdb.set_trace()
        print('aaa')

    results_processor = TestResultsProcessor()
    results_processor.store_report(tr)


    return jsonify(data)

