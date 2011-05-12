from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='musicob',
      version=version,
      description="Utility for serializing and notating music.",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='music notation lilypond',
      author='Jonathan Marmor',
      author_email='jmarmor@gmail.com',
      url='',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
