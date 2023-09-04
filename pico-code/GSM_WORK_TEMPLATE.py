# This code work only on pi pico W

import machine
import time
import ubinascii
from umqtt.simple import MQTTClient
from machine import Pin

# Настройки MQTT
MQTT_SERVER = "IP"
MQTT_PORT = 1883
MQTT_TOPIC = "Test"

# Настройка UART для связи с GSM модулем
uart = machine.UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))


def send_at_command(cmd, timeout=2000):
    print("Sending:", cmd)
    uart.write(cmd + "\r\n")
    time.sleep_ms(timeout)
    response = uart.read().decode()
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
    while True:
        # Отправить данные на сервер MQTT
        mqtt_client.publish(MQTT_TOPIC, "Hello from GSM")
        print("Send")
        time.sleep(3)


main()
