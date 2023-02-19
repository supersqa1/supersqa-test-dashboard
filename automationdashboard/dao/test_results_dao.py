import pymysql

from automationdashboard import app


class DBHelper:

    def __init__(self):

        self.host = app.config['DB_HOST']
        self.user = app.config['DB_USER']
        self.password = app.config['DB_PASSWORD']
        self.port = app.config['DB_PORT']

        if not self.host:
            raise Exception(f"Config values for 'DB_HOST' not found.")
        if not self.user:
            raise Exception(f"Config values for 'DB_USER' not found.")
        if not self.password:
            raise Exception(f"Config values for 'DB_PASSWORD' not found.")
        if not self.port:
            raise Exception(f"Config values for 'DB_PORT' not found.")


    def create_connection(self, db=None):
        connection = pymysql.connect(host=self.host,
                                          port=int(self.port),
                                          user=self.user,
                                          password=self.password,
                                          database=db,
                                          cursorclass=pymysql.cursors.DictCursor)

        return connection

    def execute(self, sql):

        connection = self.create_connection()

        with connection:
            with connection.cursor() as cursor:
                cursor.execute(sql)

            connection.commit()

    def select(self, sql):
        connection = self.create_connection()

        with connection:
            with connection.cursor() as cursor:
                cursor.execute(sql)
                all_rows = cursor.fetchall()

        return all_rows


class TestResultsDAO:


    def __init__(self):
        pass

    def get_all_test_results_from_db(self):

        sql = "SELECT * FROM automationdashboard.test_results;"
        rs_sql = DBHelper().select(sql)

        data = []
        for i in rs_sql:
            i.update({'start_time': str(i['start_time'])})
            i.update({'end_time': str(i['end_time'])})
            data.append(i)

        return data

    def get_test_results_by_test_group(self, test_group_name, start_time=None, end_time=None):

        filters = ""
        if start_time:
            filters = filters + f" AND start_time = '{start_time}'"
        if end_time:
            filters = f" AND end_time = '{end_time}'"

        sql = f"SELECT * FROM automationdashboard.test_results WHERE test_group_name = '{test_group_name}' " + filters + ";"
        app.logger.info(sql)
        # import pdb; pdb.set_trace()
        rs_sql = DBHelper().select(sql)

        data = []
        for i in rs_sql:
            i.update({'start_time': str(i['start_time'])})
            i.update({'end_time': str(i['end_time'])})
            data.append(i)


        return data

    def insert_test_result(self, result_object):
        data = dict()
        data['start_time'] = result_object.start_time
        data['end_time'] = result_object.end_time
        data['number_of_failed_tests'] = result_object.number_of_failed_tests
        data['number_of_passed_tests'] = result_object.number_of_passed_tests
        data['result_status'] = result_object.result_status
        data['test_group_name'] = result_object.test_group_name
        sql = f"""INSERT INTO `automationdashboard`.`test_results` (`test_group_name`, `result_status`, `number_of_passed_tests`,
                  `number_of_failed_tests`, `start_time`, `end_time`)
                 VALUES ("{result_object.test_group_name}", "{result_object.result_status}", {result_object.number_of_passed_tests}, {result_object.number_of_failed_tests},
                 "{result_object.start_time}", "{result_object.end_time}");"""

        DBHelper().execute(sql)