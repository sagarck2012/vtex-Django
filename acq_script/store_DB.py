# _*_ coding: utf-8 _*_

#------------------------------------------
#--- Author: Sagar Chakraborty
#--- Date: 11th May 2020
#--- Version: 1.0
#--- Python Ver: 3.8
#------------------------------------------

#Importing libraries
import pymysql
import json
import datetime
import logging
import pytz
from string import Template


#Global Variables
host = "localhost"
user = "root"
password = "Admin@2019"
db = "vtex"




#Config logging format
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO) #Below this level data will be printed to console
file_handler = logging.FileHandler('./projectlog/project_log_'+str(datetime.datetime.now().strftime('%Y-%m-%d'))+".txt")
format = "%(asctime)s :: Source %(name)s :: Line No %(lineno)d :: %(levelname)s ::  %(message)s"
formatter = logging.Formatter(format)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


# Master Function to Select DB Funtion based on MQTT Topic

def sensor_Data_Handler(Topic, jsonData):
	logger.debug("Inside sensor data handler")
	print("Inside sensor data handler")
	if Topic == "dsiot/vt/mrtime":
		logger.debug(jsonData)
		database_handler(Topic, jsonData)

	elif Topic == "dsiot/vt/rpm":
		logger.debug(jsonData)
		rpm_database_handler(Topic, jsonData)


#===============================================================



#===============================================================
# Functions to push Sensor Data into Database
#===============================================================

#===============================================================
# Insert Raw Positioning data to table
def database_handler(Topic, jsonData):
	# time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

	dataJson = json.loads(jsonData)
	dev_id = dataJson["did"]
	adc = dataJson["adc"]
	rssi = dataJson["rssi"]
	if adc > 60:
		device_status = 1
	else:
 		device_status = 0


	# print("device_status: " + device_status)
	


	try:
		conn = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)
		#get device registration ID
		cursor2 = conn.cursor()
		sql = "SELECT `id` FROM `device_reg` WHERE `device_id` = %s"
		cursor2.execute(sql,(dev_id))
		row = cursor2.fetchone()
		# print("Rowcount:",cursor2.rowcount)
		if cursor2.rowcount > 0:

			cursor2.close()
			del cursor2
			
			# Push into DB Table
			cursor = conn.cursor()
			sql = "INSERT INTO `adc_data`(`adc_value`, `rssi_value`, device_status, `device_reg_id`, `timestamp`, `acq_script`, `topic`) VALUES (%s,%s,%s,%s,%s,%s,%s)"
			cursor.execute(sql,(adc, rssi, device_status, row["id"], datetime.datetime.now(pytz.timezone("Asia/Dhaka")).replace(tzinfo=None), "vtex_reciever.py", Topic))
			conn.commit()
			logger.debug("Data inserted to database")
			print("Data inserted to database")

			cursor.close()
			del cursor
		
		else:
			pass
	except Exception as e:
		logger.error("Data insertion failed")
		logger.error(e)



#===============================================================



#===============================================================
# Functions to push Sensor Data into Database
#===============================================================

#===============================================================
# Insert Raw Positioning data to table
def rpm_database_handler(Topic, jsonData):
	# time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

	dataJson = json.loads(jsonData)
	dev_id = dataJson["did"]
	rpm = dataJson["rpm"]
	if rpm <= 10 :
		rpm_status = 0
            # Machine not running
	if rpm >= 11 and rpm <= 20 :
		rpm_status = 2
            # Low RPM
	if rpm > 20 :
		rpm_status = 1


	# print("device_status: " + device_status)
	


	try:
		conn = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)
		#get device registration ID
		cursor2 = conn.cursor()
		sql = "SELECT `id` FROM `device_reg` WHERE `device_id` = %s"
		cursor2.execute(sql, (dev_id))
		row = cursor2.fetchone()
		print(row)
		if cursor2.rowcount > 0:

			cursor2.close()
			del cursor2
			
			# Push into DB Table
			cursor = conn.cursor()
			sql = "INSERT INTO `rpm_data`(`rpm_value`,rpm_status, `device_reg_id`, `timestamp`, `acq_script`, `topic`) VALUES (%s,%s,%s,%s,%s,%s)"
			cursor.execute(sql,(rpm, rpm_status, row["id"], datetime.datetime.now(pytz.timezone("Asia/Dhaka")).replace(tzinfo=None), "vtex_reciever.py", Topic))
			conn.commit()
			logger.debug("Data inserted to database")

			cursor.close()
			del cursor

			# Push into DB Table
			cursor3 = conn.cursor()
			sql3 = "UPDATE `device_reg` SET rpm_status=%s WHERE device_id = %s"
			cursor3.execute(sql3,(rpm_status, dev_id))
			conn.commit()
			logger.debug("Data updated to database")
			print("Data updated to database")

			cursor3.close()
			del cursor3

		else:
			pass

	
	except Exception as e:
		logger.error("Data insertion failed")
		print("Data insertion failed")
		logger.error(e)
		print(e)



#===============================================================




