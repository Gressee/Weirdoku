from kivy.clock import Clock
from kivy.uix.behaviors.button import ButtonBehavior
from kivy.uix.floatlayout import FloatLayout

from defines import *
import globals as g
from game import Game

import kivy
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle, Line

class Cell(ButtonBehavior, Label):

    def __init__(self, cell_grid, game: Game, grid_x, grid_y, **kwargs):
        super().__init__(**kwargs)
        self.cell_grid: CellGrid = cell_grid
        self.game: Game = game
        self.grid_x = grid_x
        self.grid_y = grid_y 
        
        self.text = ''
        self.bold = True
        self.font_size = 70 * Window.width/DEFAULT_WIN_WIDTH

        self.color

        self.update_visuals()

    def on_release(self):
        self.game.set_value(self.grid_x, self.grid_y, self.game.get_selected_value())
        self.cell_grid.update_visuals()

    def update_visuals(self):
        # Updtae backgroud color 
        self.canvas.before.clear()
        with self.canvas.before:
            if self.game.get_type(self.grid_x, self.grid_y) == TYPE_NORMAL:
                self.color = C_BRIGHT
                Color(C_DARK[0], C_DARK[1], C_DARK[2], C_DARK[3])
            elif self.game.get_type(self.grid_x, self.grid_y) == TYPE_HINT:
                self.color = C_DARK
                Color(C_BRIGHT_DARK[0], C_BRIGHT_DARK[1], C_BRIGHT_DARK[2], C_BRIGHT_DARK[3])
            elif self.game.get_type(self.grid_x, self.grid_y) == TYPE_SUM:
                self.color = C_DARK
                Color(C_RED[0], C_RED[1], C_RED[2], C_RED[3])
            Rectangle(pos=self.pos, size=self.size)
        
        # Update text
        t = self.game.get_value(self.grid_x, self.grid_y)
        if t == None or t == NO_VALUE: self.text = ''
        else: self.text = str(t)

    def mainloop(self, delta):
        # Later used for animation
        pass

class CellGrid(GridLayout):

    def __init__(self, game: Game, grid_size, **kwargs):
        super().__init__(**kwargs)
        self.game: Game = game

        self.cols = grid_size[0]
        self.rows = grid_size[1]
        # Padding is accounted for in the size and pos of this gridlayout
        self.padding = 0
        self.spacing = 0

        self.cells = []
        for x in range(grid_size[0]):
            for y in range(grid_size[0]):
                c = Cell(
                    cell_grid=self,
                    game=self.game,
                    grid_x=x,
                    grid_y=y
                )
                self.cells.append(c)
                self.add_widget(c)

        self.update_visuals()

    def update_visuals(self):
        # Update cells
        for c in self.cells:
            c.update_visuals()
        # Draw the grid lines
        self.canvas.after.clear()
        with self.canvas.after:
            Color(C_BRIGHT[0], C_BRIGHT[1], C_BRIGHT[2], C_BRIGHT[3])
            # Vertical
            g_size = self.game.get_grid_size()
            w = Window.width * 5/1080
            for i in range(g_size[0]+1):
                Line(
                    width=w,
                    close=False,
                    points=[self.pos[0] + int(i*self.size[0]/(g_size[0])), self.pos[1],
                            self.pos[0] + int(i*self.size[0]/(g_size[0])), self.pos[1] + self.size[1]]
                )
            for i in range(g_size[1]+1):
                Line(
                    width=w,
                    close=False,
                    points=[self.pos[0], self.pos[1] + int(i*self.size[1]/(g_size[1])),
                            self.pos[0] + self.size[0], self.pos[1] + int(i*self.size[1]/(g_size[1]))]
                )

    def mainloop(self, delta):
        # Later used for animation
        for c in self.cells:
            c.mainloop(delta)

