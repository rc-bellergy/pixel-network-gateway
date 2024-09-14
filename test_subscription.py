from pixel_network.subscription import listen_device_property_changes
import asyncio
import os
from dotenv import load_dotenv
import paho.mqtt.client as mqtt

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
                    groupName
                    property
                    value
                    updatedAt
                    object {
                        id
                        name
                        temperature: property(propertyName: "Measurements/TEMPERATURE")
                        humidity: property(propertyName: "Measurements/HUMIDITY")

                    }
                }
            }
        }
    }
    """

# Sample data:
# {'type': 'data', 'id': '1', 'payload': {'data': {'Objects': {'event': 'update', 'relatedNode': {'groupName': 'Measurements', 'property': 'TEMPERATURE', 'value': 27.3, 'updatedAt': '2024-09-14T21:49:37.102194+08:00', 'object': {'id': '38b67ce9-c052-41e6-b1d3-8ded52e7bbad', 'name': 'LoRaWAN Device (24-E1-24-13-6E-24-03-32)_YYS', 'temperature': 27.3, 'humidity': 36}}}}}}

# send data to thingsboard usign MQTT
def send_to_thingsboard(data):

    # MQTT settings
    mqtt_host = os.getenv('MQTT_HOST')
    mqtt_port = os.getenv('MQTT_PORT')
    mqtt_topic = os.getenv('MQTT_TOPIC')
    mqtt_access_token = os.getenv('MQTT_ACCESS_TOKEN')

    # Extract the relevant data
    temperature = data['payload']['data']['Objects']['relatedNode']['temperature']
    humidity = data['payload']['data']['Objects']['relatedNode']['humidity']
    
    # Create the message payload
    message = json.dumps({"temperature": temperature, "humidity": humidity})
    
    # Create an MQTT client instance
    client = mqtt.Client()
    
    # Set the username for the MQTT broker
    client.username_pw_set(mqtt_access_token)
    
    # Connect to the MQTT broker
    client.connect(mqtt_host, mqtt_port, 60)
    
    # Publish the message
    client.publish(mqtt_topic, message, qos=1)
    
    # Disconnect from the MQTT broker
    client.disconnect()

async def main():
    async for data in listen_device_property_changes(websocket_url, query):
        print(data)
        send_to_thingsboard(data)

asyncio.run(main())
