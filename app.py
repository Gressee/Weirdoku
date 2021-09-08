from defines import *
import globals as g
from screens.main_menu import ScrMainMenu
from screens.size_selection import ScrSizeSelection
from screens.game import ScrGame

import kivy 
from kivy.app import App
from kivy.uix.screenmanager import FadeTransition, ScreenManager



class MainApp(App):
    
    def build(self):
        # Create the screen manager
        self.sm = ScreenManager()
        # Add screens
        self.sm.add_widget(ScrMainMenu(name=SCR_MAIN_MENU))
        self.sm.add_widget(ScrSizeSelection(name=SCR_SIZE_SELECTION))
        self.sm.add_widget(ScrGame(name=SCR_GAME))

        return self.sm


