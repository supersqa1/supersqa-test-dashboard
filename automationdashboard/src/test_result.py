


class TestResult:

    def __init__(self, start_time, end_time, number_of_passed_tests, number_of_failed_tests, test_group_name, result_status):
        self.start_time = start_time
        self.end_time = end_time
        self.number_of_passed_tests = number_of_passed_tests
        self.number_of_failed_tests = number_of_failed_tests
        self.test_group_name = test_group_name
        self.result_status = result_status.upper()

        if self.result_status not in ("PASS", "FAIL"):
            raise ValueError(f"Invalid value '{self.result_status}' for 'result_status'. Valid values are 'PASS' and 'FAIL' only.")


