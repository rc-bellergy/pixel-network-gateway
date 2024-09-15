from pixel_network.subscription import listen_device_property_changes
from thingsboard.mqtt_broker import send_to_thingsboard
import asyncio
from dotenv import load_dotenv
import os

# access_token = os.getenv('MQTT_ACCESS_TOKEN') 

queries = [
    {
        "query": """
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
    },
    {
        "query": """
            subscription {
                Objects(filterA: {
                    type: "device"
                    schemaId: "593af6ca-42cd-4806-95db-e0fef4fcd0de"
                    propertyChanged: [{groupName: "Measurements", property: "WSTATUS"}]
                }) {
                    event
                    relatedNode {
                        ... on ObjectProperty {
                            object {
                                id
                                leaked: property(propertyName: "Measurements/WSTATUS")
                            }
                        }
                    }
                }
            }
            """
    }
]

async def handle_subscription(query):
    async for data in listen_device_property_changes(query):
        send_to_thingsboard(data)

async def main():
    tasks = [handle_subscription(q["query"]) for q in queries]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())

asyncio.run(main())
