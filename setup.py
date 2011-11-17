#!/usr/bin/env python

import sys
from setuptools import setup
from notifications import __version__

_py3 = sys.version_info > (3,)

required_pkgs = []
if not _py3: required_pkgs.append("simplejson")

setup(name="notifications",
      version=__version__,
      description="""Client for the iOS app "Notifications" (aka "Push 4.0").""",
      author="Thomas Jost",
      author_email="thomas.jost@gmail.com",
      maintainer="Chris Lucas",
      maintainer_email="chris@chrisjlucas.com",
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
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
          'Topic :: Communications',
          'Topic :: Internet :: WWW/HTTP',
      ],
      install_requires=required_pkgs,
)
