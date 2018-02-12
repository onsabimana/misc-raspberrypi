import os
import time

SENSOR_LOCATION = '/sys/bus/w1/devices/'
DEVICE_PREFIX  = '28-*'

# load hw modules/drivers for the temperature sensor to work
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

# Find the driver
def find_driver():
    finder = os.popen('ls {location} | grep {prefix}'.format(location=SENSOR_LOCATION, prefix=DEVICE_PREFIX))

    devices = finder.read()
    devices = devices.strip('\n')
    devices = devices.split('\n')

    # first matching device
    return SENSOR_LOCATION + devices[0]


driver = find_driver()
reader = '/'.join([driver, 'w1_slave'])


def temp_raw():
    with open(reader, 'r') as f:
        lines = f.readlines()

    return lines

#  TODO: leave this function blank for students to code the formula
def convert_to_farhneit(temp_c):
    return temp_c * 9.0 / 5.0 + 32.0


def read_temp():
    """
        Temperature sensor output format: 2 rows of bytes ( 9 bytes). 8 bytes payload + 1 byte checksum
        see DS18B20 for what each byte means. For our puprose we call them bytes b0-8

        b0 b1 b2 b3 b4 b5 b6 b7 b8 : crc=4d YES
        b0 b1 b2 b3 b4 b5 b6 b7 b8 t=temp_c

        where temp_c is actual temperature reading in degree celicious * 1000
        YES on the first row indicates a positive reading

    """
    rows = temp_raw()

    while rows[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        rows = temp_raw()

    start_index_temp_output = rows[1].find('t=')

    # when we have a good match as per expected format
    if start_index_temp_output != -1:
        temp_string = rows[1].strip()[start_index_temp_output+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c, convert_to_farhneit(temp_c)


def main():
    while True:
        print read_temp()
        time.sleep(1)


if __name__ == '__main__':
    main()
