from requests import get 
from bs4 import BeautifulSoup
import json 

base_url = 'https://www.mercari.com/search/'

# have a way to display all of the category choices by printing the dict
categoryIds = {'Women': 1, 'Men': 2, 
'Electronics': {'Computers & Laptops': {'Laptops & netbooks': 771, 'Desktops & all-in-ones': 772}}}

conditionIds = {'New': 1, 'Like New': 2, 'Good': 3}

def search_product(keywords, conditions=None, category=None, sortby=None):
	url = base_url + '?'
	keywords = keywords.split()
	keywords = '%20'.join(keywords)
	keywords_url = f'keyword={keywords}'
	url += keywords_url + '&'
	if category: 
		category_path = category.split('/')
		yo = categoryIds
		for category in category_path:
			yo = yo[category]
		print(yo)
		category_url = f'categoryIds={yo}'
		url += category_url + '&'

	if conditions:
		conditions = conditions.split(', ')
		conditions = [str(conditionIds[condition]) for condition in conditions]
		conditions = '-'.join(conditions)
		conditions_url = f'itemConditions={conditions}'
		url += conditions_url

	return url

url = search_product('gaming laptop', conditions='Like New, Good', category='Electronics/Computers & Laptops/Laptops & netbooks')
request = get(url)
soup = BeautifulSoup(request, 'lxml')
print(request.json())