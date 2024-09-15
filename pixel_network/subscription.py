import websockets
import json
import asyncio
from pixel_network.auth import get_jwt_token
import os
from dotenv import load_dotenv
from pushbullet.notification import send_push_notification

# Load environment variables from .env file
load_dotenv()

graphql_url = os.getenv('GRAPHQL_URL')
websocket_url = os.getenv('WEBSOCKET_URL')
user_login = os.getenv('USER_LOGIN')
user_password = os.getenv('USER_PASSWORD')

async def listen_device_property_changes(subscription_query):
    max_retries = 5
    retry_delay = 30
    retries = 0

    while retries < max_retries:
        try:
            # Fetch a new JWT token
            jwt_token = get_jwt_token(user_login, user_password, graphql_url)
            if not jwt_token:
                raise Exception("Failed to obtain JWT token")

            headers = {"Authorization": f"Bearer {jwt_token}"}

            async with websockets.connect(
                websocket_url,
                subprotocols=["graphql-ws"],
                extra_headers=headers
            ) as websocket:

                # Send connection init message
                await websocket.send(json.dumps({
                    "type": "connection_init",
                    "payload": {}
                }))

                # Await ack from server
                response = await websocket.recv()
                print("Connection init response:", response)

                # Send subscription start message
                await websocket.send(json.dumps({
                    "type": "start",
                    "id": "1",
                    "payload": {
                        "query": subscription_query
                    }
                }))

                while True:
                    try:
                        message = await websocket.recv()
                        data = json.loads(message)
                        if data.get('type') == 'ka':  # skip "keep-alive" messages
                            print(".", end="", flush=True)
                            continue
                        print()
                        yield data
                    except Exception as e:
                        print(f"Error receiving message: {e}")
                        break

        except Exception as e:
            print(f"Connection error: {e}")
            retries += 1
            print(f"Retrying in {retry_delay} seconds... (Attempt {retries}/{max_retries})")
            await asyncio.sleep(retry_delay)
        else:
            print("Reconnect successfully.")
            retries = 0  # Reset retries if the connection was successful

    print("Max retries reached. Exiting...")
    send_push_notification("pixel-network connection alert", f"Failed to connect to pixel-network. Maximum of {max_retries} retries reached. Abandoning attempt.")
