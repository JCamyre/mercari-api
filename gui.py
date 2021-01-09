from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown


class SearchScreen(GridLayout):

    def __init__(self, **kwargs):
        super(SearchScreen, self).__init__(**kwargs)
        self.cols = 1
        self.keywords = TextInput(hint_text='search keywords', multiline=False, size_hint=(.2, None), height=30)
        self.add_widget(self.keywords)
        self.condition = TextInput(hint_text='enter desired conditions', multiline=False, size_hint=(.2, None), height=30)
        self.add_widget(self.condition)
        
        # Have a selection for sortby.
        # Should I do categories a selection thing?
        self.search_btn = Button(text='Search Products')
        self.add_widget(self.search_btn)





class MyApp(App):

    def build(self):
        return SearchScreen()


if __name__ == '__main__':
    MyApp().run()