#!/usr/bin/env python

from setuptools import setup

version = '0.1'

setup(
   name='musicob',
   version=version,
   description="Utility for serializing and notating music.",
   keywords='music notation lilypond',
   author='Jonathan Marmor',
   author_email='jmarmor@gmail.com',
   zip_safe=False,
   install_requires=['PyYaml'],
   packages = ['musicob']
   )
