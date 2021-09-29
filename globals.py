from defines import *
from kivy.core.window import Window

grid_size: tuple = (0, 0)

# Every demension in px has to be multiplied by this
# factor to adjust for different screen sizes
# The screen width is is used bc height often varies 
# a bit for different aspect rations but the screen width 
# often is the same
scale = Window.width/DEFAULT_WIN_WIDTH
