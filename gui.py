from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.config import Config

# Have to add Roboto-Light.tff manually, can I automate for people downloading it as an executable?
Config.set('kivy', 'default_font', ['data/fonts/Roboto-Light.tff', 'data/fonts/Roboto-Regular.ttf', 'data/fonts/Roboto-Italic.ttf', 'data/fonts/Roboto-Bold.ttf', 'data/fonts/Roboto-BoldItalic.ttf']) 
Config.write()

class SearchScreen(GridLayout):

    def __init__(self, **kwargs):
        super(SearchScreen, self).__init__(**kwargs)
        self.cols = 1
        self.keywords = TextInput(hint_text='search keywords', multiline=False, size_hint=(.2, None), height=30) # , 
        self.add_widget(self.keywords)
        self.condition = TextInput(hint_text='enter desired conditions', multiline=False, size_hint=(.2, None), height=30)
        self.add_widget(self.condition)

        # Category Selection
        electronics_dropdown = DropDown()
        computers_dropdown = DropDown()

        self.computers_btn = Button(text='Computers', size_hint=(.2, None), height=30)
        self.computers_btn.bind(on_release=computers_dropdown.open)
        self.laptops = Button(text='Laptops', size_hint=(.2, None), height=30)
        self.laptops.bind(on_release=lambda btn: computers_dropdown.select(btn.text))
        computers_dropdown.add_widget(self.laptops)

        self.electronics_btn = Button(text='Electronics', size_hint=(.2, None), height=30)
        self.electronics_btn.bind(on_release=electronics_dropdown.open)
        electronics_dropdown.add_widget(self.computers_btn)
        self.add_widget(self.electronics_btn)

        conditions_dropdown = DropDown()
        self.conditions_btn = Button(text='Conditions', size_hint=(.2, None), height=30)
        self.conditions_btn.bind(on_release=conditions_dropdown.open)
        for condition in ['New', 'Like New', 'Good']:
            btn = Button(text=condition, size_hint=(.2, None), height=30)
            btn.bind(on_release=lambda btn: conditions_dropdown.select(btn.text))
            conditions_dropdown.add_widget(btn)
        self.add_widget(self.conditions_btn)


        # Have a selection for sortby.
        # Should I do categories a selection thing?
        self.search_btn = Button(text='Search Products')
        self.search_btn.bind(on_release=lambda x: print('yo'))
        self.add_widget(self.search_btn)





class MyApp(App):

    def build(self):
        return SearchScreen()


if __name__ == '__main__':
    MyApp().run()

'''
class Menu(BoxLayout):
    def __init__(self,**kwargs):
        super(Menu, self).__init__(**kwargs)
        Clock.schedule_interval(self.getTemp, 1)
    def getTemp(self,dt):
        thetemp = 55 #will be changed to temp.read()
        self.TempLabel.text = str(thetemp)
        print(thetemp)

or

<ScreenThermo>:
    Label:
        #this is where i want my label that shows the temperature my sensor reads
        text: root.thermo_text


class ScreenThermo(BoxLayout):
      thermo_text = StringProperty("stuff")
my_screen.thermo_text = "ASD"
'''