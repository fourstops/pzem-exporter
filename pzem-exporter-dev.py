import os
import time
from datetime import datetime
import logging
import argparse

from pzem import PZEM_016
from prometheus_client import start_http_server, Gauge, Histogram

logging.basicConfig(
    format='%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s',
    level=logging.INFO,
    handlers=[logging.FileHandler("pzem_exporter.log"),
              logging.StreamHandler()],
    datefmt='%Y-%m-%d %H:%M:%S')

DEBUG = os.getenv('DEBUG', 'false') == 'true'

pzem = PZEM_016("/dev/ttyUSB1")  # Replace with the correct pa>


VOLTAGE = Gauge('voltage','Voltage measured (V)')
CURRENT = Gauge('current','Current measured in amps (A)')
POWER = Gauge ('power','Power consumption measured (W-Hr)')
ENERGY = Gauge ('energy','Energy measured (W)')
FREQUENCY = Gauge ('frequency','AC frequency measured (Hz)')
POWER_FACTOR= Gauge ('power_factor','Power effeciency (%)')
ALARM = Gauge ('alarm', 'alarm status (boolean)')

def get_readings():
    reading = pzem.read()
    voltage = "Voltage", reading["voltage"]
    current = "Current", reading["current"]
    power = "Power", reading["power"]
    energy = "Energy", reading["energy"]
    frequency = "Frequency", reading["frequency"]
    power_factor = "Power_Factor", reading["power_factor"]
    alarm_status = "Alarm_Status", reading["alarm_status"]

    VOLTAGE.set(reading["voltage"])
    CURRENT.set(reading["current"])
    POWER.set(reading["power"])
    ENERGY.set(reading["energy"])
    FREQUENCY.set(reading["frequency"])
    POWER_FACTOR.set(reading["power_factor"])
    ALARM.set(reading["alarm_status"])
    return reading

def collect_all_data():
    """Collects all the data currently set"""
    sensor_data = {}
    sensor_data['voltage'] = VOLTAGE.collect()[0].samples[0].value
    sensor_data['current'] = CURRENT.collect()[0].samples[0].value
    sensor_data['power'] = POWER.collect()[0].samples[0].value
    sensor_data['energy'] = ENERGY.collect()[0].samples[0].value
    sensor_data['frequency'] = FREQUENCY.collect()[0].samples[0].value
    sensor_data['power_factor'] = POWER_FACTOR.collect()[0].samples[0].value
    sensor_data['alarm'] = ALARM.collect()[0].samples[0].value

    return sensor_data

def str_to_bool(value):
    if value.lower() in {'false', 'f', '0', 'no', 'n'}:
        return False
    elif value.lower() in {'true', 't', '1', 'yes', 'y'}:
        return True
    raise ValueError('{} is not a valid boolean value'.format(value))


def main() -> None:

    while True:
        reading = pzem.read()
        timestamp = datetime.utcfromtimestamp(reading["timestamp"])

        #logging.info(f"{reading}")

        # Limitation on InfluxDB to handle boolean type
        alarm_status = 1 if reading["alarm_status"] else 0

        #print(reading)
        #print ("Current", reading["current"])
        time.sleep(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--bind", metavar='ADDRESS', default='0.0.0.0', help="Specify alternate bind address [default: 0.0.0.0]")
    parser.add_argument("-p", "--port", metavar='PORT', default=8016, type=int, help="Specify alternate port [default: 8000]")
    parser.add_argument("-d", "--debug", metavar='DEBUG', type=str_to_bool, help="Turns on more verbose logging, showing sensor output and post responses [default: false]")
    args = parser.parse_args()

    start_http_server(addr=args.bind, port=args.port)

    if args.debug:
        DEBUG = True

    logging.info("Listening on http://{}:{}".format(args.bind, args.port))

    while True:
        get_readings()
        if DEBUG:
            logging.info('Sensor data: {}'.format(collect_all_data()))
        time.sleep (4)
