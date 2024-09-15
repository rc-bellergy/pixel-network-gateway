import os
import paho.mqtt.client as mqtt
import json
from dotenv import load_dotenv


# send pixel-network data to thingsboard usign MQTT
def send_to_thingsboard(pixelnetwork_data):

    # MQTT settings
    mqtt_host = os.getenv('MQTT_HOST')
    mqtt_port = 1883
    mqtt_topic = 'v1/devices/me/telemetry'

    # Load access tokens from access_tokens.json
    with open('access_tokens.json', 'r') as f:
        access_tokens = json.load(f)

    # Extract the relevant data
    device_data = pixelnetwork_data.get('payload', {}).get('data', {}).get('Objects', {}).get('relatedNode', {}).get('object', {})
    
    # Create an MQTT client instance
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    access_token = access_tokens[device_data.get('id')]
    client.username_pw_set(access_token)

    # Create the message payload
    message = json.dumps(device_data)

    # print('access_token: ', access_token)
    # print('message: ', message)
        
    try:
        # Connect to the MQTT broker
        connect = client.connect(mqtt_host, mqtt_port, 60)
        if connect != mqtt.MQTT_ERR_SUCCESS:
            print(f"Failed to connect to MQTT broker. Error code: {result}")
            return
        client.loop_start()
        
        # Publish the message
        result = client.publish(mqtt_topic, message, qos=1)
        result.wait_for_publish()
        client.loop_stop()
        client.disconnect()
        
        print(f"Message sent to {mqtt_host}/{access_token}: {message}")  

    except Exception as e:
        print(f"An error occurred: {e}")


