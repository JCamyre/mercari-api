'''This package contains modules with methods to access data from Mercari, a second-hand seller website'''
from .base import _process_soup, _get_soup, _get_url
from .gui import MyApp, get_products

# Redo requirements.txt with pipenv
def run_app():
	MyApp()

print('I hope you enjoy using this package.')

if __name__ == '__main__':
	pass

