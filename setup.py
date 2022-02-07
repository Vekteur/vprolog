# Standard library imports
from pathlib import Path
import re

# Third party imports
from setuptools import setup

# Not a robust solution to get the version, but is there a better way?
__version__ ,= re.findall("__version__: str = '(.*)'", open('vprolog/__init__.py').read())

# The directory containing this file
HERE = Path(__file__).resolve().parent

README = (HERE / 'README.md').read_text()

setup(
	name='vprolog',
	version=__version__,
	description='Incomplete Prolog interpreter in Python',
	long_description=README,
	long_description_content_type='text/markdown',
	url='https://github.com/Vekteur/vprolog',
	author='Victor Dheur',
	author_email='vic.dheur@gmail.com',
	license='MIT',
	classifiers=[
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python',
		'Programming Language :: Python :: 3',
	],
	packages=['vprolog'],
	include_package_data=True,
	install_requires=['lark>=1'],
	entry_points={'console_scripts': ['vprolog=vprolog.__main__:main']},
)