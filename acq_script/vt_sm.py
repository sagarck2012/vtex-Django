import paho.mqtt.client as mqtt
from threading import Timer
import time
import json
import random
import uuid


id = uuid.uuid1()
client_id = id.hex
client =mqtt.Client(client_id)


broker = "182.163.112.102"
port = 1883
# client.username_pw_set("ds_broker", "Ds@iot123")
broker_user = "iotdatasoft"
broker_password = "brokeriot2o2o"


def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))


def on_message(client, userdata, message):
  print("topic: "+message.topic+"	"+"payload: "+str(message.payload))
  print('\n')


client.on_connect = on_connect  #attach the callback function to the client object 
client.on_message = on_message	#attach the callback function to the client object 

#device & variables
dev_id = ["VT001"]
adc_val = [58, 60, 102, 110, 112, 116, 130]
rpm = [22]
rssi = -55
client.username_pw_set(username=broker_user, password=broker_password)
client.connect(broker, port, 60)
print("connecting to broker")

# client.loop_start() #start the loop
# client.subscribe("sensor/data")
# print("subscribed")


def publish():
  for did in dev_id:
    adc_Data={
    "did": did,
    "adc": random.choice(adc_val),
    "rssi": rssi
    }

    rpm_Data = {
      "did": did,
      "rpm": random.choice(rpm)
    }


    adc_json = json.dumps(adc_Data)
    rpm_json = json.dumps(rpm_Data)
    print(f"rpm_json {rpm_json}")
    client.publish("dsiot/vt/mrtime", adc_json )  # publish
    client.publish("dsiot/vt/rpm", rpm_json )
    

def timer():
  publish() # initialise the function
  Timer(10.0, timer).start() # publish every 60 seconds

timer()

# time.sleep(4) # wait
# client.loop_stop() #stop the loop
client.loop_forever() # to maintain continuous network traffic flow with the broker