class ValueSelector(ButtonBehavior, Label):
    def __init__(self, selector_grid, game: Game, value, **kwargs):
        super(ValueSelector, self).__init__(**kwargs)
        self.selector_grid: ValueSelectorGrid = selector_grid
        self.game: Game = game
        self.value = value

        # Special case if this is the delete value selector
        if value == NO_VALUE:
            self.text = 'X'
        else:
            self.text = str(value)
        self.font_size = 90 * Window.width/DEFAULT_WIN_WIDTH
        self.bold = True
        

    def on_release(self):
        self.game.set_selected_value(self.value)
        self.selector_grid.update_visuals()

    def update_visuals(self):
        # Disable the default button colors and make button white
        self.canvas.before.clear()
        if self.value == self.game.get_selected_value():
            # Text color
            self.color = C_DARK
            # Background color
            with self.canvas.before:
                Color(C_BRIGHT[0], C_BRIGHT[1], C_BRIGHT[2], C_BRIGHT[3])
                Rectangle(pos=self.pos, size=self.size)
            
        else:
            # Text color
            self.color = C_BRIGHT
            # Background color
            with self.canvas.before:
                Color(C_DARK[0], C_DARK[1], C_DARK[2], C_DARK[3])
                Rectangle(pos=self.pos, size=self.size)

    def mainloop(self, delta):
        # Later used for animation
        pass

class ValueSelectorGrid(GridLayout):

    def __init__(self, game: Game, **kwargs):
        super().__init__(**kwargs)
        self.game: Game = game
        
        self.cols = 5
        self.rows = 2
        self.spacing = 5
        self.padding = (15, 5)

        self.value_selectors = []
        # The -1 is to account for a delete value button
        # The +1 is so the MAX_GRID_VALUE is also handled
        for i in range(MIN_GRID_VALUE-1, MAX_GRID_VALUE+1):
            # Handle special case for the delete value button
            if i == MIN_GRID_VALUE-1:
                vs = ValueSelector(
                    selector_grid=self,
                    game=self.game,
                    value=NO_VALUE
                )
            else:
                # Normal value case
                vs = ValueSelector(
                    selector_grid=self,
                    game=self.game,
                    value=i
                )
            self.value_selectors.append(vs)
            self.add_widget(vs)
        
        self.update_visuals()
    
    def update_visuals(self):
        for vs in self.value_selectors:
            vs.update_visuals()

    def mainloop(self, delta):
        # Later used for animation
        for vs in self.value_selectors:
            vs.mainloop(delta)
            

class ScrGame(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Handles the game logic
        self.game = Game()

        self.float_layout = FloatLayout()
        self.add_widget(self.float_layout)

        self.value_selector_grid = ValueSelectorGrid(
            game=self.game,
            size=(Window.width, 2 * int(Window.width/5)),
            size_hint=(None, None),
            pos_hint={'x': 0, 'y': .05}
        )
        self.float_layout.add_widget(self.value_selector_grid)

    
    def on_pre_enter(self):
        # Initialise the game logic
        self.game.create(g.grid_size)
        self.cell_grid = CellGrid(
            game=self.game,
            grid_size=g.grid_size,
            size=(Window.width * .9, Window.width * .9),
            size_hint=(None, None),
            pos_hint={},
            pos=(Window.width * .05, Window.height * .4)
        )
        self.float_layout.add_widget(self.cell_grid)

        # Schedule mainloop with 30 fps
        self.mainloop_schedule = Clock.schedule_interval(self.mainloop, 1/30)

    def on_enter(self, *args):
        self.cell_grid.update_visuals()
        self.value_selector_grid.update_visuals()
    
    def on_leave(self):
        # Remove the cell grid bc it gets newly created on reenter
        self.remove_widget(self.cell_grid)

        # Unschedule mainloop
        Clock.unschedule(self.mainloop_schedule)

    def mainloop(self, delta):

        # Call the mainloop on cells and selectors
        self.cell_grid.mainloop(delta)
        self.value_selector_grid.mainloop(delta)
