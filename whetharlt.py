# Import library and create instance of REST client.
import random
import time
import sys
import os
import logging
from dotenv import load_dotenv

load_dotenv(verbose=True)


root = logging.getLogger()
root.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)

from Adafruit_IO import Client, Data
aio = Client(os.getenv('ADAFRUIT_USER'), os.getenv('ADAFRUIT_KEY'))

def get_sample_data():
    return {
        'temperature':  random.random() * 10,
        'pressure': random.random() * 10,
        'humidity': random.random() * 10,
        'gasres' : random.random() * 10
    }

def push_feed_data(feed, val):
    try:
        logging.info('Pushing %s: %s', feed, val)
        data = Data(value=val)
        aio.create_data(feed, data)
    except:
        logging.exception("Unexpected error")


while True:
    data = get_sample_data();
    push_feed_data('temperature', data['temperature'])
    push_feed_data('pressure', data['pressure'])
    push_feed_data('humidity', data['humidity'])
    push_feed_data('gasres', data['gasres'])
    time.sleep(20)