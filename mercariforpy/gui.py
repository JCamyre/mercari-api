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
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle
from kivy.uix.widget import Widget
from kivy.lang.builder import Builder
import webbrowser

from .base import get_products

'''Current goals:
Implement cool looking GUI skins
Add new Kivy screen which will display image, link, title/description of products after searching
'''
LIGHTBLUE = (0.21, 1.24, 2.25, 0.9)
# Have to add Roboto-Light.tff manually, can I automate for people downloading it as an executable?
Config.set('kivy', 'default_font', ['data/fonts/Roboto-Light.tff', 'data/fonts/Roboto-Regular.ttf', 'data/fonts/Roboto-Italic.ttf', 'data/fonts/Roboto-Bold.ttf', 'data/fonts/Roboto-BoldItalic.ttf']) 
Config.write()

bg_label = Builder.load_string('''
<BackgroundColor@Widget>
    background_color: 1, 1, 1, 1
    canvas.before:
        Color:
            rgba: root.background_color
        Rectangle:
            size: self.size
            pos: self.pos
            
<BackgroundLabel@Label+BackgroundColor>
    background_color: 0, 0, 0, 0

BackgroundLabel
''')

class BackgroundColor(Widget):
    def __init__(self):
        app = App.get_running_app()
        background_color = 1, 1, 1, 1
        with self.canvas.before: 
            Color(rgba=app.root.background_color)
            Rectangle(size=self.size, pos=self.pos)

class BackgroundLabel(Label, BackgroundColor):
    background_color = 0, 0, 0, 0

class SearchScreen(GridLayout, Screen):

    def __init__(self, **kwargs):
        super(SearchScreen, self).__init__(**kwargs)
        Window.clearcolor = (1, 1, 1, 0.1)
        self.cols = 1
        self.keywords = TextInput(hint_text='Enter keywords', multiline=False, size_hint=(.2, None), 
        height=30, background_color=(0, 0, 0, 0.2), foreground_color=(1, 1, 1, 1)) # , 
        self.add_widget(self.keywords)
        self.categories = []
        self.conditions = set()
        self.sortby = 'Best match'

        def change_theme(instance):
            if instance.state == 'down':
                instance.text = 'Light Mode'
                Window.clearcolor = (0, 0, 0, 1)
                # Change buttons bg color to black
            else:
                instance.text = 'Dark Mode'
                Window.clearcolor = (1, 1, 1, 0.1)

        theme_btn = ToggleButton(text='Dark Mode', size_hint=(None, 0.2))
        theme_btn.bind(on_release=change_theme)
        self.add_widget(theme_btn)

        # Category Selection
        self.options = GridLayout()
        self.options.rows = 1
        categories_dropdown = DropDown()
        electronics_dropdown = DropDown()
        computers_dropdown = DropDown()

        def choose_category(_, text):
            if text in self.categories:
                self.categories.remove(text)
            else:
                self.categories.append(text) # Equivalent for lambda instance, text: setattr(self, 'category', text)
        
        def dropdown_btn(btn, dropdown):
            dropdown.open(btn)
            choose_category('', btn.text)

        self.computers_btn = Button(text='Computers', size_hint=(.2, None), height=30)
        self.computers_btn.bind(on_release=lambda btn: dropdown_btn(btn, computers_dropdown))
        self.laptops = ToggleButton(text='Laptops', size_hint=(.2, None), height=30) # 
        self.desktops = ToggleButton(text='Desktops', size_hint=(.2, None), height=30)

        self.laptops.bind(on_release=lambda btn: computers_dropdown.select(btn.text))
        computers_dropdown.bind(on_select = choose_category) # "Listen for the selection". This is the highly coveted DropDown.select()
        computers_dropdown.add_widget(self.laptops)

        self.electronics_btn = Button(text='Electronics', size_hint=(None, None), height=30, 
                                        color=(1, 1, 1, 1), background_color=LIGHTBLUE)
        self.electronics_btn.bind(on_release=lambda btn: dropdown_btn(btn, electronics_dropdown))
        electronics_dropdown.add_widget(self.computers_btn)
        electronics_dropdown.bind(on_select=choose_category)

        self.categories_btn = Button(text='Categories', size_hint=(.1, None), height=30, 
                                        color=(1, 1, 1, 1), background_color=LIGHTBLUE)
        self.categories_btn.bind(on_release=categories_dropdown.open)
        categories_dropdown.add_widget(self.electronics_btn)
        self.options.add_widget(self.categories_btn)

        # Conditions Selection
        conditions_dropdown = DropDown()
        self.conditions_btn = Button(text='Conditions', size_hint=(.1, None), height=30, color=(1, 1, 1, 1), background_color=LIGHTBLUE)
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
            background_color=LIGHTBLUE)

        def choose_sortby(spinner, text):
            self.sortby = text

        sortby_spinner.bind(text=choose_sortby)
        self.options.add_widget(sortby_spinner)
        self.add_widget(self.options)

        def search_products(keywords, conditions={'Like New', 'Good'}, categories=None, sortby=None):
            # Put check in place for 
            info = get_products(keywords, conditions=conditions, categories=categories, sortby=sortby)
            self.manager.current = 'products'
            self.manager.current_screen.load_products(info) # Directly referencing the screenobject, not the name

        self.search_btn = Button(text='Search Products', color=(1, 1, 1, 1), background_color=LIGHTBLUE)
        self.search_btn.bind(on_release=lambda _: search_products(self.keywords.text, conditions=self.conditions, categories=self.categories, sortby=self.sortby))
        self.add_widget(self.search_btn)

