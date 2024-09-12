# Testing code for pixel-network gateway to thingsboard

## Install

    pipenv install

## Start

    pipenv shell
    python subscription_test.py

## Features ToDo

- [done] Login to pixel-network system to get the JWT token
- [done] Use the GraphQL subscription to get the devices data pixel-network
- Convert received data to MQTT and send to thingsboard
- Save all actions to log
- [done] When cennection is lost:
  - 1. try to reconnect
  - 2. push notification to admin use pushbullet
- Handle Bulk Provisioning
  - 1. lookups devices list
  - 2. import new devices to thingsboard
  - 3. add devices to GraphQL subscriptions


## References of schemaId of devices
```json
  {
    "schemaName": "Milesight EM320 TH",
    "schemaId": "b96f601a-3895-47b3-ae2a-377240fd4a98",
  },
  {
    "schemaName": "Milesight EM300 Temperature and Humidity",
    "schemaId": "008e2f3a-19d4-4869-9811-4bd079844578",
  },
  {
    "schemaName": "Milesight EM300 ZLD",
    "schemaId": "593af6ca-42cd-4806-95db-e0fef4fcd0de",
  },
  {
    "schemaName": "Milesight EM500 PT100",
    "schemaId": "a190347c-287f-4aec-a8a2-90fee0a1f957",
  },
  {
    "schemaName": "Milesight EM500-SWL",
    "schemaId": "23e92ee1-9287-4037-862b-ce4c1627df71",
  },
  {
    "schemaName": "SEN20600 DRMT",
    "schemaId": "6b6e92fc-adda-4147-a7d0-7d8464e45cdb",
  },
  {
    "schemaName": "Netvox R718N115",
    "schemaId": "afffc379-33e7-4df2-93e9-8a1ed0070fa6",
  },
  {
    "schemaName": "Milesight WS301",
    "schemaId": "15c2c663-08dc-4732-810f-4f02a1b44de7",
  }
```