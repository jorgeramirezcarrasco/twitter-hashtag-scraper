from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(

    name='twitter-hashtag-scraper',
    version='1.0.0', 
    description='Unofficial Twitter Hashtag Scraper using free proxies', 
    long_description=long_description, 
    url='https://github.com/jramirezc93/twitter-hashtag-scraper',  
    author='Jorge Ramírez Carrasco',
    keywords='twitter, web scraping',
    python_requires='>=3.6, <4',
    install_requires=[
                    'beautifulsoup4>=4.9.1',
                    'bs4>=0.0.1',
                    'certifi>=2020.6.20',
                    'chardet>=3.0.4',
                    'idna>=2.10',
                    'lxml>=4.5.2',
                    'numpy>=1.19.1',
                    'pandas>=1.1.0',
                    'python-dateutil>=2.8.1',
                    'pytz>=2020.1',
                    'requests>=2.24.0',
                    'six>=1.15.0',
                    'soupsieve>=2.0.1',
                    'urllib3>=1.25.10'
                    ]
)