def select_sensor_last_data_query(sensor_id: int, sensor_type):
    return f"""SELECT data, timestamp FROM {sensor_type}
               WHERE sensor_id = {sensor_id} 
               ORDER BY timestamp DESC LIMIT 1;"""


def select_sensor_period_data_query(sensor_id: int, sensor_type, start_timestamp: int, end_timestamp: int):
    return f"""SELECT data, timestamp FROM {sensor_type}
                   WHERE (sensor_id = {sensor_id}) 
                   AND (timestamp BETWEEN {start_timestamp} AND {end_timestamp});"""


def insert_new_sensor_data(sensor_id: int, sensor_type, timestamp: int, sensor_data: float):
    return f"""INSERT INTO {sensor_type} VALUES ({sensor_id}, {timestamp}, {sensor_data})"""
