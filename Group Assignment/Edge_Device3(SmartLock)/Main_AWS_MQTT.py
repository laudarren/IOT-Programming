import time  #Import time library
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import serial

# AWS IoT certificate based connection
myMQTTClient = AWSIoTMQTTClient("DarrenRPI")
# myMQTTClient.configureEndpoint("YOUR.ENDPOINT", 8883)
myMQTTClient.configureEndpoint("a1hep1576b3ncr-ats.iot.ap-southeast-1.amazonaws.com", 8883)
myMQTTClient.configureCredentials("/home/pi/SWE30011/Darren/AmazonRootCA1.pem", "/home/pi/SWE30011/Darren/1aa4dad3ba697077218bc9433fd2a1fa3eb3d8f768b02490d0e2a77eaf38824b-private.pem.key", "/home/pi/SWE30011/Darren/1aa4dad3ba697077218bc9433fd2a1fa3eb3d8f768b02490d0e2a77eaf38824b-certificate.pem.crt")
myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

ser=serial.Serial('/dev/ttyUSB0',9600,timeout = 1)
ser.flush()

# Custom callback when a message is received
def customCallback(client, userdata, message):
    print(message.payload)
    
    if message.payload == b'1':
        ser.write(b"1")
    if message.payload == b'2':
        ser.write(b"2")
        
#connect and publish
myMQTTClient.connect()
myMQTTClient.publish("cloud/info", "connected", 0)
#myMQTTClient.publish("xxxx/info", "connected", 0)



while 1:
    time.sleep(2)  # Adjust the sleep interval as needed
    myMQTTClient.subscribe("cloud/data", 0, customCallback)
