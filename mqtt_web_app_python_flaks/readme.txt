sudo apt install python3-pip
sudo pip install Flask paho-mqtt

mosqitto server test
mosquitto_sub -h localhost -t "Test"             #subscribe on a topik
mosquitto_pub -h localhost -t "test" -m "Hello"  # post topik

sudo cat /var/log/mosquitto/mosquitto.log

install mosqitto
sudo apt update
sudo add-apt-repository ppa:mosquitto-dev/mosquitto-ppa
sudo apt install mosquitto mosquitto-clients
sudo ufw allow 1883 #add port to firewall
sudo ufw allow 9001 #add port to firewall
sudo systemctl restart mosquitto
ss  -tuln | grep -E '1883|9001'
sudo wget https://raw.githubusercontent.com/eclipse/paho.mqtt.javascript/master/src/paho-mqtt.js # on use java, need to place on /var/www/html and index.html  paho-mqtt.js  script.js

#---------------------------------------------------------------
sudo vi /etc/mosquitto/mosquitto.conf
# Place your local configuration in /etc/mosquitto/conf.d/
#
# A full description of the configuration file is at
# /usr/share/doc/mosquitto/examples/mosquitto.conf.example

persistence true
persistence_location /var/lib/mosquitto/

log_dest file /var/log/mosquitto/mosquitto.log

include_dir /etc/mosquitto/conf.d

listener 1883
allow_anonymous true
protocol mqtt

listener 9001
protocol websockets
allow_anonymous true

max_keepalive 1000
#---------------------------------------------------------------

nohup python3 app.py > app.log 2>&1 & # start server on backgroun
ps aux | grep app.py # grep server PID
kill -9 'PID' # kill server PID
tail -f app.log # in directory app show logs