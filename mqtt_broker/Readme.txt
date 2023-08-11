Install and settings mosqitto broker

sudo apt update
sudo add-apt-repository ppa:mosquitto-dev/mosquitto-ppa
sudo apt install mosquitto mosquitto-clients
sudo systemctl start mosquitto
sudo systemctl enable mosquitto
sudo apt update
sudo apt install apache2
sudo ufw allow 1883
sudo ufw allow 9001

sudo vi /etc/mosquitto/mosquitto.conf
#---------------------------------------------------------------
persistence true
allow_anonymous true
persistence_location /var/lib/mosquitto/
log_dest file /var/log/mosquitto/mosquitto.log
include_dir /etc/mosquitto/conf.d
listener 1883
protocol mqtt
listener 9001
protocol websockets
max_keepalive 1000
#---------------------------------------------------------------

sudo cat /var/log/mosquitto/mosquitto.log
mosquitto_pub -h localhost -t "test" -m "Hello"
mosquitto_sub -h localhost -t "test"

If use java and Html.
cd /var/www/html # in this folder need paste data from mqtt_server_data. After, restart apache2.
sudo systemctl restart apache2

If use python and Flask.
sudo apt install python3-pip
pip install Flask paho-mqtt

Copy project dir mqtt_web_app_python_flaks.  
cd /mqtt_web_app_python_flaks # Move to project folder.
python3 app.py # Start server, page available on http://youIp:5000
