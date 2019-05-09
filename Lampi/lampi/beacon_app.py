#!/usr/bin/env python

import kivy
import json
import pigpio
import shelve
import colorsys
import atexit

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty, NumericProperty
from kivy.clock import Clock
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

    character_gold = StringProperty()
    
    def on_enter(self):
        Clock.schedule_once(self.set_gold)

    def set_gold(self, dt):
        character_data = shelve.open('databases/character.db')
        try:
            character_gold = character_data['gold']
        finally:
            character_data.close()

    def get_fire_staff_price(self):
        shop_data = shelve.open('databases/shop.db')
        try:
            fire_staff_price = shop_data['Fire Staff']
        finally:
            shop_data.close()
        return '{} gold'.format(fire_staff_price)

    def buy_fire_staff(self):
        shop_data = shelve.open('databases/shop.db')
        character_data = shelve.open('databases/character.db')
        try:
            gold = int(character_data['gold'])
            attack = int(character_data['attack'])
            fire_staff_price = int(shop_data['Fire Staff'])

            if gold >= fire_staff_price:
                gold = gold - fire_staff_price
                attack = attack + 2

                character_data['gold'] = str(gold)
                character_data['attack'] = str(attack)
            
                self.character_gold = str(gold) 
        finally:
            character_data.close()
            shop_data.close()

    def get_steel_armor_price(self):
        shop_data = shelve.open('databases/shop.db')
        try:
            steel_armor_price = shop_data['Steel Armor']
        finally:
            shop_data.close()
        return '{} gold'.format(steel_armor_price)

    def buy_steel_armor(self):
        shop_data = shelve.open('databases/shop.db')
        character_data = shelve.open('databases/character.db')
        try:
            gold = int(character_data['gold'])
            health = int(character_data['health'])
            steel_armor_price = int(shop_data['Steel Armor'])

            if gold >= steel_armor_price:
                gold = gold - steel_armor_price
                health = health + 5

                character_data['gold'] = str(gold)
                character_data['health'] = str(health)
            
                self.character_gold = str(gold) 
        finally:
            character_data.close()
            shop_data.close()

    def get_great_sword_price(self):
        shop_data = shelve.open('databases/shop.db')
        try:
            great_sword_price = shop_data['Greatsword']
        finally:
            shop_data.close()
        return '{} gold'.format(great_sword_price)

    def buy_great_sword(self):

        shop_data = shelve.open('databases/shop.db')
        character_data = shelve.open('databases/character.db')
        try:
            gold = int(character_data['gold'])
            attack = int(character_data['attack'])
            great_sword_price = int(shop_data['Greatsword'])

            if gold >= great_sword_price:
                gold = gold - great_sword_price
                attack = attack + 5

                character_data['gold'] = str(gold)
                character_data['attack'] = str(attack)
            
                self.character_gold = str(gold) 
        finally:
            character_data.close()
            shop_data.close()

    def get_character_gold(self):
        character_data = shelve.open('databases/character.db')
        try:
            gold = character_data['gold']
        finally:
            character_data.close()
        return "Gold:{}".format(gold)

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
        self.mqtt.publish("beacon/send_request", json.dumps(msg))
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
            self.mqtt.publish("beacon/send_response", json.dumps(msg))
            sm.current = "battle"
        else:
            msg = {'OpponentID': opponentDeviceID, 'Accepted': False}
            self.mqtt.publish("beacon/send_response", json.dumps(msg))
            sm.current = "home"

if __name__ == '__main__':
    BeaconApp().run()
