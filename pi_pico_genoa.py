from sbus_receiver_orig import SBUSReceiver
import uasyncio as asyncio
from machine import PWM, Pin


def map_value(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


def update_rx_data(timRx):
    global update_rx
    update_rx = True


class ServoController:
    def __init__(self, servo_pin, min_pulse, max_pulse, max_change_per_loop, freq=50):
        self.servo_pin = servo_pin
        self.pwm = PWM(Pin(servo_pin))
        self.pwm.freq(freq)

        self.min_pulse = min_pulse
        self.max_pulse = max_pulse
        self.max_change_per_loop = max_change_per_loop

        self.current_position = 0
        self.target_position = 0

    def set_target_position(self, target_position):
        self.target_position = target_position

    async def update_servo_position(self):
        while True:
            # Calculate the intermediate position
            if abs(self.target_position - self.current_position) > self.max_change_per_loop:
                step = self.max_change_per_loop if self.target_position > self.current_position else -self.max_change_per_loop
                self.current_position += step
            else:
                self.current_position = self.target_position

            # Map the intermediate position to PWM duty cycle
            pulse = map_value(self.current_position, 172, 1810, self.min_pulse, self.max_pulse)
            self.pwm.duty_ns(pulse)

            await asyncio.sleep_ms(5)  # Adjust the sleep time based on servo control rate


async def process_sbus_data():
    global update_rx, genoaDrumNos, genoaDrumStern, controlGenoaDrumStern, genoaControl, controlGenoaDrumNos, controlDrumStern, \
        controlGenoaControl, controlMode, genoaControl_M

    def map_genoa_control(genoaDrumStern, genoaControl):
        if genoaDrumStern == 172:
            genoaControl_min = 0
            genoaControl_max = 200
        elif genoaDrumStern == 1810:
            genoaControl_min = 0
            genoaControl_max = -200
        else:
            genoaControl_min = 0
            genoaControl_max = 0
        return ((genoaControl - 172) * (genoaControl_max - genoaControl_min) / (1810 - 172)) + genoaControl_min

    while True:
        if update_rx:
            sbus.get_new_data()
            update_rx = False

            genoaDrumStern = sbus.get_rx_channel(4)
            genoaControl = sbus.get_rx_channel(6)
            genoaDrumNos = sbus.get_rx_channel(7)

            if genoaDrumNos == 172:
                controlMode = "Mode_1"
                controlGenoaDrumStern = 992
            elif genoaDrumNos == 1810:
                controlMode = "Mode_2"
                genoaControl_M = map_genoa_control(genoaDrumStern, genoaControl)
                controlGenoaDrumStern = genoaDrumStern + genoaControl_M

            servo1.set_target_position(genoaDrumNos)
            servo2.set_target_position(controlGenoaDrumStern)

        await asyncio.sleep_ms(2)



async def print_sbus_data():
    global genoaDrumNos, genoaDrumStern
    while True:
        
        await asyncio.sleep_ms(200)


sbus = SBUSReceiver(0)
update_rx = False
# Initialize variables to store servo control values
genoaDrumNos = 0  # declaration and initialization variable
genoaDrumStern = 0  # declaration and initialization variable
genoaControl = 0
genoaControl_M = 0
# -------------------------------------------
controlGenoaDrumNos = 0
controlGenoaDrumStern = 0
controlGenoaControl = 0
controlMode = ""
# ------------------------------------------

timRx = machine.Timer()
timRx.init(freq=2778, callback=update_rx_data)

# Create servo instances and set their properties
servo1 = ServoController(servo_pin=14, min_pulse=1300000, max_pulse=1700000, max_change_per_loop=100, freq=330) #genoaDrumNos
servo2 = ServoController(servo_pin=13, min_pulse=1100000, max_pulse=1900000, max_change_per_loop=100, freq=330) #genoaDrumStern

loop = asyncio.get_event_loop()
loop.create_task(process_sbus_data())

# Create tasks for each servo instance
loop.create_task(servo1.update_servo_position())
loop.create_task(servo2.update_servo_position())

loop.create_task(print_sbus_data())
loop.run_forever()







