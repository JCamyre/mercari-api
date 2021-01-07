from requests import get 
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__) 

base_url = 'https://www.mercari.com/search/'

# Dictionaries translate the string version of categories and conditions to the numerical ids for the website
categoryIds = {'Women': 1, 'Men': 2, 
'Electronics': {'Computers & Laptops': {'Laptops & netbooks': 771, 'Desktops & all-in-ones': 772}}}

conditionIds = {'New': 1, 'Like New': 2, 'Good': 3}

'''Search for a product's url using keywords. Filter results based on the condition and category of products.
Can also choose how to sort products.'''
def search_url(keywords, conditions: str = None, category: str = None, sortby: str = None):
	url = base_url + '?'
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

url = search_url('gaming laptop', conditions='Like New, Good', category='Electronics/Computers & Laptops/Laptops & netbooks')
request = get(url)
soup = BeautifulSoup(request.content, 'lxml')
print(soup)
logger.info(f'GET: {url}')
headers = {'User-Agent': "'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 "
                         "(KHTML, like Gecko) Chrome/29.0.1547.62 Safari/537.36'"}
response = get(url, headers=headers, timeout=20)
assert response.status_code == 200
soup = BeautifulSoup(response.content, 'lxml')
print(soup.get_text())
'''_method_name to indictate that the method is not used when importing this package, rather it is only to be used
within the package itself in other methods'''