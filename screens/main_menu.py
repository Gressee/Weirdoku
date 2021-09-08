from kivy.uix.behaviors.button import ButtonBehavior
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window

from defines import *
import globals as g
from utils import change_to_screen

import kivy
from kivy.uix.screenmanager import Screen
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button

class BtnPlay(ButtonBehavior, Label):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.font_size = 100 * Window.width/1080
    
    def on_press(self):
        # Change the Button color to the activation color set
        self.color = C_DARK
        with self.canvas.before:
            Color(C_BRIGHT[0], C_BRIGHT[1], C_BRIGHT[2], C_BRIGHT[3])
            Rectangle(pos=self.pos, size=self.size)
    
    def on_release(self):
        # Change visuals
        self.color = C_BRIGHT
        with self.canvas.before:
            Color(C_DARK[0], C_DARK[1], C_DARK[2], C_DARK[3])
            Rectangle(pos=self.pos, size=self.size)

        # Change screen
        change_to_screen(SCR_SIZE_SELECTION)

class ScrMainMenu(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.rel_layout = RelativeLayout()

        self.rel_layout.add_widget(BtnPlay(
            text='Play',
            size_hint=(None, None),
            size=(Window.width*.4, Window.width*.2),
            pos_hint={},
            pos=(( 1/2 * Window.width * (1-.4), Window.height*.5))
        ))


        self.add_widget(self.rel_layout)
