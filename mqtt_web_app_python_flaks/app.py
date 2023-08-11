from flask import Flask, render_template, jsonify
import paho.mqtt.client as mqtt

app = Flask(__name__)
temperature = "Waiting for data..."


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Successfully connected to MQTT broker!")
    else:
        print("Failed to connect to MQTT broker. Return code:", rc)
    client.subscribe("Test")  # Topic to sunscribe


def on_subscribe(client, userdata, mid, granted_qos):
    print("Successfully subscribed to topic 'Test' with QOS:", granted_qos)


def on_message(client, userdata, msg):
    global temperature
    temperature = msg.payload.decode()
    print("Received message:", temperature)


def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected disconnection.")
    else:
        print("Disconnected from MQTT broker.")


client = mqtt.Client()
client.on_connect = on_connect
client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_disconnect = on_disconnect

client.connect("3.67.91.220", 1883, 60)  # broker ip/hostname, port, keepalive

# Если у вас есть аутентификация для MQTT-брокера
# client.username_pw_set("your_username", "your_password")

client.loop_start()


@app.route('/')
def index():
    return render_template('index.html', temperature=temperature)


@app.route('/update_temperature')
def update_temperature():
    print("Sending temperature:", temperature)
    return jsonify(temperature=temperature)


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
