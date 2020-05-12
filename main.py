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
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.button import Button
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.graphics import Color
from kivy.graphics import Triangle
from kivy.graphics import Rectangle
from kivy.graphics import Color
from kivy.graphics import Line
from numpy import size
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
        cur.execute(""" SELECT Username, Password FROM Login WHERE Username=? AND Password=?""",
        (self.id_no.text, self.passw.text))
        result = cur.fetchone()
        if result:
            self.manager.current = 'split_window'
        else:
            show_popup()
        con.commit()
        con.close()


class P(FloatLayout):
    pass

def show_popup():
    show = P()

    #Default position is middle of screen, don't want dynamic resizing
    popupwindow = Popup(title = "Popup Window", content = show, size_hint=(None, None), size = (400, 400))

    popupwindow.open()

class SplitWindow(Screen):
    pass

class MainMenuDonor(Screen):
    pass

class MainMenuRecipient(Screen):
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
        cur.execute(""" DELETE FROM User WHERE hname=? """,
                     (self.hname.text,))
 
        cur.execute(
                """ INSERT INTO User (hname, location, language, contactinfo, nostaff, capacity, status) VALUES (?,?,?,?,?,?,?)""",
                (self.hname.text, self.location.text, self.language.text, self.contactinfo.text, self.nostaff.text,
                 self.capacity.text, self.status.text)
                )
        con.commit()
        con.close()

class ScanRFIDWindow(Screen, FloatLayout):
    pass

class ManualOverride(Screen):
    pass

class ViewDonations(Screen):
    def on_pre_enter(self, *args):
        con = sqlite3.connect('user.db')
        cur = con.cursor()
        filtered = cur.execute('SELECT * FROM Donation')
        self.items = filtered.fetchall()
        self.data = [{'text': self.items[x][1], 'id': str(x)} for x in range(size(self.items, 0))]
        con.commit()
        con.close()
        rv = self.ids.donation_rv
        rv.data = self.data
        rv.refresh_from_data()

class RequestDonation(Screen):

    typemach = ObjectProperty()
    makemodel = ObjectProperty()
    requir = ObjectProperty()
    lang = ObjectProperty()
    powconv = ObjectProperty()
    contact = ObjectProperty()

    def btn(self):
        self.manager.current = 'main_menu_recipient'

    def request(self):
        con = sqlite3.connect('user.db')
        cur = con.cursor()
        cur.execute(
            """INSERT INTO Recip_Req (typemach, makemodel, requir, lang, powconv, contact) VALUES(?,?,?,?,?,?)""",
            (self.typemach.text, self.makemodel.text, self.requir.text, self.lang.text, self.powconv.text,self.contact.text)
        )
        con.commit()
        con.close()
        self.typemach.text = ""
        self.makemodel.text = ""
        self.requir.text = ""
        self.lang.text = ""
        self.powconv.text = ""
        self.contact.text = ""


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
            """INSERT INTO Donation (serial, makemodel, manual, servinfo, prevmaint, nextmaint, disposal, contact) 
            VALUES(?,?,?,?,?,?,?,?)""",
            (self.serial.text, self.makemodel.text, self.manual.text, self.servinfo.text, self.prevmaint.text,
             self.nextmaint.text, self.disposal.text,
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


class AvailableList(Screen):
    def on_pre_enter(self, *args):
        self.items = filterDbBy('Available_Equipment', 'mach_type',AvailableEquipment.category)
        self.data = [{'text': self.items[x][1], 'id': str(x)} for x in range(size(self.items, 0))]
        rv = self.ids.available_rv
        rv.data = self.data
        rv.refresh_from_data()


class AvailableEquipment(Screen):
    category = ''

    @classmethod
    def updateCategory(cls, category):
        cls.category = category

class EquipmentInfo(Screen):
    def on_enter(self):
        self.updateInfo()

    def updateInfo(self):
        self.item = filterDbBy('Available_Equipment', 'mach_type', AvailableEquipment.category)[
            int(SelectableButton1.btn_id)]
        self.ids.title.text = AvailableEquipment.category.capitalize()
        self.ids.serial.text = self.item[0]
        self.ids.makemodel.text = self.item[2]
        self.ids.manual.text = self.item[3]
        self.ids.servinfo.text = self.item[4]
        self.ids.prevmaint.text = self.item[5]
        self.ids.nextmaint.text = self.item[6]
        self.ids.disposal.text = self.item[7]
        self.ids.contact.text = self.item[8]

class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior, RecycleBoxLayout):
    pass

class SelectableButton1(RecycleDataViewBehavior, Button):
    """ Add selection support to the Label """
    index = None
    btn_id = None

    def refresh_view_attrs(self, rv, index, data):
        """ Catch and handle the view changes """
        self.index = index
        return super(SelectableButton1, self).refresh_view_attrs(rv, index, data)

    @classmethod
    def updateBtn(cls, btn_id):
        cls.btn_id = btn_id


class SelectableButton2(RecycleDataViewBehavior, Button):
    """ Add selection support to the Label """
    index = None
    btn_id = None

    def refresh_view_attrs(self, rv, index, data):
        """ Catch and handle the view changes """
        self.index = index
        return super(SelectableButton2, self).refresh_view_attrs(rv, index, data)


class AvailableRV(RecycleView):
    rv_layout = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(AvailableRV, self).__init__(**kwargs)
        self.items = filterDbBy('Available_Equipment', 'mach_type', 'defibrillator')
        self.data = [{'text': self.items[x][1], 'id': str(x)} for x in range(size(self.items, 0))]

class DonationRV(RecycleView):
    rv_layout = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(DonationRV, self).__init__(**kwargs)
        con = sqlite3.connect('user.db')
        cur = con.cursor()
        filtered = cur.execute('SELECT * FROM Donation')
        self.items = filtered.fetchall()
        self.data = [{'text': self.items[x][1], 'id': str(x)} for x in range(size(self.items, 0))]
        con.commit()
        con.close()

# For transitions between windows
class WindowManager(ScreenManager):
    pass


def filterDbBy(table,field,term):
    con = sqlite3.connect('user.db')
    cur = con.cursor()
    filtered = cur.execute('SELECT * FROM {} WHERE {} =?'.format(table,field), (term,))
    res = filtered.fetchall()
    con.commit()
    con.close()
    return res


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
        cur.execute(""" CREATE TABLE Recip_Req(
        'typemach' TEXT,
        'makemodel' TEXT,
        'requir' TEXT,
        'lang' TEXT,
        'powconv' TEXT,
        'contact' TEXT
        )
         """)
        con.commit()
        con.close()

    except:
       pass

    path=''
    previous=''

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
