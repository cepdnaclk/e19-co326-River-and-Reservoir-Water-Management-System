from paho.mqtt import client as mqtt_client
import time
import random
import json
import numpy as np
#Constants to connect to MQTT
broker = "test.mosquitto.org"
port = 1883
topic = "ditto-tutorial"
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = "ditto"
password = "ditto"

#Constantes para crear el mensaje de Eclipse Ditto
DITTO_NAMESPACE = "reservoir";
DITTO_THING_ID = "gate";

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    # Set Connecting Client ID
    client = mqtt_client.Client(client_id)
    #client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def publish(client):
     while True:
         time.sleep(1)
         msg = getValues();
         if msg is not None:
            result = client.publish(topic, msg)
            status = result[0]
            if status == 0:
                print(f"Send '{msg}' to topic '{topic}'")
            else:
                print(f"Failed to send message to topic {topic}")

def getValues():
    raised_level, flow_rate= np.random.random(), np.random.random()
    if raised_level is not None and flow_rate is not None:
        raised_level = "{0:0.1f}".format(raised_level)
        flow_rate = "{0:0.1f}".format(flow_rate)
        output =  "{\"topic\": \""
        output += DITTO_NAMESPACE
        output += "/"
        output += DITTO_THING_ID
        output += "/things/twin/commands/modify\",\"headers\":{\"response-required\":false, \"content-type\":\"application/vnd.eclipse.ditto+json\"},"
        output += "\"path\": \"/features\", \"value\":{"
        output += sensorString("raised_level", raised_level) 
        output += ","
        output += sensorString("flow_rate", flow_rate)
        output += "}}"
        return output
    else:
        print("Failed on lecture, check circuit")
        return None

def sensorString(name, value):
    return "\"" + name + "\": { \"properties\": { \"value\": " + value + "}}"; 

def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)

if __name__ == '__main__':
    run()
