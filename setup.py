#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os import path
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

setup(name='vscode-launcher-tray',
      version='0.2.0',
      description='A system tray tool to launch Visual Studio code quickly.',
      author='Yan-ren Tsai',
      author_email='elleryq@gmail.com',
      url='https://github.com/elleryq/vscode-launcher-tray',
      classifiers=[
          # How mature is this project? Common values are
          #   3 - Alpha
          #   4 - Beta
          #   5 - Production/Stable
          'Development Status :: 3 - Alpha',

          # Indicate who your project is intended for
          'Intended Audience :: Developers',
          'Topic :: Utilities',

          # Pick your license as you wish (should match"license"above)
          'License :: OSI Approved :: MIT License',

          # Specify the Python versions you support here. In particular, ensure
          # that you indicate whether you support Python 2, Python 3 or both.
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
      ],
      # What does your project relate to?
      keywords='tools',

      # You can just specify the packages manually here if your project is
      # simple. Or you can use find_packages().
      packages=find_packages(exclude=['contrib', 'docs', 'tests']),
      # install_requires=['PyQt5'],
      # List additional groups of dependencies here (e.g. development
      # dependencies). You can install these using the following syntax,
      # for example:
      # $ pip install -e .[dev,test]
      extras_require={
          'dev': ['check-manifest'],
          'test': ['coverage'],
      },
      # include_package_data=True,  # If use MANIFEST.in
      package_data={
          '': ['*.txt', '*.rst', '*.md'],
          # And include any *.msg files found in the 'hello' package, too:
          # 'hello': ['*.msg'],
          'vscode_launcher_tray': ['pixmaps/*.png', 'data/*.desktop'],
      },

      data_files=[
        ('share/applications', ['vscode_launcher_tray/data/vscode-launcher-tray.desktop']),
        ('share/pixmaps', ['vscode_launcher_tray/pixmaps/vscode-launcher-tray.png']),
      ],


      # To provide executable scripts, use entry points in preference to the
      # "scripts" keyword. Entry points provide cross-platform support and allow
      # pip to create the appropriate form of executable for the target platform.
      entry_points={
          'console_scripts': [
              'vscode-launcher-tray=vscode_launcher_tray:main',
          ],
      },
    )