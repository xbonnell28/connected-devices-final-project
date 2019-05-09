#!/usr/bin/env python

import kivy
import json
import pigpio
import shelve
import colorsys

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
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

    def get_fire_staff_price(self):
        shop_data = shelve.open('databases/shop.db')
        try:
            fire_staff_price = shop_data['Fire Staff']
        finally:
            shop_data.close()
        return '{} gold'.format(fire_staff_price)

    def get_steel_armor_price(self):
        shop_data = shelve.open('databases/shop.db')
        try:
            steel_armor_price = shop_data['Steel Armor']
        finally:
            shop_data.close()
        return '{} gold'.format(steel_armor_price)

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

            gold = gold - great_sword_price
            attack = attack + 5

            App.get_running_app().root.ids.ShopScreen.gold = gold

            character_data['gold'] = str(gold)
            character_data['attack'] = str(attack)
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


class TestApp(App):

    def build(self):
        self.mqtt = Client()
        self.mqtt.connect("localhost", 1883)
        msg = {'beacon_id': 'b827ebc460ad', 'name': 'Christian'}
        self.mqtt.publish("beacon/available", json.dumps(msg))
        return sm
    
    def search(self):
        self.mqtt.message_callback_add("devices/+/beacon/available", self.receive_search_results)
        self.mqtt.subscribe("beacon/available/+")

    def receive_search_results(self, client, userdata, message):
        msg = json.loads(message.payload)

if __name__ == '__main__':
    TestApp().run()
