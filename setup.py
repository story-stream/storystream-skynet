__author__ = 'Rich @ StoryStream'

try:
    from setuptools import setup
    kw = {'zip_safe': False, 'install_requires': []}
except ImportError:
    from distutils import setup
    kw = {'requires': []}


setup(name='StoryStream SkyNet',
      version='0.3',
      author='Bite Studio',
      description='Library for accessing the StoryStream API',
      packages=['storystream_skynet'],
      **kw)