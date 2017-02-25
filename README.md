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