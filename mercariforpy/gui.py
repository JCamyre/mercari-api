from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.config import Config
from kivy.uix.spinner import Spinner
from kivy.uix.togglebutton import ToggleButton
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen

from .base import get_products

'''Current goals:
Implement cool looking GUI skins
Add new Kivy screen which will display image, link, title/description of products after searching
'''

# Have to add Roboto-Light.tff manually, can I automate for people downloading it as an executable?
Config.set('kivy', 'default_font', ['data/fonts/Roboto-Light.tff', 'data/fonts/Roboto-Regular.ttf', 'data/fonts/Roboto-Italic.ttf', 'data/fonts/Roboto-Bold.ttf', 'data/fonts/Roboto-BoldItalic.ttf']) 
Config.write()


class SearchScreen(Screen, GridLayout):

    def __init__(self, **kwargs):
        super(SearchScreen, self).__init__(**kwargs)
        Window.clearcolor = (1, 1, 1, 0.2)
        self.light_theme = True # False == dark theme
        self.cols = 1
        self.keywords = TextInput(hint_text='Enter keywords', multiline=False, size_hint=(.2, None), 
        height=30, background_color=(0, 0, 0, 0.2), foreground_color=(1, 1, 1, 1)) # , 
        self.add_widget(self.keywords)
        self.categories = set()
        self.conditions = set()
        self.sortby = 'Best match'

        # Category Selection
        self.options = GridLayout()
        self.options.rows = 1
        categories_dropdown = DropDown()
        electronics_dropdown = DropDown()
        computers_dropdown = DropDown()

        def dropdown_btn(btn, dropdown):
            dropdown.open(btn)
            self.categories.add(btn.text)

        self.computers_btn = Button(text='Computers', size_hint=(.2, None), height=30)
        self.computers_btn.bind(on_release=lambda btn: dropdown_btn(btn, computers_dropdown))
        self.laptops = ToggleButton(text='Laptops', size_hint=(.2, None), height=30) # 
        self.desktops = ToggleButton(text='Desktops', size_hint=(.2, None), height=30)

        def choose_category(instance, text):
            if text in self.categories:
                self.categories.remove(text)
            else:
                self.categories.add(text) # Equivalent for lambda instance, text: setattr(self, 'category', text)

        self.laptops.bind(on_release=lambda btn: computers_dropdown.select(btn.text))
        computers_dropdown.bind(on_select = choose_category) # "Listen for the selection". This is the highly coveted DropDown.select()
        computers_dropdown.add_widget(self.laptops)

        self.electronics_btn = Button(text='Electronics', size_hint=(None, None), height=30, 
                                        color=(1, 1, 1, 1), background_color=(.21, 1.24, 2.25, 0.9))
        self.electronics_btn.bind(on_release=lambda btn: dropdown_btn(btn, electronics_dropdown))
        electronics_dropdown.add_widget(self.computers_btn)
        electronics_dropdown.bind(on_select=choose_category)

        self.categories_btn = Button(text='Categories', size_hint=(.1, None), height=30, 
                                        color=(1, 1, 1, 1), background_color=(.21, 1.24, 2.25, 0.9))
        self.categories_btn.bind(on_release=categories_dropdown.open)
        categories_dropdown.add_widget(self.electronics_btn)
        self.options.add_widget(self.categories_btn)

        # Conditions Selection
        conditions_dropdown = DropDown()
        self.conditions_btn = Button(text='Conditions', size_hint=(.1, None), height=30, color=(1, 1, 1, 1), background_color=(.21, 1.24, 2.25, 0.9))
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
        self.options.add_widget(self.conditions_btn)

        # Sortby Selection
        sortby_spinner = Spinner(
            text='Best match',
            values=('Newest first', 'Lowest price first', 'Highest price first', 'Number of likes'),
            size_hint=(.1, None),
            height=30,
            pos_hint={'center_x': .5, 'center_y': .5}, 
            color=(1, 1, 1, 1), 
            background_color=(.21, 1.24, 2.25, 0.9))

        def choose_sortby(spinner, text):
            self.sortby = text

        sortby_spinner.bind(text=choose_sortby)
        self.options.add_widget(sortby_spinner)
        self.add_widget(self.options)

        def search_products(keywords, categories=None, conditions={'Like New', 'Good'}, sortby=None):
            info = get_products(keywords, categories=categories, conditions=conditions, sortby=sortby)
            root.manager.current = 'products'
            return ProductsScreen(info)


        self.search_btn = Button(text='Search Products', color=(1, 1, 1, 1), background_color=(.21, 1.24, 2.25, 0.9))
        self.search_btn.bind(on_release=lambda _: search_products(self.keywords.text, categories=self.conditions, conditions=self.categories, sortby=self.sortby))
        self.add_widget(self.search_btn)

# Alternative colors: (21, 124, 251), (165, 206, 254), (0.01, 206, 255, 0.9)


class ProductsScreen(Screen, GridLayout):
    def __init__(self, info, **kwargs):
        super(ProductsScreen, self).__init__(**kwargs)
        Window.clearcolor = (1, 1, 1, 0.2)
        self.cols = 3 # Title, price, link
        for title, price, link in info:
            self.add_widget(Label(text=title))
            self.add_widget(Label(text=price))
            self.add_widget(Label(text=link))





class MyApp(App):

    def build(self):
        sm = ScreenManager()
        sm.add_widget(Screen(name='search'))
        sm.add_widget(Screen(name='products'))

        return sm


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