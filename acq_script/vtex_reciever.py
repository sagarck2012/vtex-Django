# _*_ coding: utf-8 _*_

#------------------------------------------
#--- Author: Sagar Chakraborty
#--- Date: 11th May 2020
#--- Version: 1.0
#--- Python Ver: 3.8
#------------------------------------------

import paho.mqtt.client as mqtt
from threading import Timer
import datetime
import time as t
import json
import random
import uuid
import logging
from store_DB import sensor_Data_Handler
# from . import store_DB

#variables
sub_topic = "dsiot/vt/#"
id = uuid.uuid1()
client_id = "acquisition_Script"+id.hex
#broker= "broker.datasoft-bd.com"
broker = "182.163.112.102"
port =1883
user = "iotdatasoft"
password = "brokeriot2o2o"

#Config logging format
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG) #Below this level data will be printed to console
file_handler = logging.FileHandler('./projectlog/project_log_'+str(datetime.datetime.now().strftime('%Y-%m-%d'))+".txt")
format = "%(asctime)s :: Source %(name)s :: Line No %(lineno)d :: %(levelname)s ::  %(message)s"
formatter = logging.Formatter(format)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)



# # Function to add debug print
# def tprint(var):
#     print(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+" :: "+str(var)+"\n")

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logger.debug("Connection successful")
    elif rc == 1:
        logger.error("Connection refused – incorrect protocol version")
    elif rc == 2:
        logger.error("Connection refused – invalid client identifier")
    elif rc == 3:
        logger.error("Connection refused – server unavailable")
    elif rc == 4:
        logger.error("Connection refused – bad username or password")
    elif rc == 5:
        logger.error("Connection refused – not authorised")
    else:
        logger.error("Connection error")    
    logger.info("Connected with result code "+str(rc))


def on_message(client, userdata, message):
    logger.debug("topic: "+message.topic+"	"+"payload: "+str(message.payload))
    # tprint('\n')
    # data = json.loads(message.payload)
    sensor_Data_Handler(message.topic, message.payload)


def on_publish(client,userdata,result):             #create function for callback
    logger.debug("data published \n")
    return result


client = mqtt.Client(client_id)  # Create instance of client with client ID “digi_mqtt_test”
client.on_connect = on_connect  # Define callback function for successful connection
client.on_message = on_message  # Define callback function for receipt of a message
client.username_pw_set(username=user,password= password)

client.connect(broker, port, 60)
t.sleep(0.25)


client.subscribe(sub_topic)
t.sleep(0.25)
logger.info ("subscribed")
print("Project Initiating")
t.sleep(1)
print("Launch Code Generated.")
t.sleep(1)
print("Looking into system variables")
t.sleep(1)
print("Project initiating in 3 seconds")
t.sleep(1)
a = 3
while a>0:
    print(".")
    a = a-1
    t.sleep(1)
print("Project Successfully launched")

client.loop_forever()  # Start networking daemon
