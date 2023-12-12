import time  #Import time library
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import serial

# AWS IoT certificate based connection
myMQTTClient = AWSIoTMQTTClient("huaxipi")
# myMQTTClient.configureEndpoint("YOUR.ENDPOINT", 8883)
myMQTTClient.configureEndpoint("a1hep1576b3ncr-ats.iot.ap-southeast-1.amazonaws.com", 8883)
myMQTTClient.configureCredentials("/home/huaxipi/certs/AmazonRootCA1.pem", "/home/huaxipi/certs/7f62d1424115ec1eb7a275c9b31910c59e637182e9d72ce0a48b4635d991a49c-private.pem.key", "/home/huaxipi/certs/7f62d1424115ec1eb7a275c9b31910c59e637182e9d72ce0a48b4635d991a49c-certificate.pem.crt")
myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

#connect and publish
myMQTTClient.connect()
myMQTTClient.publish("cloud/data", "connected", 0)

ser = serial.Serial("/dev/ttyUSB0", 9600, timeout=1)
ser.flush()
#myMQTTClient.publish("xxxx/info", "connected", 0)

def customCallback(client, userdata, message):
    print(message.payload)
    
    if message.payload == b'3':
        ser.write(b"1")
    if message.payload == b'4':
        ser.write(b"2")
    if message.payload == b'5':
        ser.write(b"3")
    if message.payload == b'6':
        ser.write(b"4")
        
while 1:
    time.sleep(2)
    myMQTTClient.subscribe("cloud/data", 0, customCallback)
        

