import websockets
import json

async def listen__device_property_changes(jwt_token, url, subscription_query):

    headers = {"Authorization": f"Bearer {jwt_token}"}
    # print("Headers being sent:", headers)  # Debug print to check headers

    async with websockets.connect(
        url,
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
                if data.get('type') == 'ka': # skip "keep-alive" messages
                    continue
                yield data
            except Exception as e:
                print(f"Error: {e}")
                break

