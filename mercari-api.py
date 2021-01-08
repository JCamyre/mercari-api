from requests import get 
from bs4 import BeautifulSoup
import logging
import re

# add a GUI

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
		return f'{self._title}: ${self._price}'

# Dictionaries translate the string version of categories and conditions to the numerical ids for the website
categoryIds = {'Women': 1, 'Men': 2, 
'Electronics': {'Computers & Laptops': {'Laptops & netbooks': 771, 'Desktops & all-in-ones': 772}}}

conditionIds = {'New': 1, 'Like New': 2, 'Good': 3}

'''Search for a product's url using keywords. Filter results based on the condition and category of products.
Can also choose how to sort products.'''
def _get_url(keywords, conditions: str = None, category: str = None, sortby: str = None):
	url = BASE_URL + '?'
	keywords = keywords.split()
	keywords = '%20'.join(keywords)
	keywords_url = f'keyword={keywords}'
	url += keywords_url + '&'
	if category: 
		category_path = category.split('/')
		category_id = categoryIds
		for category in category_path:
			category_id = category_id[category]
		category_url = f'categoryIds={category_id}'
		url += category_url + '&'

	if conditions:
		conditions = conditions.split(', ')
		conditions = [str(conditionIds[condition]) for condition in conditions]
		conditions = '-'.join(conditions)
		conditions_url = f'itemConditions={conditions}'
		url += conditions_url

	return url

url = _get_url('gaming laptop', conditions='Like New, Good', category='Electronics/Computers & Laptops/Laptops & netbooks')

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

soup = _get_soup(url)
posts = soup.find_all('div', {'class': 'Flex__Box-ych44r-1'})[:-1]
for post in posts[1:]: # empty first list
	# link = post.find('div')
	# <a href alt='IMPORTANT INFO'></a> not working for some reason
	# Need to get URL for each post.
	post_title = post.get_text()
	test_item = _item(post_title)
	print(test_item)
	_pattern = re.compile(r'\b\d{2}GB') # ?|64 \b
	_find_match(_pattern, post_title)
	_pattern = re.compile(r'\bi\d')
	intel_cpu = _find_match(_pattern, post_title)
	if intel_cpu:
		print('Intel Core ' + intel_cpu.group(0))
	_pattern = re.compile(r'\b(?i:\wTX)\s?\d{3,4}') # (?i)(\wTX) doesn't work. Using inline flag name locally (within parentheses)
	nvidia_gpu = _find_match(_pattern, post_title)
	if nvidia_gpu:
		print(nvidia_gpu.group(0))
	print('*' * 100)


