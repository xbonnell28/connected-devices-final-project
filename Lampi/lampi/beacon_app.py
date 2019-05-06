#!/usr/bin/env python
import kivy
import json
import pigpio
import shelve
import colorsys

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from paho.mqtt.client import Client

Builder.load_file("beacon.kv")

class HomeScreen(Screen):
    pass

class CharacterScreen(Screen):
    pass

class ShopScreen(Screen):
    pass

class SearchScreen(Screen):
    pass

sm = ScreenManager()
sm.add_widget(HomeScreen(name="home"))
sm.add_widget(CharacterScreen(name="character"))
sm.add_widget(ShopScreen(name="shop"))
sm.add_widget(SearchScreen(name="search"))

class TestApp(App):

    def build(self):
        self.mqtt = Client()
        self.mqtt.connect("localhost", 1883)
        return sm
    
    def go_to_character_screen(self):
        msg = {'battle' : True}
        self.mqtt.publish("lamp/changed", json.dumps(msg), qos=1)

if __name__ == '__main__':
    TestApp().run()
