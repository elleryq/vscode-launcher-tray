# vscode-launcher-tray

A simple tray program to launch code in specified directory quickly.

## Requirement

```
sudo apt install python3-pyqt5
```

## Local development or run without install

```
PYTHONPATH=vscode_launcher_tray python3 -m vscode_launcher_tray
```

## Installation

```
python3 setup.py install --record installed_files.txt
```

Or uninstall
```
cat installed_files.txt | xargs rm -f
```

## Build debian package

Ubuntu 16.04
```
sudo apt install python3-pyqt5 python3-all python3-stdeb
python3 setup.py bdist_deb
sudo dpkg -i deb_dist/<generated_deb>
```
