import paho.mqtt.client as mqtt
import time
import random
import json
import numpy as np

#Constants to connect to MQTT
broker = "34.143.239.132"
port = 3005
topic = "ditto-tutorial"
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = "ditto"
password = "ditto"

# Digital twin info
namespace = "myreservoir"
res_name = "reservoir"
gate_name = "spill_gate"

# MQTT connection
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Successful connection")
    else:
        print(f"Connection failed with code {rc}")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
#client.username_pw_set(username, password)
client.on_connect = on_connect
client.connect(broker, port)

# Data generator
def generate_gate_data():
    raised_level = random.uniform(0, 100)
    flow_rate = random.uniform(0, 45)
    return raised_level, flow_rate

def generate_res_data():
    temparature = random.uniform(10, 35)
    water_level = random.uniform(0, 150)
    humidity = random.uniform(0, 100) 
    return temparature, water_level, humidity

# Ditto Protocol
def get_ditto_protocol_value_res(time, temperature, water_level, humidity):
    return {
        "temperature" : {
            "properties": {
                "value":temperature
            }
        },
        "water_level": {
            "properties": {
                "value":water_level
            }
        },
        "humidity": {
            "properties": {
                "value":humidity
            }
        }
    }

def get_ditto_protocol_value_gate(time, raised_level, flow_rate):
    return {
        "raised_level" : {
            "properties": {
                "value":raised_level
            }
        },
        "flow_rate": {
            "properties": {
                "value":flow_rate
            }
        }
    }

def get_ditto_protocol_msg(name, value):
    return {
        "topic": "{}/{}/things/twin/commands/merge".format(namespace, name),
        "headers": {
            "content-type": "application/merge-patch+json"
        },
        "path": "/features",
        "value": value
    }

# Send data
try:
    while True:
        t = round(time.time() * 1000) # Unix ms
        
        # res twin
        temperature, water_level, humidity = generate_res_data()
        msg = get_ditto_protocol_msg(res_name, get_ditto_protocol_value_res(t, temperature, water_level, humidity))
        client.publish(topic+ "/" + namespace + "/" + res_name, json.dumps(msg))
        print(topic+ "/" + namespace + "/" + res_name + " data published")
        
        # gate twins
        for i in range(1,2):
            name = gate_name+str(i)
            opening_height, flow_rate = generate_gate_data()
            msg = get_ditto_protocol_msg(name, get_ditto_protocol_value_gate(t, opening_height, flow_rate))
            client.publish(topic+ "/" + namespace + "/" + name, json.dumps(msg))
            print(topic+ "/" + namespace + "/" + name + " data published")
        
        time.sleep(5)
        
except KeyboardInterrupt:
    client.disconnect()