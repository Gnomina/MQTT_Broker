window.onload = function() {
    const client = new Paho.MQTT.Client("3.67.91.220", 9001, "clientId");

    client.onConnectionLost = onConnectionLost;
    client.onMessageArrived = onMessageArrived;

    client.connect({
        onSuccess: onConnect,
        onFailure: function(error) {
            console.log("Connection failed:", error.errorMessage);
        }
    });

    function onConnect() {
      console.log("Connected");
      client.subscribe("Test");
    }

    function onConnectionLost(responseObject) {
      if (responseObject.errorCode !== 0) {
        console.log("onConnectionLost:" + responseObject.errorMessage);
      }
    }

    function onMessageArrived(message) {
        console.log("onMessageArrived:" + message.payloadString);
        document.getElementById("temperatureData").innerText = message.payloadString;
    }
};

