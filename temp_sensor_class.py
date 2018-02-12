from __future__ import print_function

import os
import time

SENSOR_LOCATION = '/sys/bus/w1/devices/'
DEVICE_PREFIX = '28-*'

# load hw modules/drivers for the temperature sensor to work
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')


class TemperatureSensor():
    """ Temperature sensor class """

    def __init__(self):
        finder = os.popen('ls {location} | grep {prefix}'.format(
            location=SENSOR_LOCATION, prefix=DEVICE_PREFIX))

        devices = finder.read()
        devices = devices.strip('\n')
        devices = devices.split('\n')

        # first matching device
        self.driver = SENSOR_LOCATION + devices[0]
        self.sensor = '/'.join([self.driver, 'w1_slave'])

        self._current_temp = 0

    def read_sensor(self):
        with open(self.sensor, 'r') as fd:
            return fd.readlines()

    def update(self):
        """
            Temperature sensor output format: 2 rows of bytes(9 bytes). 8 bytes payload + 1 byte checksum
            see DS18B20 for what each byte means. For our puprose we call them bytes b0-8

            b0 b1 b2 b3 b4 b5 b6 b7 b8: crc = 4d YES
            b0 b1 b2 b3 b4 b5 b6 b7 b8 t = temp_c

            where temp_c is actual temperature reading in degree celicious * 1000
            YES on the first row indicates a positive reading
        """

        output = self.read_sensor()

        while output[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            output = self.read_sensor()

        temp_index = output[1].find('t=')

        # when we have a good match as per expected format
        if temp_index != -1:
            temp_string = output[1].strip()[temp_index+2:]
            self._current_temp = float(temp_string) / 1000.0

    def read_temp(self):
        self.update()
        return self._current_temp

    def read_celcius(self):
        return self.read_temp()

    def read_farhneit(self):
        return self.read_temp() * 9.0 / 5.0 + 32


def main():
    sensor = TemperatureSensor()

    while True:
        print('Current Temperature in Celcius: ', sensor.read_celcius())
        print('Current Temperature in Farhneit: ', sensor.read_farhneit())
        time.sleep(1)


if __name__ == '__main__':
    main()
