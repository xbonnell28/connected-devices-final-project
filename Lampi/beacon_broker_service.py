#!/usr/bin/env python
import json

from lamp_common import *
from paho.mqtt.client import Client

class BrokerService(object):

	def __init__(self):
		self._client = self.create_and_configure_broker_client()

	def serve(self):
		self._client.connect('localhost', port=50001)
        	self._client.loop_forever()

	def create_and_configure_broker_client(self):
		client = Client()
        	client.on_connect = self.on_connect
        	client.message_callback_add("devices/+/beacon/available",
                                    self.on_message_start_battle)
		client.on_massage = self.default_on_message
        	return client

	def on_connect(self, client, userdata, rc, unknown):
		self._client.subscribe("devices/+/beacon/available", qos=1)


	def default_on_message(self, client, userdata, msg):
	        print("Received unexpected message on topic " +
        	      msg.topic + " with payload '" + str(msg.payload) + "'")

	def on_message_start_battle(self, client, userdata, msg):
		print("we got a message")
		print(msg.topic)
		device_id = msg.topic.split('/')[1]
		msg = {'battle': 'this is a test'}
		self._client.publish("devices/{}/beacon/battle".format(device_id), json.dumps(msg), qos=1)


if __name__ == '__main__':
	beacon = BrokerService().serve()




