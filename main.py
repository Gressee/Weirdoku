from defines import *
import app as app

from kivy.core.window import Window

if __name__ == '__main__':
    Window.size = (560, 1000)
    Window.clearcolor = C_DARK
    app.MainApp().run()