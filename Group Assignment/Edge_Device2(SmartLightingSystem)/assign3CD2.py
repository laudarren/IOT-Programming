# Import libraries
import paho.mqtt.client as paho
import os
import socket
import ssl
import random
import string
import json
import time
import datetime
from time import sleep
from random import uniform

import serial
import mysql.connector
import time

device = '/dev/ttyUSB0'
arduino = serial.Serial(device, 9600, timeout=1)

connflag = False

def on_connect(client, userdata, flags, rc):
    global connflag
    print("Connect to AWS")
    connflag = True
    print("Connection returned result: " + str(rc))

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))

mqttc = paho.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message

awshost = "a1hep1576b3ncr-ats.iot.ap-southeast-1.amazonaws.com"
awsport = 8883
clientId = "huaxi_Client"
thingName = "huaxipi_Client"
caPath = "/home/huaxipi/certs/AmazonRootCA1.pem"
certPath = "/home/huaxipi/certs/7f62d1424115ec1eb7a275c9b31910c59e637182e9d72ce0a48b4635d991a49c-certificate.pem.crt"
keyPath = "/home/huaxipi/certs/7f62d1424115ec1eb7a275c9b31910c59e637182e9d72ce0a48b4635d991a49c-private.pem.key"

mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)

mqttc.connect(awshost, awsport, keepalive=60)

mqttc.loop_start()

while True:
    mydb = mysql.connector.connect(host="localhost",user="huaxipi",password="ninja020919",database="brightness_db")
    print(mydb)

    mycursor = mydb.cursor()

    mycursor.execute("SELECT COUNT(ldrSensor1) FROM ldrSensor WHERE ldrSensor1>300");
    rdata1 = mycursor.fetchall()
    print(rdata1[0][0]);

    mycursor.execute("SELECT COUNT(ldrSensor2) FROM ldrSensor WHERE ldrSensor2>300");
    rdata2 = mycursor.fetchall()
    print(rdata2[0][0]);

    totalForS1S2 = rdata1[0][0] + rdata2[0][0];

    mycursor.execute("SELECT COUNT(ldrSensor3) FROM ldrSensor WHERE ldrSensor3>300");
    rdata3 = mycursor.fetchall()
    print(rdata3[0][0]);

    mycursor.execute("SELECT COUNT(ldrSensor4) FROM ldrSensor WHERE ldrSensor4>300");
    rdata4 = mycursor.fetchall()
    print(rdata4[0][0]);

    totalForS3S4 = rdata3[0][0] + rdata4[0][0];

    clouddb = mysql.connector.connect(host="localhost",username="huaxipi",password="ninja020919",database="cloudSensor_db")
    print(clouddb)
    with clouddb:
        mycursor = clouddb.cursor()
        mycursor.execute("INSERT INTO countNum (count1,count2) VALUES (%s, %s)" %(totalForS1S2,totalForS3S4))
        clouddb.commit()
        mycursor.close()
        
        timestamp = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

    time.sleep(2)
    if connflag:
        payload_data = {
        'timestamp': str(timestamp),
        'Count 1': str(totalForS1S2),
        'Count 2': str(totalForS3S4)
    }

    payload_json = json.dumps(payload_data)
    mqttc.publish("rpi/lighting", payload_json, qos=1)
    print("Message sent: rpi/lighting")
    print(payload_json)
else:
    print("Waiting for connection...")

arduino.write(b"13" if totalForS1S2 > 50 else b"14")

    
    #if (totalForS3S4 > 50):
       # arduino.write(b"15")
    #else:
       # arduino.write(b"16")
    
time.sleep(1800);
