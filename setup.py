#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from os import path, makedirs
import subprocess
import glob
from setuptools import setup, find_packages
from distutils.dep_util import newer
from distutils.command.build import build
from distutils.log import warn, info, error

here = path.abspath(path.dirname(__file__))


class BuildData(build):
    def run (self):
        super().run()

        for ts in glob.glob(path.join("i18n", '*.ts')):
            lang = path.basename(ts[:-3])
            qm = path.join(
                "vscode_launcher_tray",
                "translations",
                "{}.qm".format(lang))

            directory = path.dirname(qm)
            if not path.exists(directory):
                info('creating %s' % directory)
                makedirs(directory)

            if newer(ts, qm):
                info('compiling {ts} -> {qm}'.format(ts=ts, qm=qm))
                try:
                    rc = subprocess.call(['lrelease', '-qm', qm, ts])
                    if rc != 0:
                        raise Warning("msgfmt returned {}".format(rc))
                except Exception as e:
                    error("Error: %s" % str(e))
                    sys.exit(1)


setup(name='vscode-launcher-tray',
      version='0.3.8',
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
          'vscode_launcher_tray': ['pixmaps/*.png', 'data/*.desktop', 'translations/*.qm'],
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
      cmdclass={
        'build': BuildData, 
      }
    )
