
from setuptools import setup


setup(name='pyshortcuts',
      version='1.0',
      description='Python Helper Utilities',
      author='Kyle A Gearhart',
      author_email='kagearhart@gmail.com',
      license='GPLv3',
      packages=['pyshortcuts', 'pyshortcuts.cl', 'pyshortcuts.csv', 'pyshortcuts.db', 'pyshortcuts.joblog'],
      install_requires=['pymysql', 'sshtunnel'])