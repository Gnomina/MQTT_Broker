import machine
import time

uart = machine.UART(1, baudrate=9600, tx=machine.Pin(4), rx=machine.Pin(5))


class SIM800CSocket:
    def __init__(self, uart):
        self.uart = uart
        self.pid = 0
        print("Initializing SIM800CSocket...")

    def send_cmd_wait_for_resp(self, cmd, resp, timeout=2000):
        self.uart.write(cmd.encode())
        print("Sent:", cmd.strip())
        time.sleep(0.5)
        data = self.uart.read(timeout)
        if data:
            print("Received:", data)
        else:
            print("No data received from the module!")
        return data if data and resp.encode() in data else None

    def connect(self, address):
        self.send_cmd_wait_for_resp('AT+CIPCLOSE\r\n', "CLOSE OK\r\n")
        time.sleep(0.3)
        cmd = 'AT+CIPSTART="TCP","{}",{}\r\n'.format(address[0], address[1])
        response = self.send_cmd_wait_for_resp(cmd, "OK\r\n")
        attempts = 10
        while attempts > 0:
            if response is None:
                print("No response from the module. Retrying...")
                time.sleep(1)
                response = self.send_cmd_wait_for_resp(cmd, "OK\r\n")
                attempts -= 1
                continue

            decoded_response = response.decode()

            if "CONNECT OK" in decoded_response:
                return True
            elif "ERROR" in decoded_response:
                if "ALREADY CONNECT" in decoded_response:
                    print("Already connected to the server.")
                    return True

                print("Error:", decoded_response)
            else:
                print("Unexpected response:", decoded_response)

            time.sleep(1)
            response = self.uart.read()
            attempts -= 1

        print("Failed to establish a connection after 10 attempts")
        return False

    def send_raw(self, data):
        print("Sending data:", data)
        cmd = 'AT+CIPSEND={}\r\n'.format(len(data))
        response = self.send_cmd_wait_for_resp(cmd, ">")
        if response:
            self.uart.write(data)
            response = self.send_cmd_wait_for_resp("", "SEND OK\r\n")
            if not response:
                print("Failed to send the data!")
        else:
            print("No data received from the module!")

    def close(self):
        print("Attempting to close connection...")
        cmd = 'AT+CIPCLOSE\r\n'
        response = self.send_cmd_wait_for_resp(cmd, "CLOSE OK\r\n")
        if not response:
            raise Exception("Failed to close the connection")
        print("Connection closed successfully.")

    ############################# MQTT-HEX################################

    @staticmethod
    def encode_remaining_length(remaining_length):
        bytes_list = []
        while True:
            byte = remaining_length % 128
            remaining_length //= 128
            if remaining_length > 0:
                byte |= 0x80
            bytes_list.append(byte)
            if remaining_length == 0:
                break
        return bytes(bytes_list)

    @staticmethod
    def int_to_big_endian(value, width):
        return bytes(value.to_bytes(width, 'big'))

    def mqtt_conn(self, client_id, keep_alive):
        protocol_name = "MQTT"
        protocol_level = bytes([0x04])
        connect_flags = bytes([0x02])

        protocol_name_bytes = protocol_name.encode('ascii')
        protocol_name_len = self.int_to_big_endian(len(protocol_name), 2)
        keep_alive_bytes = self.int_to_big_endian(keep_alive, 2)
        client_id_bytes = client_id.encode('ascii')
        client_id_len = self.int_to_big_endian(len(client_id), 2)

        remaining_length = len(protocol_name_len + protocol_name_bytes + protocol_level +
                               connect_flags + keep_alive_bytes + client_id_len + client_id_bytes)
        remaining_length_bytes = self.encode_remaining_length(remaining_length)

        packet = bytes([0x10]) + remaining_length_bytes + protocol_name_len + protocol_name_bytes + \
            protocol_level + connect_flags + keep_alive_bytes + client_id_len + client_id_bytes

        return packet
    ############################################ END##########################

    #################################### PUBLISH##############################
    def mqtt_publish(self, topic, payload):
        # Fixed header
        packet_type_flags = bytes([0x30])  # Тип пакета PUBLISH + флаги

        # Topic
        topic_bytes = topic.encode('ascii')
        topic_length = self.int_to_big_endian(len(topic_bytes), 2)

        # Payload
        payload_bytes = payload.encode('ascii')

        # Remaining length
        remaining_length = len(topic_length + topic_bytes + payload_bytes)
        remaining_length_bytes = self.encode_remaining_length(remaining_length)

        packet = packet_type_flags + remaining_length_bytes + \
            topic_length + topic_bytes + payload_bytes

        return packet
    ####################################### END##############################


sim800c = SIM800CSocket(uart)
sim800c.connect(('3.78.179.109', 1883))
packet = sim800c.mqtt_conn("Name", 360)
publish_packet = sim800c.mqtt_publish("Topic", "Hello World from GSM")
sim800c.send_raw(packet)
sim800c.send_raw(publish_packet)
time.sleep(1)
sim800c.send_raw(publish_packet)
sim800c.close()
