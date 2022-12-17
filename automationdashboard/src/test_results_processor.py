

from automationdashboard import app
from automationdashboard.dao.test_results_dao import TestResultsDAO


import json
import logging
import os
from datetime import datetime





class TestResultsProcessor:

    def __init__(self):
        self.data_storage = app.config.get("DATA_STORAGE")
        assert self.data_storage and self.data_storage.lower() in ('database', 'file'), \
            f"Invalid value '{self.data_storage}' for config 'DATA_STORAGE'. Valid values are 'database' or 'file'."

        self.data_storage = self.data_storage.lower()
        if self.data_storage == 'file':
            self.results_dir = app.config.get("RESULTS_DIR")
            if not self.results_dir:
                raise Exception("Config key 'RESULTS_DIR' must be set.")

    @staticmethod
    def convert_result_object_to_dict(result_object): # should this be called serialize

        data = dict()
        data['start_time'] = result_object.start_time
        data['end_time'] = result_object.end_time
        data['number_of_failed_tests'] = result_object.number_of_failed_tests
        data['number_of_passed_tests'] = result_object.number_of_passed_tests
        data['result_status'] = result_object.result_status
        data['test_group_name'] = result_object.test_group_name


        return data

    def store_report(self, result_object):
      
        if self.data_storage == 'database':
            self.store_test_result_in_db(result_object)
        elif self.data_storage == 'file':
            self.store_report_in_file(result_object)

    def store_report_in_file(self, result_object):
        """
        Creates a .json file and aves the report data in the file.
        Uses the current datetime as file name

        :param report_data: must be a dictionary or json object
        :return: None
        """
        report_data = self.convert_result_object_to_dict(result_object)
        # Check if the folder exist
        is_exist = os.path.exists(self.results_dir) and os.path.isdir(self.results_dir)
        if not is_exist:
            os.makedirs(self.results_dir)

        # create a file with the current datetime as file name
        timestamp = datetime.now().strftime('%Y%m%d%H%M%s')
        result_file_path = os.path.join(self.results_dir, timestamp) + ".json"
        with open(result_file_path, 'w') as f:
            f.write(json.dumps(report_data))

    def store_test_result_in_db(self, test_result_object):

        TestResultsDAO().insert_test_result(test_result_object)

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
            try:
                with open(f_name, 'r') as f:
                    data = json.load(f)
                    # TODO: why does this fail if file is empty
            except Exception as e:
                logging.error(e)

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
            start_datetime_obj = datetime.strptime(str(i['start_time']), "%Y-%m-%d %H:%M:%S")
            if start_datetime_obj > latest:
                latest = datetime.strptime(str(i['start_time']), "%Y-%m-%d %H:%M:%S")
                latest_info['latest_status'] = i['result_status']
                latest_info['latest_pass'] = i['number_of_passed_tests']
                latest_info['latest_fail'] = i['number_of_failed_tests']
                latest_info['total'] = int(i['number_of_passed_tests']) + int(i['number_of_failed_tests'])
                latest_info['pct_pass'] = round(int(i['number_of_passed_tests'])/latest_info['total'] * 100, )

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

        data_storage = app.config.get("DATA_STORAGE")

        if data_storage.lower() == 'database':
            results = TestResultsDAO().get_all_test_results_from_db()
        elif data_storage.lower() == 'file':
            results = self.get_all_reports_in_directory()
        else:
            raise Exception(f"Invalid value '{data_storage}' for config 'DATA_STORAGE'. Valid values are 'database' or 'file'.")

        formatted_results = self.format_data_for_fe(results)

        return formatted_results

    def format_data_for_fe(self, results):

        all_tests = {}
        for result in results:
            group_name = result['test_group_name']
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

    def get_data_from_db(self):
        results = TestResultsDAO().get_all_test_results_from_db()
        formatted_results = self.format_data_for_fe(results)
        return formatted_results

