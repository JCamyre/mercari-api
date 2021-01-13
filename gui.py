from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.config import Config
from kivy.uix.spinner import Spinner
from kivy.uix.togglebutton import ToggleButton

'''Current goals:
Implement cool looking GUI skins
'''

# Have to add Roboto-Light.tff manually, can I automate for people downloading it as an executable?
Config.set('kivy', 'default_font', ['data/fonts/Roboto-Light.tff', 'data/fonts/Roboto-Regular.ttf', 'data/fonts/Roboto-Italic.ttf', 'data/fonts/Roboto-Bold.ttf', 'data/fonts/Roboto-BoldItalic.ttf']) 
Config.write()

class SearchScreen(GridLayout):

    def __init__(self, **kwargs):
        super(SearchScreen, self).__init__(**kwargs)
        self.cols = 1
        self.keywords = TextInput(hint_text='Enter keywords', multiline=False, size_hint=(.2, None), height=30) # , 
        self.add_widget(self.keywords)
        self.categories = set()
        self.conditions = set()
        self.sortby = 'Best match'

        # Category Selection
        electronics_dropdown = DropDown()
        computers_dropdown = DropDown()

        self.computers_btn = Button(text='Computers', size_hint=(.2, None), height=30)
        self.computers_btn.bind(on_release=computers_dropdown.open)
        self.laptops = ToggleButton(text='Laptops', size_hint=(.2, None), height=30) # 
        self.desktops = ToggleButton(text='Desktops', size_hint=(.2, None), height=30)

        def choose_category(instance, text):
            self.categories = text # Equivalent for lambda instance, text: setattr(self, 'category', text)
            print(f'Currently selected: {self.categories}')

        self.laptops.bind(on_release=lambda btn: computers_dropdown.select(btn.text))
        # lambda instance, x: print(instance, x)
        computers_dropdown.bind(on_select = choose_category) # "Listen for the selection". This is the highly coveted DropDown.select()
        computers_dropdown.add_widget(self.laptops)

        self.electronics_btn = Button(text='Electronics', size_hint=(.2, None), height=30)
        self.electronics_btn.bind(on_release=electronics_dropdown.open)
        electronics_dropdown.add_widget(self.computers_btn)
        electronics_dropdown.bind(on_select=choose_category)
        self.add_widget(self.electronics_btn)

        conditions_dropdown = DropDown()
        self.conditions_btn = Button(text='Conditions', size_hint=(.2, None), height=30)
        self.conditions_btn.bind(on_release=conditions_dropdown.open)
        for condition in ['New', 'Like New', 'Good']:
            btn = ToggleButton(text=condition, size_hint=(.2, None), height=30)
            btn.bind(on_release=lambda btn: conditions_dropdown.select(btn.text))
            conditions_dropdown.add_widget(btn)
        def choose_conditions(instance, condition):
            if condition in self.conditions:
                self.conditions.remove(condition)
            else:
                self.conditions.add(condition)

        conditions_dropdown.bind(on_select=choose_conditions)
        self.add_widget(self.conditions_btn)

        sortby_spinner = Spinner(
            text='Best match',
            values=('Newest', 'Ascending', 'Descending', 'Number of likes'),
            size_hint=(None, None),
            size=(100, 44),
            pos_hint={'center_x': .5, 'center_y': .5})

        def choose_sortby(spinner, text):
            self.sortby = text
            print(f'You are currently sorting by: {self.sortby}')

        sortby_spinner.bind(text=choose_sortby)
        self.add_widget(sortby_spinner)

        # Have a selection for sortby.
        # Should I do categories a selection thing?
        def search_products(instance):
            print(f'Keywords: {self.keywords} Conditions: {self.conditions} Categories: {self.categories} Sortby: {self.sortby}')
            

        self.search_btn = Button(text='Search Products')
        self.search_btn.bind(on_release=search_products)
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