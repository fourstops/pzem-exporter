import os
import time
from datetime import datetime
import logging
import argparse
from subprocess import check_output

from pzem import PZEM_016
from prometheus_client import start_http_server, Gauge, Histogram

logging.basicConfig(
    format='%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s',
    level=logging.INFO,
    handlers=[logging.FileHandler("pzem_exporter.log"),
              logging.StreamHandler()],
    datefmt='%Y-%m-%d %H:%M:%S')

DEBUG = os.getenv('DEBUG', 'false') == 'true'

pzem_1 = PZEM_016("/dev/ttyUSB0")  # Replace with the correct path
pzem_2 = PZEM_016("/dev/ttyUSB1")

P1_VOLTAGE = Gauge('p1_voltage','Voltage measured (V)') # 'voltage' is metric name followed by description
P1_CURRENT = Gauge('p1_current','Current measured in amps (A)')
P1_POWER = Gauge ('p1_power','Power consumption measured (W-Hr)')
P1_ENERGY = Gauge ('p1_energy','Energy measured (W)')
P1_FREQUENCY = Gauge ('p1_frequency','AC frequency measured (Hz)')
P1_POWER_FACTOR= Gauge ('p1_power_factor','Power effeciency (%)')
P1_ALARM = Gauge ('p1_alarm', 'alarm status (boolean)')

P2_VOLTAGE = Gauge('p2_voltage','Voltage measured (V)') # 'voltage' is metric name followed by description
P2_CURRENT = Gauge('p2_current','Current measured in amps (A)')
P2_POWER = Gauge ('p2_power','Power consumption measured (W-Hr)')
P2_ENERGY = Gauge ('p2_energy','Energy measured (W)')
P2_FREQUENCY = Gauge ('p2_frequency','AC frequency measured (Hz)')
P2_POWER_FACTOR= Gauge ('p2_power_factor','Power effeciency (%)')
P2_ALARM = Gauge ('p2_alarm', 'alarm status (boolean)')

def get_readings():
    p1_reading = pzem_1.read()

    p1_voltage = "Voltage",p1_reading["voltage"]
    p1_current = "Current",p1_reading["current"]
    p1_power = "Power",p1_reading["power"]
    p1_energy = "Energy",p1_reading["energy"]
    p1_frequency = "Frequency",p1_reading["frequency"]
    p1_power_factor = "Power_Factor",p1_reading["power_factor"]
    p1_alarm_status = "Alarm_Status",p1_reading["alarm_status"]

    p2_reading = pzem_2.read()
    p2_voltage = "Voltage",p2_reading["voltage"]
    p2_current = "Current",p2_reading["current"]
    p2_power = "p2_power",p2_reading["power"]
    p2_energy = "Energy",p2_reading["energy"]
    p2_frequency = "Frequency",p2_reading["frequency"]
    p2_power_factor = "Power_Factor",p2_reading["power_factor"]
    p2_alarm_status = "Alarm_Status",p2_reading["alarm_status"]

    P1_VOLTAGE.set(p1_reading["voltage"])
    P1_CURRENT.set(p1_reading["current"])
    P1_POWER.set(p1_reading["power"])
    P1_ENERGY.set(p1_reading["energy"])
    P1_FREQUENCY.set(p1_reading["frequency"])
    P1_POWER_FACTOR.set(p1_reading["power_factor"])
    P1_ALARM.set(p1_reading["alarm_status"])

    P2_VOLTAGE.set(p2_reading["voltage"])
    P2_CURRENT.set(p2_reading["current"])
    P2_POWER.set(p2_reading["power"])
    P2_ENERGY.set(p2_reading["energy"])
    P2_FREQUENCY.set(p2_reading["frequency"])
    P2_POWER_FACTOR.set(p2_reading["power_factor"])
    P2_ALARM.set(p2_reading["alarm_status"])
    return p1_reading, p2_reading

def collect_all_data():
    """Collects all the data currently set"""
    sensor_data = {}
    sensor_data['voltage'] = P1_VOLTAGE.collect()[0].samples[0].value
    sensor_data['current'] = P1_CURRENT.collect()[0].samples[0].value
    sensor_data['power'] = P1_POWER.collect()[0].samples[0].value
    sensor_data['energy'] = P1_ENERGY.collect()[0].samples[0].value
    sensor_data['frequency'] = P1_FREQUENCY.collect()[0].samples[0].value
    sensor_data['power_factor'] = P1_POWER_FACTOR.collect()[0].samples[0].value
    sensor_data['alarm'] = P1_ALARM.collect()[0].samples[0].value

    return sensor_data

def str_to_bool(value):
    if value.lower() in {'false', 'f', '0', 'no', 'n'}:
        return False
    elif value.lower() in {'true', 't', '1', 'yes', 'y'}:
        return True
    raise ValueError('{} is not a valid boolean value'.format(value))


def main() -> None:

    while True:
        p1_reading = pzem_1.read()
        timestamp = datetime.utcfromtimestamp(p1_reading["timestamp"])

        #logging.info(f"{reading}")

        # Limitation on InfluxDB to handle boolean type
        alarm_status = 1 if reading["alarm_status"] else 0

        #printp1_reading)
        #print ("Current",p1_reading["current"])
        time.sleep(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--bind", metavar='ADDRESS', default='0.0.0.0', help="Specify alternate bind address [default: 0.0.0.0]")
    parser.add_argument("-p", "--port", metavar='PORT', default=8016, type=int, help="Specify alternate port [default: 8016]")
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
        time.sleep (2)
