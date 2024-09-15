from pixel_network.subscription import listen_device_property_changes
from thingsboard.mqtt_broker import send_to_thingsboard
import asyncio
import argparse

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


async def main():
    async for data in listen_device_property_changes(query):
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
