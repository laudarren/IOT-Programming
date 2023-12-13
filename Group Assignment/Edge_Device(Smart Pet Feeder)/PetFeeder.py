import time  #Import time library
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time

from flask import Flask, render_template

app = Flask(_name_)

myMQTTClient = AWSIoTMQTTClient("Cloud Server")
myMQTTClient.configureEndpoint("a5alkw0qczdkw-ats.iot.ap-southeast-1.amazonaws.com", 8883)
myMQTTClient.configureCredentials("/home/dylan/Desktop/Cert/AmazonRootCA1.pem", "/home/dylan/Desktop/Cert/8752c0b8aa60c77a014573b25df7166157fa743d8a37aea5e71f46ebd0b0074a-private.pem.key", "/home/dylan/Desktop/Cert/8752c0b8aa60c77a014573b25df7166157fa743d8a37aea5e71f46ebd0b0074a-certificate.pem.crt")
myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

myMQTTClient.connect()
myMQTTClient.publish("cloud/info", "connected", 0)


msg = { 
0: {'title' : 'Number 1', 'message' : 'Hello there'}
}

@app.route('/')
def index():
	templateData = { 'TheSet' : msg }
	return render_template('index.html',**templateData)

@app.route('/<action>')
def action(action):
	if action == 'action2':
		myMQTTClient.publish("cloud/data", "O", 0)
	if action == 'action1':
		myMQTTClient.publish("cloud/data", "C", 0)

	templateData = { 'TheSet' : msg }
	return render_template('index.html',**templateData)


if _name_ == "_main_":
	app.run(host='0.0.0.0',port=8080,debug=False)