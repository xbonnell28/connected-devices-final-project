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
        	client.message_callback_add("devices/+/beacon/send_request",
                                    self.on_battle_request)
		client.message_callback_add("devices/+/beacon/send_response",
                                    self.on_request_response)
		client.on_message = self.default_on_message
        	return client

	def on_connect(self, client, userdata, rc, unknown):
		self._client.subscribe("devices/+/beacon/send_request", qos=1)
		self._client.subscribe("devices/+/beacon/send_response", qos=1)

	def default_on_message(self, client, userdata, msg):
	        print("Received unexpected message on topic " +
        	      msg.topic + " with payload '" + str(msg.payload) + "'")

	def on_battle_request(self, client, userdata, msg):
		defender_id = json.loads(msg.payload)["DefenderID"]
		aggressor_id = msg.topic.split('/')[1]
		new_msg = {"AggressorID": aggressor_id, "DefenderID": defender_id}
		print(new_msg)
		self._client.publish("devices/{}/beacon/request".format(defender_id), json.dumps(new_msg), qos=1)

	def on_request_response(self, client, userdata, msg):
		aggressor_id = json.loads(msg.payload)["AggressorID"]
		defender_id = msg.topic.split('/')[1]
		new_msg = {"AggressorID": aggressor_id, "DefenderID": defender_id}
                print(new_msg)
                self._client.publish("devices/{}/beacon/response".format(aggressor_id), json.dumps(new_msg), qos=1)


if __name__ == '__main__':
	beacon = BrokerService().serve()




