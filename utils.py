import app as app

from kivy.app import App

# Change the screen in the screen manager in MainApp
def change_to_screen(screen_name):
    main_app: app.MainApp = App.get_running_app()
    main_app.sm.current = screen_name

# Clamp a value
def clamp(val, smallest, largest):
    if val < smallest:
        val = smallest
    elif val > largest:
        val = largest
    return val