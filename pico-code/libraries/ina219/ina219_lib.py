# This library is written for the INA219 module.
# The library uses standard micropython features.
# The library implements several functions:
# Obtaining the current battery voltage in V,
# Current in mA, Power in mW, Battery Charge in percentage

# Each function has a duplicate with formatted data output.
# I need this for use both as a printed string and for working with data.
# In order not to clutter the working code with
# additional output formatting, I added these functions.

# Code run example:

# from machine import Pin, I2C
# from ina219_lib import INA219
# import time

# i2c_obj = I2C(1, scl=Pin(3), sda=Pin(2), freq=400000)
# ina219 = INA219(i2c=i2c_obj, Rsh=0.1, addr=64)

# while True:
#    print(ina219.formatted_percentage())
#    print(ina219.formatted_voltage())
#    print(ina219.formatted_current())
#    print(ina219.formatted_power())
#    print("################################")

#    #print(ina219.Power())
#    #print(ina219.Current())
#    #print(ina219.readCorrectedV())
#    #print(ina219.voltage_to_percentage())

#    time.sleep(1)

from machine import Pin, I2C
import ustruct
import time


_REG_SHUNTVOLTAGE = const(0x01)

_REG_BUSVOLTAGE = const(0x02)

_REG_POWER = const(0x03)

_REG_CURRENT = const(0x04)


class INA219(object):
    def __init__(self, i2c=None, scl=None, sda=None, freq=None, Rsh=None, addr=None):

        self.i2c = i2c
        self.Rsh = Rsh
        self.addr = addr

    def readCorrectedV(self):
        current = self.Current()
        self.i2c.writeto(self.addr, '\2')
        data = self.i2c.readfrom(self.addr, 2)
        data = ustruct.unpack('!h', data)[0]

        if current < 10.0:
            return (data >> 3) * 4.0  # mV
        else:
            return (data >> 3) * 4.11  # mV

    def formatted_voltage(self):
        voltage = self.readCorrectedV()/1000
        if voltage is None:
            return "Voltage out of range"
        return f"Batt Volt: {voltage:.2f} V"

    def Current(self):  # This function returns unformatted data "00.0
        self.i2c.writeto(self.addr, bytearray(
            [_REG_SHUNTVOLTAGE]))  # select POWER register
        data = self.i2c.readfrom(self.addr, 2)
        data = ustruct.unpack('!h', data)[0]
        return data*self.Rsh  # 100uV/0.1Ω=1mA

    # This function returns formatted data "Current: 00.0 mA"
    def formatted_current(self):
        current = self.Current()
        if current is None:
            return "Current out of range"
        return f"Current: {current:.1f} mA"

    def Power(self):
        self.i2c.writeto(self.addr, bytearray(
            [_REG_POWER]))
        data = self.i2c.readfrom(self.addr, 2)
        raw_power = ustruct.unpack('!h', data)[0]
        power_lsb = 0.0025
        power_in_watts = raw_power * power_lsb
        return power_in_watts * 1000

    def formatted_power(self):
        power = self.Power()
        if power is None:
            return "Power out of range"
        return f"Power: {power:.1f} mW"

    def voltage_to_percentage(self):
        voltage = self.readCorrectedV() / 1000
        battery_limits = [
            {"max": 4.2, "min": 3.35},  # 1-S batt
            {"max": 8.4, "min": 6.65},  # 2-S batt
            {"max": 12.6, "min": 10.65}  # 3-S batt
        ]

        for limits in battery_limits:
            if limits["min"] <= voltage <= limits["max"]:
                percentage = (
                    (voltage - limits["min"]) / (limits["max"] - limits["min"])) * 100
                return round(percentage, 1)
        return None

    def formatted_percentage(self):
        percentage = self.voltage_to_percentage()
        if percentage is None:
            return "Battery charge: not detected or out of range"
        return f"Battery charge: {percentage:.1f} %"
