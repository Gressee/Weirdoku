from defines import *
from utils import change_to_screen
import globals as g

from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.behaviors.button import ButtonBehavior
from kivy.graphics import Color, Rectangle, Line
from kivy.clock import Clock

class BtnSize(ButtonBehavior, Label):
    
    # This button is in the SizeGrid layout and
    # has one  specific size

    def __init__(self, grid_size: tuple, **kwargs):
        super().__init__(**kwargs)
        self.grid_size = grid_size

        self.text = f'{self.grid_size[0]} X {self.grid_size[0]}'
        self.font_size = 70 * Window.width/DEFAULT_WIN_WIDTH
        self.bold = True

        #self.set_color_up()

    def on_press(self):
        self.set_color_down()
    
    def on_release(self):
        self.set_color_up()

        # Set the grid size
        g.grid_size = self.grid_size
        
        # Change screen to game screen
        change_to_screen(SCR_GAME)
        

    def set_color_down(self):
        self.canvas.before.clear()
        # Text color
        self.color = C_DARK
        # Background color
        with self.canvas.before:
            Color(C_BRIGHT[0], C_BRIGHT[1], C_BRIGHT[2], C_BRIGHT[3])
            Rectangle(pos=self.pos, size=self.size)
            
    def set_color_up(self):
        self.canvas.before.clear()
        # Text color
        self.color = C_BRIGHT
        # Background color
        with self.canvas.before:
            Color(C_DARK[0], C_DARK[1], C_DARK[2], C_DARK[3])
            Rectangle(pos=self.pos, size=self.size)

class SizeGrid(GridLayout):

    # Stores all the buttons for the different sizes 
    # in a grid layout
    # Parrent is the scroll view on the screen

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.cols = 1
        self.rows = 10

        self.spacing = 20 * Window.width/DEFAULT_WIN_WIDTH
        self.padding = 50 * Window.width/DEFAULT_WIN_WIDTH

        for i in range(4, 14):
            self.add_widget(BtnSize(
                grid_size=(i, i),
            ))

class ScrSizeSelection(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.scroll_view = ScrollView(
            size_hint=(1, None),
            size=(Window.width, Window.height)
        )

        self.scroll_view.add_widget(SizeGrid(
            size=(Window.width, Window.height * 2),
            size_hint=(1, None),
            pos_hint={'x': 0, 'top': 1}
        ))

        self.add_widget(self.scroll_view)
