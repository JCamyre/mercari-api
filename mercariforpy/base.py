from requests import get 
from bs4 import BeautifulSoup
import logging
import re


# add a GUI where you enter all the information for a product, then list of titles and you can click on them, so need the href

logger = logging.getLogger(__name__) 

BASE_URL = 'https://www.mercari.com/search/'

def _find_match(pattern, words):
	match = pattern.search(words)
	return match

# May get rid of this, I think dictionaries are fine
class _item:
	def __init__(self, title, price, url):
		self._title = title
		self._price = price 
		self._url = url

	def __str__(self): 
		return f'{self._title[3:]}: ${self._price}'

category_ids = {'Women': 1, 'Men': 2, 'Electronics': 7, 'Computers': 77, 'Laptops': 771, 
'Desktops & all-in-ones': 772}

conditionIds = {'New': 1, 'Like New': 2, 'Good': 3}

sortbyIds = {'Best match': 1, 'Newest first': 2, 'Lowest price first': 3, 'Highest price first': 4, 'Number of likes': 5}

BRANDS = ('ASUS', 'Acer', 'HP', 'Toshiba', 'Lenovo', 'Dell', 'MSI', 'Alienware') # Search for these words in the title


'''Search for a product's url using keywords. Filter results based on the condition and category of products.
Can also choose how to sort products.'''
def _get_url(keywords, conditions: list = None, categories: list = None, sortby: str = None):
	url = BASE_URL + '?'
	keywords = keywords.split()
	keywords = '%20'.join(keywords)
	keywords_url = f'keyword={keywords}'
	url += keywords_url + '&'

	if categories: 
		# for category in categories:
		category = categories[-1]
		category_id = category_ids[category]
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

# Uses url from _get_url to get request the HTML from the webpage, then converts and returns the soup
def _get_soup(url):		
	logger.info(f'GET: {url}')
	headers = {'User-Agent': "'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 " # Telling the website what browser I am "using"
							 "(KHTML, like Gecko) Chrome/29.0.1547.62 Safari/537.36'"}
	response = get(url, headers=headers, timeout=20)
	assert response.status_code == 200
	soup = BeautifulSoup(response.content, 'lxml')
	return soup

# Uses the soup from _get_soup to search for keywords in the title, such as quantity of ram, CPU, GPU, etc
def _process_soup(soup):
	products = []
	posts = soup.find_all('div', {'class': 'Flex__Box-ych44r-1'})[:-1]
	for post in posts[1:]: # empty first element
		# link = post.find('div')
		# <a href alt='IMPORTANT INFO'></a> not working for some reason
		# Need to get URL for each post. Also getting the stats from the webpage itself. 

		product = dict()

		post_title = post.find('div', {'data-testid': 'ItemName'})
		product['title'] = ' '.join(post_title.get_text().split())
		post_info = post_title.get_text()

		# Ram
		_pattern = re.compile(r'\b\d{2}GB')
		_find_match(_pattern, post_info)
		# Intel CPU
		_pattern = re.compile(r'\bi\d')
		intel_cpu = _find_match(_pattern, post_info)
		# if intel_cpu:
		# 	print('CPU: Intel Core ' + intel_cpu.group(0))
		# Nvidia GPU
		_pattern = re.compile(r'\b(?i:\wTX)\s?\d{3,4}')
		nvidia_gpu = _find_match(_pattern, post_info)
		# if nvidia_gpu:
		# 	print('GPU: ' + nvidia_gpu.group(0))

		# Price
		# _pattern = re.compile(r'\$\S{3,5}\s') # \d{3,4} \S{3,5}

		a = post.find('a')
		price = a.find('p', {'data-testid': 'ItemPrice'})
		product['price'] = price.get_text().split()[0]


		# Url
		link = a['href']
		product['url'] = 'mercari.com' + link 

		products.append(product)
	return products

# Display the products found that fit the criteria (keywords, categories, conditions) sorted by what is chosen
def get_products(keywords, categories=None, conditions={'Like New', 'Good'}, sortby=None):
	return _process_soup(_get_soup(_get_url(keywords, categories=categories, conditions=conditions, sortby=sortby)))
	# Make new Kivy screen to handle displaying products

if __name__ == '__main__':
	pass


