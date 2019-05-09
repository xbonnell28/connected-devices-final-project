#!/usr/bin/env python

import kivy
import json
import pigpio
import shelve
import colorsys
import atexit

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from paho.mqtt.client import Client

Builder.load_file("beacon.kv")

class HomeScreen(Screen):
    pass

class CharacterScreen(Screen):

    def get_character_attack(self):
        character_data = shelve.open('databases/character.db')
        try:
            attack = character_data['attack']
        finally:
            character_data.close()
        return "Attack:{}".format(attack)

    def get_character_health(self):
        character_data = shelve.open('databases/character.db')
        try:
            health = character_data['health']
        finally:
            character_data.close()
        return "Health:{}".format(health)

class ShopScreen(Screen):
    pass

class SearchScreen(Screen):
    pass

class WaitForResponseScreen(Screen):
    pass

class RespondToBattleRequestScreen(Screen):
    pass

class BattleScreen(Screen):
    pass

sm = ScreenManager()
sm.add_widget(HomeScreen(name="home"))
sm.add_widget(CharacterScreen(name="character"))
sm.add_widget(ShopScreen(name="shop"))
sm.add_widget(SearchScreen(name="search"))
sm.add_widget(WaitForResponseScreen(name="wait"))
sm.add_widget(RespondToBattleRequestScreen(name="respond"))
sm.add_widget(BattleScreen(name="battle"))


class BeaconApp(App):
    def on_start(self):
        self.mqtt = Client()
        self.mqtt.message_callback_add("beacon/request",
            self.asked_to_battle)
        self.mqtt.connect("localhost", 1883)
        self.mqtt.subscribe("beacon/request", qos=1)
        self.mqtt.loop_start()

    def build(self):
        return sm

    def request_battle(self, opponentDeviceID):
        msg = {'OpponentID': opponentDeviceID}
        self.mqtt.publish("beacon/request", json.dumps(msg))
        self.mqtt.message_callback_add("beacon/response", self.handle_response)
        self.mqtt.subscribe("beacon/response")
        sm.current = "wait"

    def asked_to_battle(self, client, userdata, message):
        self.opponent_id = json.loads(message.payload)['OpponentID']
        sm.current = "respond"

    def handle_response(self, client, userdata, message):
        accepted = json.loads(message.payload)['Accepted']
        if accepted is True:
            sm.current = "battle"
        else:
            sm.current = "home"

    def get_opponent_id(self):
        return self.opponent_id

    def respond_to_challenge(self, opponentDeviceID, accepted):
        if accepted is True:
            msg = {'OpponentID': opponentDeviceID, 'Accepted': True}
            self.mqtt.publish("beacon/response", json.dumps(msg))
            sm.current = "battle"
        else:
            msg = {'OpponentID': opponentDeviceID, 'Accepted': False}
            self.mqtt.publish("beacon/response", json.dumps(msg))
            sm.current = "home"

if __name__ == '__main__':
    BeaconApp().run()
