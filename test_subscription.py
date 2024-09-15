from pixel_network.subscription import listen_device_property_changes
import asyncio
import os
from dotenv import load_dotenv
import paho.mqtt.client as mqtt
import json
import argparse

# Load environment variables from .env file
load_dotenv()

# Access environment variables
websocket_url = os.getenv('WEBSOCKET_URL')

query = """
    subscription {
        Objects(filterA: {
            type: "device"
            schemaId: "008e2f3a-19d4-4869-9811-4bd079844578"
            propertyChanged: [{groupName: "Measurements", property: "TEMPERATURE"}]
        }) {
            event
            relatedNode {
                ... on ObjectProperty {
                    object {
                        id
                        temperature: property(propertyName: "Measurements/TEMPERATURE")
                        humidity: property(propertyName: "Measurements/HUMIDITY")
                    }
                }
            }
        }
    }
    """

# send data to thingsboard usign MQTT
def send_to_thingsboard(pixelnetwork_data):

    # MQTT settings
    mqtt_host = os.getenv('MQTT_HOST')
    mqtt_port = 1883
    mqtt_topic = 'v1/devices/me/telemetry'
    mqtt_access_token = os.getenv('MQTT_ACCESS_TOKEN')

    # Extract the relevant data
    device_data = pixelnetwork_data.get('payload', {}).get('data', {}).get('Objects', {}).get('relatedNode', {}).get('object', {})
    device_id = device_data.pop('id', None)
    
    # Create the message payload
    message = json.dumps(device_data)
    
    # Create an MQTT client instance
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    
    # Set the username for the MQTT broker
    client.username_pw_set(mqtt_access_token)
        
    try:
        # Connect to the MQTT broker
        client.connect(mqtt_host, mqtt_port, 60)
        
        # Start the loop
        client.loop_start()
        
        # Publish the message
        result = client.publish(mqtt_topic, message, qos=1)
        
        # Wait for the publish to complete
        result.wait_for_publish()
        
        # Stop the loop
        client.loop_stop()
        
        # Disconnect from the broker
        client.disconnect()
        
        print(f"Message sent to {mqtt_host}/{mqtt_access_token}: {message}")  

    except Exception as e:
        print(f"An error occurred: {e}")

async def main():
    async for data in listen_device_property_changes(websocket_url, query):
        # print(data)
        send_to_thingsboard(data)

def parse_args():
    parser = argparse.ArgumentParser(description='Run the subscription script.')
    parser.add_argument('--debug', action='store_true', help='Run in debug mode')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    if args.debug:
        sample_data = {'type': 'data', 'id': '1', 'payload': {'data': {'Objects': {'event': 'update', 'relatedNode': {'groupName': 'Measurements', 'property': 'TEMPERATURE', 'value': 27.3, 'updatedAt': '2024-09-14T21:49:37.102194+08:00', 'object': {'id': '38b67ce9-c052-41e6-b1d3-8ded52e7bbad', 'temperature': 27.3, 'humidity': 36}}}}}}
        send_to_thingsboard(sample_data)
    else:
        asyncio.run(main())
