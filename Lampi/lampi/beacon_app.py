#!/usr/bin/env python
import kivy
import json
import pigpio
import paho.mqtt.client as mqtt
import shelve
import colorsys

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty

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
        return sm

if __name__ == '__main__':
    TestApp().run()
