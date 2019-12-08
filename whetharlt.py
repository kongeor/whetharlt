import random
import time
import sys
import os
import logging
from dotenv import load_dotenv

load_dotenv(verbose=True)

# config logging

root = logging.getLogger()
root.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)

# config adafruit

from Adafruit_IO import Client, Data
aio = Client(os.getenv('ADAFRUIT_USER'), os.getenv('ADAFRUIT_KEY'))

# bme
# copied from: https://github.com/pimoroni/bme680-python/blob/master/examples/read-all.py

try:
    sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
except IOError:
    sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)

# These calibration data can safely be commented
# out, if desired.

print('Calibration data:')
for name in dir(sensor.calibration_data):

    if not name.startswith('_'):
        value = getattr(sensor.calibration_data, name)

        if isinstance(value, int):
            print('{}: {}'.format(name, value))

# These oversampling settings can be tweaked to
# change the balance between accuracy and noise in
# the data.

sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)
sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)

print('\n\nInitial reading:')
for name in dir(sensor.data):
    value = getattr(sensor.data, name)

    if not name.startswith('_'):
        print('{}: {}'.format(name, value))

sensor.set_gas_heater_temperature(320)
sensor.set_gas_heater_duration(150)
sensor.select_gas_heater_profile(0)

# Up to 10 heater profiles can be configured, each
# with their own temperature and duration.
# sensor.set_gas_heater_profile(200, 150, nb_profile=1)
# sensor.select_gas_heater_profile(1)


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
    if sensor.get_sensor_data():
        push_feed_data('temperature', sensor.data.temperature)
        push_feed_data('pressure', sensor.data.pressure)
        push_feed_data('humidity', sensor.data.humidity)

        if sensor.data.heat_stable:
            push_feed_data('gasres', sensor.data.gas_resistance)

        else:
            print(output)

    # testing
    # data = get_sample_data();
    # push_feed_data('temperature', data['temperature'])
    # push_feed_data('pressure', data['pressure'])
    # push_feed_data('humidity', data['humidity'])
    # push_feed_data('gasres', data['gasres'])

    time.sleep(60)