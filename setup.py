# -*- coding: utf-8 -*-

from setuptools import find_packages
from setuptools import setup

import os

version = '0.1'
description = "Coloreemos entre todos!."
long_description = (
    open("README.md").read() + "\n" +
    open(os.path.join("docs", "CREDITS.rst")).read() + "\n" +
    open(os.path.join("docs", "HISTORY.rst")).read()
)

setup(name='coloreando',
      version=version,
      description=description,
      long_description=long_description,
      classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: System Administrators",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Ezequiel Pochiero',
      author_email='epochiero@gmail.com',
      url='https://github.com/epochiero/coloreando',
      license='',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=[],
      include_package_data=True,
      zip_safe=False,
      dependency_links = [
          'https://github.com/abourget/gevent-socketio/archive/aeece7038b0052ddf6b4228857e4d7a67a6242f2.zip#egg=gevent-socketio'
        ],
      install_requires=[
          'Django==1.5.1',
          'Fabric==1.6.1',
          'gevent==0.13.8',
          'gevent-websocket==0.3.6',
          'gevent-socketio',
          'greenlet==0.4.1',
          'gunicorn==17.5',
          'redis==2.7.6',
          'simplejson==3.3.0',
          'wsgiref==0.1.2',
          'pysqlite',
          'honcho==0.4.2'
        ],
      extras_require={
        'test': [
          ],
        },
      )
