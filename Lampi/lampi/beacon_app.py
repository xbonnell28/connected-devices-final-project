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
""")

class HomeScreen(Screen):
    pass

class CharacterScreen(Screen):
    pass

sm = ScreenManager()
sm.add_widget(HomeScreen(name='home'))
sm.add_widget(CharacterScreen(name='character'))

class TestApp(App):

    def build(self):
        return sm

if __name__ == '__main__':
    TestApp().run()
