[![Build Status](https://travis-ci.org/elleryq/vscode-launcher-tray.svg?branch=master)](https://travis-ci.org/elleryq/vscode-launcher-tray)

# vscode-launcher-tray

A simple tray program to launch code in specified directory quickly.

## Requirement

```
sudo apt install python3-pyqt5 python3-xdg
```

## Installation

```
python3 setup.py install --record installed_files.txt
```

Or uninstall
```
cat installed_files.txt | xargs rm -f
```

## Local development or run without install

Requirements
```
sudo apt install python3-all python3-setuptools python3-stdeb python3-pyqt5 python3-xdg pyqt5-dev-tools qttools5-dev-tools t4-dev-tools
```

Run
```
PYTHONPATH=vscode_launcher_tray python3 -m vscode_launcher_tray
```

### Build debian package

Ubuntu 14.04
```
sudo apt install python3-pyqt5 python3-all python3-setuptools python3-pip
sudo pip install stdeb
python3 setup.py --command-packages=stdeb.command bdist_deb
sudo dpkg -i deb_dist/<generated_deb>
```

Ubuntu 16.04
```
sudo apt install python3-pyqt5 python3-all python3-stdeb python3-setuptools
python3 setup.py --command-packages=stdeb.command bdist_deb
sudo dpkg -i deb_dist/<generated_deb>
```
