import time  #Import time library
import datetime
import json
import threading

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

import serial
import time
import mysql.connector


# AWS IoT certificate based connection
myMQTTClient = AWSIoTMQTTClient("LoRPI")
# myMQTTClient.configureEndpoint("a1hep1576b3ncr-ats.iot.ap-southeast-1.amazonaws.com", 8883)
myMQTTClient.configureEndpoint("a1hep1576b3ncr-ats.iot.ap-southeast-1.amazonaws.com", 8883)
myMQTTClient.configureCredentials("/home/wilsonlo99/cert/AmazonRootCA1.pem", "/home/wilsonlo99/cert/dbadb0b67b7cf03aad5f6e00b332c2d83a1e8dcbed1c2cbc2a69f510e2dfa9a3-private.pem.key", "/home/wilsonlo99/cert/dbadb0b67b7cf03aad5f6e00b332c2d83a1e8dcbed1c2cbc2a69f510e2dfa9a3-certificate.pem.crt")
myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

#connect and publish
myMQTTClient.connect()
myMQTTClient.publish("rpi/info", "connected", 0)

if __name__== '__main__':
    ser = serial.Serial('/dev/ttyUSB0',9600, timeout=1)
    ser.reset_input_buffer
    
    while 1:
        number = ser.read()
        if number != b'':
            if int.from_bytes(number, byteorder='big') == 18:
                pin_led = 1
                #print("Field 1: Grass detected")
                #print("Sending pin number " + str(pin_led) + " to Arduino.")
                ser.write(str(pin_led).encode('ascii'))
                
                
                
            elif int.from_bytes(number, byteorder='big') == 19:
                pin_led = 2
                #print("Field 2: Grass detected")
                #print("Sending pin number " + str(pin_led) + " to Arduino.")
                ser.write(str(pin_led).encode('ascii'))
               
                
            elif int.from_bytes(number, byteorder='big') == 20:
                pin_led = 3
                #print("Field 1: Moisture below 20")
                #print("Sending pin number " + str(pin_led) + " to Arduino.")
                ser.write(str(pin_led).encode('ascii'))
            
                
            elif int.from_bytes(number, byteorder='big') == 21:
                pin_led = 4
                #print("Field 2: Moisture below 20")
                #print("Sending pin number " + str(pin_led) + " to Arduino.")
                ser.write(str(pin_led).encode('ascii'))
                
            
            else:
                mydb = mysql.connector.connect(host="localhost",user="wilsonlo99",password="NOOBzai@12",database="sensor_db")
    
                print(mydb)
            
                while(ser.in_waiting == 0):
                    pass
            
                # Read serial output line from arduino & split the output into array of integer(values)
                line = ser.readline().strip().decode('utf-8')
                values = line.split(', ')
                print(values)
                moist_Field1 = float(values[1])
                moist_Field2 = float(values[2])
                distance_Field1 = int(values[3])
                distance_Field2 = int(values[4])
                temperature = float(values[5])
                
                #Forming a string of sensor data and publish it to cloud platform through MQTT broker
                timestamp = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
                
                payload = '{"timestamp": "' + str(timestamp) + '", "moisture1": ' + str(moist_Field1) + ', "moisture2": ' + str(moist_Field2) + ', "distance1": ' + str(distance_Field1) + ', "distance2": ' + str(distance_Field2) + ', "temperature": ' + str(temperature) +'}'

                print (payload)
                myMQTTClient.publish("rpi/data", payload, 0)
                
                #Funtion that handle the message from subscribed topic and perform specific action based on sent message
                def customCallback(client, userdata, message):
                    try:
                            # Parse the JSON payload
                            payload_dict = json.loads(message.payload.decode('utf-8'))
                            cloud_message = payload_dict.get('cloud message')
                            
                            if cloud_message == "action1":
                                print("{}".format(cloud_message))
                                pin_led = 1
                                ser.write(str(pin_led).encode('ascii'))
                            elif cloud_message == "action2":
                                print("{}".format(cloud_message))
                                pin_led = 2
                                ser.write(str(pin_led).encode('ascii'))
                            elif cloud_message == "action3":
                                print("{}".format(cloud_message))
                                pin_led = 5
                                ser.write(str(pin_led).encode('ascii'))
                            elif cloud_message == "action4":
                                print("{}".format(cloud_message))
                                pin_led = 6
                                ser.write(str(pin_led).encode('ascii'))
                            elif cloud_message == "action13":
                                print("{}".format(cloud_message))
                                pin_led = 7
                                ser.write(str(pin_led).encode('ascii'))
                            elif cloud_message == "action14":
                                print("{}".format(cloud_message))
                                pin_led = 8
                                ser.write(str(pin_led).encode('ascii'))
                            else:
                                print("Invalid or missing 'cloud message' field in payload.")
                                
                    except json.JSONDecodeError as e:
                            print("Error decoding JSON payload: {}".format(e))
                            
                #Subscribe to cloud/data topic and execute 'customCallback' function
                myMQTTClient.subscribe("cloud/data", 1, customCallback)
                
                with mydb:
                    mycursor = mydb.cursor()
                    # Insert sensor data into database
                    # Moisture
                    sql = "INSERT INTO moistLog (moisture_Field1, moisture_Field2) VALUES (%s, %s)"
                    values = (moist_Field1, moist_Field2)
                    mycursor.execute(sql, values)
                    # Distance
                    sql2 = "INSERT INTO distanceLog (distance_Field1, distance_Field2) VALUES (%s, %s)"
                    values2 = (distance_Field1, distance_Field2)
                    mycursor.execute(sql2, values2)
                    # Temperature
                    mycursor.execute("INSERT INTO tempLog (Temperature) VALUES (%s)" %(temperature))
                    
                    mydb.commit()
                    
                    
                    # Getting sensor data from database
                    # Moisture
                    sqlSelect = "SELECT moisture_Field1, moisture_Field2 FROM moistLog ORDER BY moistId DESC LIMIT 1"
                    mycursor.execute(sqlSelect)
                    
                    # Fetch the latest data
                    result = mycursor.fetchone()

                    if result:
                        moist_Field1, moist_Field2 = result
                        print(f"Latest Moisture Data - Field 1: {moist_Field1}, Field 2: {moist_Field2}")
                    
                    # Distance
                    sqlSelect2 = "SELECT distance_Field1, distance_Field2 FROM distanceLog ORDER BY distanceId DESC LIMIT 1"
                    mycursor.execute(sqlSelect2)
                    
                    result2 = mycursor.fetchone()
                    if result2:
                        distance_Field1, distance_Field2 = result2
                        print(f"Latest Distance Data - Field 1: {distance_Field1}, Field 2: {distance_Field2}")
                            
                    # Temperature
                    sqlSelect3 = "SELECT temperature FROM tempLog ORDER BY tempId DESC LIMIT 1"
                    mycursor.execute(sqlSelect3)
                    
                    result3 = mycursor.fetchone()
                    if result3:
                        temperature = result3[0]
                        print(f"Latest Temperature Data: {temperature}")
                        
                    mycursor.close()
