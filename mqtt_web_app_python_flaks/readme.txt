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
kill -2 'PID' # kill server PID
tail -f app.log # in directory app show logs

#--------------------------------------------------------------------
Create a systemd Unit file for your application:

Open a new file for the service:
sudo nano /etc/systemd/system/app.service

Fill in with the following content:
#-------------------------------------------------------------------
[Unit]
Description=My Python App
After=network.target

[Service]
User=user
WorkingDirectory=/path/to/directory/
ExecStart=/usr/bin/python3 /path/to/directory/app.py
Restart=always
StandardOutput=append:/path/to/log/app-output.log
StandardError=append:/path/to/log/app-error.log

[Install]
WantedBy=multi-user.target
#-------------------------------------------------------------------
Replace /path/to/directories/ with the actual path to your app.py. Also specify the path where you want to save the logs (for example, /var/log/).


sudo touch app-output.log
sudo mv app-output.log /var/log/Python_Flaks_app/

sudo touch app-error.log
sudo mv app-error.log  /var/log/Python_Flaks_app/

sudo chown ubuntu:ubuntu /usr/local/bin/mqtt_app/app.py
sudo chown ubuntu:ubuntu /usr/local/bin/mqtt_app/templates/ -R

Restart systemd for it to apply the new changes:
sudo systemctl daemon-reload

Start you App:
sudo systemctl start app


To check that your application is working:
sudo systemctl status app

Enable autostart of your application at system startup:
sudo systemctl enable app

Now your application will automatically launch when the system starts. Your application logs will be saved to the log files you specify.
#-------------------------------------------------------------------