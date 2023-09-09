import pymysql
from calendar import timegm
from time import gmtime, sleep
from hub.database.database_queries import select_sensor_last_data_query, select_sensor_period_data_query, insert_new_sensor_data


class DataBaseServicer:

    def __init__(self, host, user, password, db, clean_timeout=None):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.clean_timeout = clean_timeout

    def connect(self):
        return pymysql.connect(host=self.host,
                                user=self.user,
                                password=self.password,
                                db=self.db,
                                charset='utf8mb4'
                                )

    def create_scheme(self):
        with self.connect() as connection:
            for table in ['temperature', 'humidity', 'light']:
                create_table_query = f"""CREATE TABLE {table}(
                                         sensor_id BIGINT,
                                         timestamp BIGINT,
                                         data FLOAT,
                                         PRIMARY KEY(sensor_id, timestamp)
                                         );"""
                with connection.cursor() as cursor:
                    try:
                        cursor.execute(create_table_query)
                        print(f'Created {table} table')
                    except pymysql.err.OperationalError:
                        print(f'Found existing {table} table')
            connection.commit()

    def insert_sensor_data(self, sensor_id, sensor_type, timestamp, sensor_data):
        with self.connect() as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(insert_new_sensor_data(sensor_id, sensor_type, timestamp, sensor_data))
                # Duplicate data
                except pymysql.err.IntegrityError:
                    pass
                except Exception as e:
                    print(str(e))
            connection.commit()

    def sensor_last_data(self, sensor_id, sensor_type):
        with self.connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute(select_sensor_last_data_query(sensor_id, sensor_type))
                response = cursor.fetchone()
            connection.commit()
        return response

    def sensor_period_data(self, sensor_id, sensor_type, start_timestamp, end_timestamp):
        with self.connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute(select_sensor_period_data_query(sensor_id, sensor_type,
                                                               start_timestamp, end_timestamp))
                response = cursor.fetchall()
            connection.commit()
        return response

    def clean_service(self):
        if not self.clean_timeout:
            return
        current_timestamp = timegm(gmtime())
        with self.connect() as connection:
            with connection.cursor() as cursor:
                for table in ['temperature', 'humidity', 'light']:
                    cursor.execute(f"""DELETE FROM {table} 
                                       WHERE timestamp < {current_timestamp + self.clean_timeout}""")
                connection.commit()

    def clean_task(self):
        while True:
            if not self.clean_timeout:
                break
            self.clean_service()
            sleep(self.clean_timeout)
