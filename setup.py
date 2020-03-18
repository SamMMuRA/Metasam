try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

with open("README") as f:
	long_description=f.read()

setup(name='metasam',
version='1.0',
description=long_description,
url='',
author='SamMMuRA',
license='Freeware',
zip_safe=False,
packages=['metasam'],
install_requires=['requests','pycurl','Scrapy','pyPdf','pandas','matplotlib','fpdf','unidecode','python-magic','pyfiglet'],
py_modules=['metasam/des','metasam/g_sitemap','metasam/meta','metasam/spider_sitemap'],
scripts=[],
entry_points={'console_scripts':['metasam_try = metasam.prueba:main'],},
classifiers=[
'Development Status:: Beta',
'Operating System::Linux',
])
