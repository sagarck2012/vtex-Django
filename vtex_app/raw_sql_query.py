def get_avg_rssi_values_per_hour(device_reg_id):
    query = '''
          SELECT 
          CAST(AVG(rssi_value) AS DECIMAL(10,2)) AS RSSI,
          DATE(TIMESTAMP) AS DAY,
          HOUR(TIMESTAMP) AS HOUR,
          TIME_FORMAT(TIMESTAMP, '%h:%i %p') AS t101 
            FROM
          adc_data 
          WHERE device_reg_id = ''' + str(device_reg_id) + ''' GROUP BY DAY(TIMESTAMP),
          HOUR(TIMESTAMP) 
          HAVING t101 BETWEEN '00:00 AM' 
          AND '23:59 PM' AND DAY = CURDATE()'''

    return query


def get_avg_rssi_values_per_day(duration, device_reg_id):
    query = '''
          SELECT 
          CAST(AVG(rssi_value) AS DECIMAL(10,2)) AS RSSI,
          DATE(TIMESTAMP) AS DAY
            FROM
          adc_data 
          WHERE device_reg_id = ''' + str(device_reg_id) + ''' GROUP BY DAY
          HAVING DAY BETWEEN DATE_ADD(CURDATE(), INTERVAL -''' + str(duration) + ''' DAY) 
          AND CURDATE()-1'''

    return query


def get_avg_rpm_values_and_count_per_hour(device_reg_id):
    query = '''SELECT 
          CAST((SUM(rpm_value)/60) AS DECIMAL (10,2)) AS RPM, 
          DATE(TIMESTAMP) AS DAY,
          HOUR(TIMESTAMP) AS HOUR,
          COUNT(rpm_status) AS COUNT,
          TIME_FORMAT(TIMESTAMP, '%h:%i %p') AS t 
        FROM
          rpm_data 
        WHERE rpm_status = 1 
          AND device_reg_id =''' + str(device_reg_id) + ''' GROUP BY DAY(TIMESTAMP),
          HOUR(TIMESTAMP) 
        HAVING t BETWEEN '00:00 AM' 
          AND '23:59 PM' 
          AND DAY = CURDATE()'''
    return query


def get_avg_rpm_values_and_count_per_day(duration, device_reg_id):
    query = '''SELECT 
              CAST((SUM(rpm_value) / 60) AS DECIMAL (10, 2)) AS RPM,
              DATE(TIMESTAMP) AS DAY,
              COUNT(rpm_status) AS COUNT
            FROM
              rpm_data 
            WHERE rpm_status = 1 
              AND device_reg_id = ''' + str(device_reg_id) + ''' 
            GROUP BY DAY 
            HAVING DAY BETWEEN DATE_ADD(CURDATE(), INTERVAL - ''' + str(duration) + ''' DAY) 
              AND CURDATE() - 1 
             '''
    return query


