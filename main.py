import kivy

kivy.require('1.11.1')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.graphics import Color
from kivy.graphics import Triangle
from kivy.graphics import Rectangle
from kivy.graphics import Color
from kivy.graphics import Line
import sqlite3


class InitialWindow(Screen):
    pass

class MainWindow(Screen):
    pass

class SecondWindow(Screen):
    pass

class DonateEquipment(Screen, FloatLayout):
    pass

class ProfileWindow(Screen):
    hname = ObjectProperty()
    location = ObjectProperty()
    language = ObjectProperty()
    contactinfo = ObjectProperty()
    nostaff = ObjectProperty()
    capacity = ObjectProperty()
    status = ObjectProperty()

    def btn(self):
        con = sqlite3.connect('user.db')
        cur = con.cursor()
        cur.execute(
            """ INSERT INTO User (hname, location, language, contactinfo, nostaff, capacity, status) VALUES (?,?,?,?,?,?,?)""",
            (self.hname.text, self.location.text, self.language.text, self.contactinfo.text, self.nostaff.text,
             self.capacity.text, self.status.text)
            )
        con.commit()
        con.close()

class ScanRFIDWindow(Screen, FloatLayout):
    pass

class ViewDonations(Screen):
    pass

class NewDonation(Screen):
    pass

# For transitions between windows
class WindowManager(ScreenManager):
    pass


GUI = Builder.load_file("kv/main.kv")

class MyApp(App):
    try:
        con = sqlite3.connect('user.db')
        cur = con.cursor()
        cur.execute(""" CREATE TABLE User(
        hname text,
        location text,
        language text,
        contactinfo text,
        nostaff text,
        capacity text,
        status text
        )
        """)
        con.commit()
        con.close()

    except:
       pass

    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        return GUI

    def change_screen(self,window_name,direction):
        #get window manager from kv file
        window_manager = self.root.ids['window_manager']
        window_manager.current = window_name
        window_manager.transition.direction = direction

if __name__ == "__main__":
    MyApp().run()