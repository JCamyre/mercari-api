'''This package contains modules with methods to access data from Mercari, a second-hand seller website'''
from .base import _process_soup, _get_soup, _get_url
from .gui import MyApp

def get_products(keywords, categories=None, conditions={'Like New', 'Good'}, sortby=None):
	print(keywords, categories, conditions, sortby)
	_process_soup(_get_soup(_get_url(keywords, categories=categories, conditions=conditions, sortby=sortby)))

def run_app():
	MyApp(method=get_products)

print('I hope you enjoy using this package.')

if __name__ == '__main__':
	pass

