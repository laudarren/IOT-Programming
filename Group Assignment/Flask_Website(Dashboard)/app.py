import time 
from flask import Flask, render_template 

import boto3
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

# AWS IoT certificate based connection
myMQTTClient = AWSIoTMQTTClient("MyCloudComputer")
# myMQTTClient.configureEndpoint("YOUR.ENDPOINT", 8883)
myMQTTClient.configureEndpoint("a1hep1576b3ncr-ats.iot.ap-southeast-1.amazonaws.com", 8883)
myMQTTClient.configureCredentials("/home/ubuntu/cert/AmazonRootCA1.pem", "/home/ubuntu/cert/132545bbe9e2702e12b4569f0c2c1797cbda4c81eddb003529832ddca43581a6-private.pem.key", "/home/ubuntu/cert/132545bbe9e2702e12b4569f0c2c1797cbda4c81eddb003529832ddca43581a6-certificate.pem.crt")
myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

#connect and publish
myMQTTClient.connect()

app = Flask (__name__) 

@app.route("/") 
def index():
    
    return render_template('index.html') 

@app.route("/<action>") 
def action(action): 
    #Action for Garden Node
    if action == 'action1' : 
        payload = '{"cloud message":"'+ "action1" +'"}'
        myMQTTClient.publish("cloud/data", payload, 0)
    if action == 'action2' : 
        payload = '{"cloud message":"'+ "action2" +'"}'
        myMQTTClient.publish("cloud/data", payload, 0)
    if action == 'action3' : 
        payload = '{"cloud message":"'+ "action3" +'"}'
        myMQTTClient.publish("cloud/data", payload, 0)
    if action == 'action4' : 
        payload = '{"cloud message":"'+ "action4" +'"}'
        myMQTTClient.publish("cloud/data", payload, 0)
    #Action for Door node
    if action == 'action5' :
        myMQTTClient.publish("cloud/data", 1, 0)
    if action == 'action6' :
        myMQTTClient.publish("cloud/data", 2, 0)
    #Action for Lighting node
    if action == 'action7' :
        myMQTTClient.publish("cloud/data", 3, 0)
    if action == 'action8' :
        myMQTTClient.publish("cloud/data", 4, 0)
    if action == 'action9' :
        myMQTTClient.publish("cloud/data", 5, 0)
    if action == 'action10' :
        myMQTTClient.publish("cloud/data", 6, 0)
    #Action for Pet node
    if action == 'action11' :
        myMQTTClient.publish("cloud/data", 7, 0)
    if action == 'action12' :
        myMQTTClient.publish("cloud/data", 8, 0)
    #Additional action for Garden node
    if action == 'action13' : 
        payload = '{"cloud message":"'+ "action13" +'"}'
        myMQTTClient.publish("cloud/data", payload, 0)
    if action == 'action14' : 
        payload = '{"cloud message":"'+ "action14" +'"}'
        myMQTTClient.publish("cloud/data", payload, 0)
    
    
    return render_template('index.html')
    
if __name__ == "__main__" :
     
    app.run(host='0.0.0.0', port = 8080, debug = False) 
    