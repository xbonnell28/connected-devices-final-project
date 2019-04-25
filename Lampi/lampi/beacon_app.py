#!/usr/bin/env python
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

Builder.load_string("""
<HomeScreen>:
    BoxLayout:
        orientation: 'vertical'
        Button:
            text: 'Character'
            on_press: root.manager.current = 'character'
        Button:
            text: 'Shop'
            on_press: root.manager.current = 'shop'
        Button:
            text: 'Search'
            on_press: root.manager.current = 'search'

<CharacterScreen>:
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'Bilbo Baggins'
        Label:
            text: 'Attack: 10'
        Label:
            text: 'HP: 100'
        Button:
            text: 'Home'
            on_press: root.manager.current = 'home'

<ShopScreen>:
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'Weapon Shop'
        BoxLayout:
            BoxLayout:
                orientation: 'vertical'
                Label:
                    text: 'Greatsword'
                Label:
                    text: '100 gold'
            Button:
                text: 'Buy'
        BoxLayout:
            BoxLayout:
                orientation: 'vertical'
                Label:
                    text: 'Fire Staff'
                Label:
                    text: '50 gold'
            Button:
                text: 'Buy'
        BoxLayout:
            BoxLayout:
                orientation: 'vertical'
                Label:
                    text: 'Steel Armor'
                Label:
                    text: '200 gold'
            Button:
                text: 'Buy'
        Button:
            text: 'Home'
            on_press: root.manager.current = 'home'


<SearchScreen>:
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'Nearby Beacons'
        BoxLayout:
            Label:
                text: 'Davids Beacon'
            Button:
                text: 'Battle!'
        BoxLayout:
            Label:
                text: 'Christians Beacon'
            Button:
                text: 'Battle!'
        Button:
            text: 'Home'
            on_press: root.manager.current = 'home'

""")

class HomeScreen(Screen):
    pass

class CharacterScreen(Screen):
    pass

class ShopScreen(Screen):
    pass

class SearchScreen(Screen):
    pass

sm = ScreenManager()
sm.add_widget(HomeScreen(name='home'))
sm.add_widget(CharacterScreen(name='character'))
sm.add_widget(ShopScreen(name='shop'))
sm.add_widget(SearchScreen(name='search'))

class TestApp(App):

    def build(self):
        return sm

if __name__ == '__main__':
    TestApp().run()