# Alternative colors: (21, 124, 251), (165, 206, 254), (0.01, 206, 255, 0.9)


class ProductsScreen(GridLayout, Screen):
    def __init__(self, info=None, **kwargs):
        super(ProductsScreen, self).__init__(**kwargs)
        Window.clearcolor = (1, 1, 1, 0.2)
        self.cols = 1 # Title, price, url

        def change_screen(self):
            self.manager.current_screen.clear_widgets()
            self.manager.current = 'search'

        self.return_btn = Button(text='return')
        self.return_btn.bind(on_release=lambda _: self.change_screen())

    def load_products(self, info): # How to clear elements?
        self.scroll = ScrollView(size=self.size)
        self.layout = GridLayout(cols=3, size_hint_y=None, size=(1000, len(info) * 100), spacing=(0, 5), padding=(0, 0)) # GridLayout.size.y must be > ScrollView.size.y for it to scroll
        if info:
            for item in info:
                title = BackgroundLabel(text=item['title'], color=(0, 0, 0, 1), background_color=LIGHTBLUE)
                self.layout.add_widget(title)
                price = BackgroundLabel(text=f'Price: {item["price"]}', size_hint=(None, 0.2), color=(0, 0, 0, 1), background_color=LIGHTBLUE)
                self.layout.add_widget(price) # , background_color=LIGHTBLUE
                btn = Button(text=item['url'], color=(1, 1, 1, 1), background_color=LIGHTBLUE, on_release=lambda instance: webbrowser.open(instance.text))
                # Changed environment variable to use Chrome for webbrowser
                # The reason for every button url being the same is because when the button is pressed, it looks for item['url'] to be ran, and the last item['url'] is the from the last item in the dictionary, so they all go to the same url
                self.layout.add_widget(btn) # For some reason, all buttons are bound to the url = item[-1]['url']

        self.scroll.add_widget(self.layout)
        self.add_widget(self.scroll)

class MyApp(App):

    def build(self):
        sm = ScreenManager()
        sm.add_widget(SearchScreen(name='search'))
        sm.add_widget(ProductsScreen(name='products'))

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
        (thetemp)

or

<ScreenThermo>:
    Label:
        #this is where i want my label that shows the temperature my sensor reads
        text: root.thermo_text


class ScreenThermo(BoxLayout):
      thermo_text = StringProperty("stuff")
my_screen.thermo_text = "ASD"
'''