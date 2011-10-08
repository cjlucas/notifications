#!/usr/bin/env python

from setuptools import setup
from notifications import __version__

setup(name="notifications",
      version=__version__,
      description="""Client for the iOS app "Notifications" (aka "Push 4.0").""",
      author="Thomas Jost",
      author_email="thomas.jost@gmail.com",
      url="https://github.com/cjlucas/notifications",
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
