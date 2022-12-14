

import json
import logging
import os
from datetime import datetime


class TestResults:

    def __init__(self):

        self.results_dir = os.environ.get("RESULTS_DIR")
        if not self.results_dir:
            raise Exception("Env variable 'RESULTS_DIR' must be set.")


    def store_report_in_file(self, report_data):
        """
        Creates a .json file and aves the report data in the file.
        Uses the current datetime as file name

        :param report_data: must be a dictionary or json object
        :return: None
        """

        # Check if the folder exist
        is_exist = os.path.exists(self.results_dir) and os.path.isdir(self.results_dir)
        if not is_exist:
            os.makedirs(self.results_dir)

        # create a file with the current datetime as file name
        timestamp = datetime.now().strftime('%Y%m%d%H%M%s')
        result_file_path = os.path.join(self.results_dir, timestamp) + ".json"
        with open(result_file_path, 'w') as f:
            f.write(json.dumps(report_data))


    def get_all_reports_in_directory(self):
        """
        Gets all the available result files in the results folder.
        The folder is set as instance variable.
        Each file is read into a json, and collected in a list.

        :return: a list of dictionaries. Each dictionary is a result.
        """

        all_files = os.listdir(self.results_dir)

        all_files_content = []
        for report_file in all_files:
            if report_file.endswith('.json'):
                f_name = os.path.join(self.results_dir, report_file)
                with open(f_name, 'r') as f:
                    data = json.load(f)
                all_files_content.append(data)
        return all_files_content

    def get_latest_result_details(self, results_list):
        """
        Given a list of results, it parses the list and calculates some details.
            * Gets the status of the latest run
            * Gets the total number of passed tests in the list
            * Gets the total number of failed tests in the list
            * Calculates the pass/fail percentage

        :param results_list:
        :return:
        """
        latest = datetime.min  # initialize oldest datetime
        latest_info = {}
        for i in results_list:
            start_datetime_obj = datetime.strptime(i['startDateTime'], "%Y-%m-%d %H:%M:%S")
            if start_datetime_obj > latest:
                latest = datetime.strptime(i['startDateTime'], "%Y-%m-%d %H:%M:%S")
                latest_info['latest_status'] = i['resultStatus']
                latest_info['latest_pass'] = i['numberOfTestCasesPassed']
                latest_info['latest_fail'] = i['numberOfTestCasesFailed']
                latest_info['total'] = int(i['numberOfTestCasesPassed']) + int(i['numberOfTestCasesFailed'])
                latest_info['pct_pass'] = round(int(i['numberOfTestCasesPassed'])/latest_info['total'] * 100, )

        return latest_info


    def get_all_results_formatted(self):
        """
        Returns all files found in the results directory in a formatted way.
        The format is what the frontend template is expecting.

        Example formatted data to be returned:
                formatted_results = [
                                        [
                                            {
                                                "Backend Smoke": {
                                                    "name": "Backend Smoke",
                                                    "pass_fail": "PASS"
                                                    "pctPASS": "34",
                                                    "pctFAIL": "55",
                                                    "runs": [{"result": "PASS", "startTime": "30291"}, {"result": "PASS", "startTime": "30291"}, {"result": "PASS", "startTime": "30291"}]
                                                 }
                                            },
                                            {
                                                "Backend regrees": {
                                                    "name": "Backend Smoke",
                                                    "pctPASS": "666",
                                                    "pctFAIL": "0089",
                                                    "runs": [{"result": "PASS", "startTime": "4556", "endTime": "4556"},{"result": "PASS", "startTime": "30291"}, {"result": "PASS", "startTime": "68433"}]
                                                }
                                            },
                                        ],
                                        [
                                            {
                                                "fe Smoke": {
                                                    "name": "Backend Smoke",
                                                    "pctPASS": "34",
                                                    "pctFAIL": "55",
                                                    "runs": [
                                                        {"result": "PASS", "startTime": "30291"},
                                                        {"result": "PASS", "startTime": "30291"},
                                                        {"result": "PASS", "startTime": "30291"}
                                                    ]
                                                }
                                            },
                                            {
                                                "fe regre": {
                                                    "name": "Backend Smoke",
                                                    "pctPASS": "34",
                                                    "pctFAIL": "55",
                                                    "runs": [
                                                        {"result": "PASS", "startTime": "30291"},
                                                        {"result": "PASS", "startTime": "30291"},
                                                        {"result": "PASS", "startTime": "30291"}
                                                    ]
                                                }
                                            }
                                        ]
                                    ]
        """


        logging.info("Creating formatted data from all available report files.")
        results = self.get_all_reports_in_directory()

        all_tests = {}
        for result in results:
            group_name = result['testGroupName']
            if group_name in all_tests.keys():
                all_tests[group_name]["runs"].append(result)
            else:
                all_tests[group_name] = {"name": group_name, "runs": [result], "pass_fail": "IDK"}

        # get more detail on each test group
        for group_name, details in all_tests.items():
            runs = details['runs']
            more_detail = self.get_latest_result_details(runs)
            details.update(more_detail)

        # create a list of list, with each list containing X test groups. Each list will be a row in the UI
        final_data = []
        tmp = []
        for key, value in all_tests.items():
            tmp.append({key:value})
            if len(tmp) >= 3:
                final_data.append(tmp)
                tmp = []

        # means last item is in the tmp list so add it (it will be a list with 1 item)
        if tmp:
            final_data.append(tmp)

        return final_data