from pixel_network.auth import get_jwt_token
from pixel_network.subscription import listen__device_property_changes
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access environment variables
graphql_url = os.getenv('GRAPHQL_URL')
user_login = os.getenv('USER_LOGIN')
user_password = os.getenv('USER_PASSWORD')
websocket_url = os.getenv('WEBSOCKET_URL')

# get JWT Token
jwt_token = get_jwt_token(user_login, user_password, graphql_url)

print("Login success:", jwt_token)

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
    async for data in listen__device_property_changes(jwt_token, websocket_url, query):
        print(data)

asyncio.run(main())