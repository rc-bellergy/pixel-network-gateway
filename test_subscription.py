from pixel_network.subscription import listen_device_property_changes
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access environment variables
websocket_url = os.getenv('WEBSOCKET_URL')

query = """
    subscription {
        Objects(filterA: {
            type: "device"
            schemaId: "b96f601a-3895-47b3-ae2a-377240fd4a98"
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
                    }
                }
            }
        }
    }
    """

async def main():
    async for data in listen_device_property_changes(websocket_url, query):
        print(data)

asyncio.run(main())
