# Testing code for pixel-network gateway to thingsboard

## Install

    pipenv install

## Start

    pipenv shell
    python subscription_test.py

## Features ToDo

- [done] Login to pixel-network system to get the JWT token
- [done] Use the GraphQL subscription to get the devices data pixel-network
- [done] Convert received data to MQTT and send to thingsboard
- when connection error, push notification to admin use pushbullet
- Handle Bulk Provisioning
- [done] Handle multiple devices subscriptions
- Save all actions to log
- [done] When cennection is lost:
  - 1. try to reconnect
  - 2. push notification to admin use pushbullet
- Handle Bulk Provisioning
  - 1. lookups devices list
  - 2. import new devices to thingsboard
  - 3. add devices to GraphQL subscriptions

