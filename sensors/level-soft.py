import numpy as np
import time

def publish(data):
    print(data)

def read():
    return np.round(np.random.rand() * 1000)

while(True):
    publish(read())
    time.sleep(1)

