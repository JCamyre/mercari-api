from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

# Create both screens. Please note the root.manager.current: this is how
# you can control the ScreenManager from kv. Each screen has by default a
# property manager that gives you the instance of the ScreenManager used.
Builder.load_string("""

<SettingsScreen>:
    BoxLayout:
        Button:
            text: 'My settings button'
        Button:
            text: 'Back to menu'
            on_press: root.manager.current = 'menu'
""")

# Declare both screens
class MenuScreen(GridLayout, Screen):
    def __init__(self, **kwargs):
    	super(MenuScreen, self).__init__(**kwargs)
    	self.cols = 2
    	self.settings_btn = Button(text='Go to settings')
    	def change_screen(_):
    		self.manager.current = 'settings'
    	self.settings_btn.bind(on_press=change_screen)
    	self.add_widget(self.settings_btn)
    	self.add_widget(Label(text='yo'))


class SettingsScreen(Screen):
    pass

class TestApp(App):

    def build(self):
        # Create the screen manager
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(SettingsScreen(name='settings'))

        return sm

if __name__ == '__main__':
    TestApp().run()