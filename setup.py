__author__ = 'bite'

requires = ['urllib2']

try:
    from setuptools import setup
    kw = {'zip_safe': False, 'install_requires': requires}
except ImportError:
    from distutils import setup
    kw = {'requires': requires}


setup(name='StoryStream SkyNet',
      version='0.1',
      author='Bite Studio',
      description='Library for accessing the StoryStream API',
      packages=['storystream-skynet'],
      **kw)