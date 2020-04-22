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
    id_no = ObjectProperty()
    passw = ObjectProperty()

    # Define button behaviour to only let you through if you have correct details
    def btn(self):
        con = sqlite3.connect('user.db')
        cur = con.cursor()
        cur.execute(""" SELECT Username, Password FROM Login WHERE Username=? OR Password=?""", 
        (self.id_no.text, self.passw.text))
        result = cur.fetchone()
        if (result[0] == self.id_no.text and result[1] == self.passw.text):
            self.manager.current = 'split_window'
        con.commit()
        con.close()

class SplitWindow(Screen):
    pass

class MainMenuDonor(Screen):
    pass

class MainMenuRecipient(Screen):
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

class RequestDonation(Screen):

    typemach = ObjectProperty()
    makemodel = ObjectProperty()
    requir = ObjectProperty()
    lang = ObjectProperty()
    powconv = ObjectProperty()
    contact = ObjectProperty()

    def btn(self):
        self.manager.current = 'main_menu_recipient'

class AvailableEquipment(Screen):

    def btn(self):
        self.manager.current = 'main_menu_recipient'


class NewDonation(Screen):


    serial = ObjectProperty()
    makemodel = ObjectProperty()
    manual = ObjectProperty()
    servinfo = ObjectProperty()
    prevmaint = ObjectProperty()
    nextmaint = ObjectProperty()
    disposal = ObjectProperty()
    contact = ObjectProperty()
    
    def upload(self):
        con = sqlite3.connect('user.db')
        cur = con.cursor()
        cur.execute(
            """INSERT INTO Donation (serial, makemodel, manual, servinfo, prevmaint, nextmaint, disposal, contact) VALUES(?,?,?,?,?,?,?,?)""",
            (self.serial.text, self.makemodel.text, self.manual.text, self.servinfo.text, self.prevmaint.text, self.nextmaint.text, self.disposal.text,
            self.contact.text)
        )
        con.commit()
        con.close()
        self.serial.text = ""
        self.makemodel.text = ""
        self.manual.text = ""
        self.servinfo.text = ""
        self.prevmaint.text = ""
        self.nextmaint.text = ""
        self.disposal.text = ""
        self.contact.text = ""

# For transitions between windows
class WindowManager(ScreenManager):
    pass


GUI = Builder.load_file("kv/main.kv")

#Function to populate database with registered hospitals if it is empty
def RegisteredHospitals(filename, hospitaldata):
    con = sqlite3.connect(filename)
    cur = con.cursor()
    cur.execute("""SELECT COUNT(*) from Login """)
    result=cur.fetchall()
    if result[0][0]==0:
        cur.executemany(""" INSERT INTO Login(Username, Password) VALUES (?,?)""",
            hospitaldata
        )
    con.commit()
    con.close()

class MyApp(App):
    try:
        con = sqlite3.connect('user.db')
        cur = con.cursor()
        cur.execute(""" CREATE TABLE Login( 
        'Username' TEXT,
        'Password' TEXT    
        )
        """)
        cur.execute(""" CREATE TABLE User(
        'hname' TEXT,
        'location' TEXT,
        'language' TEXT,
        'contactinfo' TEXT,
        'nostaff' TEXT,
        'capacity' TEXT,
        'status' TEXT
        )
        """)
        cur.execute(""" CREATE TABLE Donation(
        'serial' TEXT,
        'makemodel' TEXT,
        'manual' TEXT,
        'servinfo' TEXT,
        'prevmaint' TEXT,
        'nextmaint' TEXT,
        'disposal' TEXT,
        'contact' TEXT
        )
        """)
        con.commit()
        con.close()

    except:
       pass

    # Define registered hospitals
    # Not the best method but the best I could think of for now
    # To do: Add functionality to register new hospitals if deemed necessary
    hospitaldata = [('UCD', 'UCD2019'), ('Steinn', 'Iceland'), ('085195', 'Emma')]
    # Input registered hospitals if table was empty
    RegisteredHospitals('user.db', hospitaldata)

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
