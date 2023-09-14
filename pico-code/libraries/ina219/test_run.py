from machine import Pin, I2C
from ina219_lib import INA219
import time

i2c_obj = I2C(1, scl=Pin(3), sda=Pin(2), freq=400000)
ina219 = INA219(i2c=i2c_obj, Rsh=0.1, addr=64)

while True:
    print(ina219.formatted_percentage())
    print(ina219.formatted_voltage())
    print(ina219.formatted_current())
    print(ina219.formatted_power())
    print("################################")

    # print(ina219.Power())
    # print(ina219.Current())
    # print(ina219.readCorrectedV())
    # print(ina219.voltage_to_percentage())

    time.sleep(1)
