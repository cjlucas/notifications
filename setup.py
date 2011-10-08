#!/usr/bin/env python

from setuptools import setup
from notifications import __version__

setup(name="notifications",
      version=__version__,
      description="Client for the iPhone/iPod Touch `Notifications' app",
      author="Thomas Jost",
      author_email="thomas.jost@gmail.com",
      url="http://code.schnouki.net/p/notifications/",
      license="ISC",
      py_modules=['notifications'],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Communications',
          'Topic :: Internet :: WWW/HTTP',
      ]
)
