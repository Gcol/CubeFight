#!/usr/bin/env python
import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
requires = []
with open(os.path.join(here, 'requirement.txt')) as f:
      for line in f:
            requires.append(line.strip())

setup(
      name='WebSocketTest',
      version='1.0',
      description='First Project Test for web socket connection',
      author='CubeFght',
      author_email='CubeFghtRoyal@gmail.com',
      install_requires = requires
)