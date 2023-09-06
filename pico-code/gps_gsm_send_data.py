import machine
import time
import ubinascii
from umqtt.simple import MQTTClient
from micropyGPS import MicropyGPS
from machine import Pin

# Настройки MQTT
MQTT_SERVER = "3.77.57.101"
MQTT_PORT = 1883
MQTT_TOPIC = "Test"

# Настройка UART для связи с GSM модулем
uart1 = machine.UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))
uart0 = machine.UART(0, baudrate=9600, bits=8, parity=None,
                     stop=1, timeout=5000, rxbuf=1024)

# Filter Class


class KalmanFilter:
    def __init__(self, process_variance, measurement_variance, initial_value=0, initial_estimate_error=1):
        # Исходные значения
        self.estimate = initial_value  # Оценка
        self.estimate_error = initial_estimate_error  # Ошибка оценки
        # Дисперсия процесса (как быстро наше истинное значение изменяется во времени)
        self.process_variance = process_variance
        # Дисперсия измерения (как точны наши измерения)
        self.measurement_variance = measurement_variance

    def update(self, measurement):
        # Прогноз
        prediction = self.estimate
        prediction_error = self.estimate_error + self.process_variance

        # Коррекция
        kalman_gain = prediction_error / \
            (prediction_error + self.measurement_variance)
        self.estimate = prediction + kalman_gain * (measurement - prediction)
        self.estimate_error = (1 - kalman_gain) * prediction_error

        return self.estimate


def send_at_command(cmd, timeout=2000):
    print("Sending:", cmd)
    uart1.write(cmd + "\r\n")
    time.sleep_ms(timeout)
    response = uart1.read().decode()
    print(response)
    return response


def setup_gprs():
    # Здесь ваши команды для настройки и активации GPRS соединения
    send_at_command("AT")


def connect_mqtt():
    client_id = ubinascii.hexlify(machine.unique_id())
    client = MQTTClient(client_id="pico_client", server=MQTT_SERVER, port=1883,
                        user=None, password=None, keepalive=60, ssl=False, ssl_params={})
    client.connect()
    return client


def main():
    setup_gprs()
    mqtt_client = connect_mqtt()

    gps = MicropyGPS()
    kf = KalmanFilter(process_variance=2, measurement_variance=3)

    while True:
        buf = uart0.readline()
        # Update the gps instance with buf data if required
        for char in buf:
            gps.update(chr(char))

        speed_measurement = gps.speed[2]
        estimate = kf.update(speed_measurement)

        latitude = gps.latitude
        longitude = gps.longitude

        latitude_degrees = latitude[0]
        latitude_minutes = latitude[1]
        latitude_direction = latitude[2]

        longitude_degrees = longitude[0]
        longitude_minutes = longitude[1]
        longitude_direction = longitude[2]

        decimal_latitude = latitude_degrees + latitude_minutes / 60
        if latitude_direction == 'S':
            decimal_latitude *= -1

        decimal_longitude = longitude_degrees + longitude_minutes / 60
        if longitude_direction == 'W':
            decimal_longitude *= -1

        estimate_round = round(estimate, 2)
        # out_message = f"Speed km/h: {estimate:.2f}, Lat: {decimal_latitude:.5f}, Lon: {decimal_longitude:.5f}"
        out_message = f"Speed km/h: {estimate:.2f}, {decimal_latitude:.5f} {decimal_longitude:.5f}"
        print(
            f"Measurement: {speed_measurement:.2f}, Estimate: {estimate:.2f}")
        print(out_message)

        try:
            mqtt_client.publish(MQTT_TOPIC, str(out_message))
            print("Send")
        except Exception as e:
            print("Error sending to MQTT:", e)
            # Maybe reconnect to MQTT here

        time.sleep(5)


main()
