from requests import get 
from bs4 import BeautifulSoup
import logging
import re


# add a GUI where you enter all the information for a product, then list of titles and you can click on them, so need the href
# [b]Yo: [ref='www.youtube.com']Laptop title[/ref][/b]

logger = logging.getLogger(__name__) # Creates an instance of the Logger class, so that we can configure it using handlers and display information 

BASE_URL = 'https://www.mercari.com/search/'

def _find_match(pattern, words):
	match = pattern.search(words)
	return match

# Sample Regex for finding Intel processors: Look for '\bi\d\b', which is find any i next to a digit (i3, i5, i7)
# Regex for ram, if : Look for '\b\d{2}?|64GB\b'. or '\b\d{2}?|64 GB\b'
# Regex for storage: Look for '\b\d{3}GB\b' or '\b\d TB\b'
# Laptop brand is in the same spot everytime. Get a tuple of brands.
class _item:
	def __init__(self, information): # get a brand name from title
		title, price, *misc = information.split('$') # Should I do this as a method in the class?
		self._title = title
		self._price = price 
		self._misc = misc

	def __str__(self): # Could do a __repr__ and __str__, where __str__ only has brand name, key information, and price
		return f'{self._title[3:]}: ${self._price}'

# Dictionaries translate the string version of categories and conditions to the numerical ids for the website
# Have to revamp this
categoryIds = {'Women': 1, 'Men': 2, 
'Electronics': {'Computers & Laptops': {'Laptops & netbooks': 771, 'Desktops & all-in-ones': 772}}}

conditionIds = {'New': 1, 'Like New': 2, 'Good': 3}

sortbyIds = {'Best match': 1, 'Newest first': 2, 'Lowest price first': 3, 'Highest price first': 4, 'Number of likes': 5}

BRANDS = ('ASUS', 'Acer', 'HP', 'Toshiba', 'Lenovo', 'Dell', 'MSI', 'Alienware') # Search for these words in the title


'''Search for a product's url using keywords. Filter results based on the condition and category of products.
Can also choose how to sort products.'''
def _get_url(keywords, conditions: str = None, categories: str = None, sortby: str = None):
	url = BASE_URL + '?'
	keywords = keywords.split()
	keywords = '%20'.join(keywords)
	keywords_url = f'keyword={keywords}'
	url += keywords_url + '&'

	if categories: # Still the issue of 
		for categories in category_path:
			category_id = category_id[category]
		category_url = f'categoryIds={category_id}'
		url += category_url + '&'

	if conditions:
		conditions = [str(conditionIds[condition]) for condition in conditions]
		conditions = '-'.join(conditions)
		conditions_url = f'itemConditions={conditions}'
		url += conditions_url + '&'

	if sortby:
		sortby_url = f'sortBy={sortbyIds[sortby]}'
		url += sortby_url

	return url

'''_method_name to indictate that the method is not used when importing this package, rather it is only to be used
within the package itself in other methods. getters, setters, mutation methods, private variables, encapsulation.'''
def _get_soup(url):		
	logger.info(f'GET: {url}') # 'GET' HTTP request data from a website
	'''HTTP headers let me pass additional information with an HTTP request
	User-Agent: Network protocol peers can see which browser I am 'using'''
	headers = {'User-Agent': "'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 " # these are the ML "agents" that completes tasks for humans
	                         "(KHTML, like Gecko) Chrome/29.0.1547.62 Safari/537.36'"}
	response = get(url, headers=headers, timeout=20) # wait 20s for website to send a response
	assert response.status_code == 200 # if response.status_code != 200, raise an AssertionError. 200 status code means a response was sent.
	soup = BeautifulSoup(response.content, 'lxml')
	return soup

def _process_soup(soup):
	posts = soup.find_all('div', {'class': 'Flex__Box-ych44r-1'})[:-1]
	for post in posts[1:]: # empty first element
		# link = post.find('div')
		# <a href alt='IMPORTANT INFO'></a> not working for some reason
		# Need to get URL for each post. Also getting the stats from the webpage itself. 

		post_title = post.get_text()
		test_item = _item(post_title)
		print(test_item)
		_pattern = re.compile(r'\b\d{2}GB')
		_find_match(_pattern, post_title)
		_pattern = re.compile(r'\bi\d')
		intel_cpu = _find_match(_pattern, post_title)
		if intel_cpu:
			print('CPU: Intel Core ' + intel_cpu.group(0))
		_pattern = re.compile(r'\b(?i:\wTX)\s?\d{3,4}') # (?i)(\wTX) doesn't work. Using inline flag name locally (within parentheses)
		nvidia_gpu = _find_match(_pattern, post_title)
		if nvidia_gpu:
			print('GPU: ' + nvidia_gpu.group(0))
		print('*' * 100)



if __name__ == '__main__':
	_process_soup(_get_soup(url))

	html = '''<a href="some_url">next</a>
	<span class="class"><a href="another_url">later</a></span>'''

	soup = BeautifulSoup(html, 'lxml')
	print(type(soup))
	for a in soup.find_all('a', href=True):
	    print("Found the URL:", a['href'])

	soup = BeautifulSoup('<a class="nav-link match-link-stats" href="/football/matches/match867851_Kalteng_Putra-Arema-online/" title="Stat"><i class="icon-match-link"></i></a>', 'lxml')
	tag = soup.find('a')
	type(tag)
	print(tag.get('href'))
	tag['href']

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
# GUI

'''Current goals:
Implement cool looking GUI skins
'''

# Have to add Roboto-Light.tff manually, can I automate for people downloading it as an executable?
Config.set('kivy', 'default_font', ['data/fonts/Roboto-Light.tff', 'data/fonts/Roboto-Regular.ttf', 'data/fonts/Roboto-Italic.ttf', 'data/fonts/Roboto-Bold.ttf', 'data/fonts/Roboto-BoldItalic.ttf']) 
Config.write()

class SearchScreen(GridLayout):

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

        def search_products(instance):
            # print(f'Keywords: {self.keywords.text}, Conditions: {self.conditions}, Categories: {self.categories}, Sortby: {self.sortby}')
             self.keywords.text, self.conditions, self.categories, self.sortby

        self.search_btn = Button(text='Search Products', color=(1, 1, 1, 1), background_color=(.21, 1.24, 2.25, 0.9))
        self.search_btn.bind(on_release=lambda _: get_products(self.keywords.text, conditions=self.conditions, categories=self.categories, sortby=self.sortby))
        self.add_widget(self.search_btn)


# Alternative colors: (21, 124, 251), (165, 206, 254)
# (0.01, 206, 255, 0.9)

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