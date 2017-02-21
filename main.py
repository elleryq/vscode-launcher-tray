#!/usr/bin/env python3
import os
import sys
import json
import logging
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
        QDialog, QWidget, QSystemTrayIcon, QMenu, QApplication,
        QPushButton, QLabel, QFrame, QFileDialog, QGridLayout,
        QLineEdit, QDialogButtonBox, QVBoxLayout)
from PyQt5.QtCore import QCoreApplication

# Compat between Python 3.4 and Python 3.5
if not hasattr(json, 'JSONDecodeError'):
    json.JSONDecodeError = ValueError

logger = logging.getLogger(__name__)


class Config(dict):
    def __init__(self, json_config_file=None):
        if not json_config_file:
            json_config_file = os.path.join(
                os.path.expanduser("~/.config/"),
                "vscode-launcher-tray.json")
        self.json_config_file = json_config_file
        try:
            self.update(json.load(open(json_config_file)))
        except (FileNotFoundError, json.JSONDecodeError) as ex:
            logger.warning("{} not found.".format(json_config_file))

    def save(self):
        json.dump(self, open(self.json_config_file, "wt"))


class ProjectDialog(QDialog):


    def __init__(self, parent=None):
        super(ProjectDialog, self).__init__(parent)

        self.initUI()


    def initUI(self):
        self.setMinimumSize(200, 100)
        self.setWindowTitle("Dialog")

        frameStyle = QFrame.Sunken | QFrame.Panel

        self.directoryLabel = QLabel()
        self.directoryLabel.setFrameStyle(frameStyle)
        self.directoryButton = QPushButton("Open Project directory")
        self.directoryButton.clicked.connect(self.setExistingDirectory)
        self.projectNameLabel = QLabel()
        self.projectNameLabel.setText("Project name")
        self.projectNameLabel.setFrameStyle(frameStyle)
        self.projectNameLineEdit = QLineEdit()
        self.projectNameLineEdit.textChanged.connect(self.setName)

        layout = QVBoxLayout()

        widget = QWidget()
        gridlayout = QGridLayout()
        gridlayout.setColumnStretch(1, 1)
        gridlayout.setColumnMinimumWidth(1, 250)

        gridlayout.addWidget(self.directoryButton, 0, 0)
        gridlayout.addWidget(self.directoryLabel, 0, 1)
        gridlayout.addWidget(self.projectNameLabel, 1, 0)
        gridlayout.addWidget(self.projectNameLineEdit, 1, 1)
        widget.setLayout(gridlayout)

        layout.addWidget(widget)

        # OK and Cancel buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)

    def setExistingDirectory(self):
        options = QFileDialog.DontResolveSymlinks | QFileDialog.ShowDirsOnly
        directory = QFileDialog.getExistingDirectory(self,
                "QFileDialog.getExistingDirectory()",
                self.directoryLabel.text(), options=options)
        if directory:
            self.directoryLabel.setText(directory)
            self._directory = directory

    @property
    def directory(self):
        return self._directory

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    def setName(self, name):
        self._name = name

    @staticmethod
    def getProjectNameAndDirectory(parent=None):
        dialog = ProjectDialog(parent)
        result = dialog.exec_()

        directory = dialog.directory
        return (dialog.name, dialog.directory, result == QDialog.Accepted)

class VSCodeTrayIcon(QSystemTrayIcon):

    def __init__(self, icon, config=None, parent=None):
        QSystemTrayIcon.__init__(self, icon, parent)

        self.config = config
        self.project_dialog = ProjectDialog(parent)

        menu = QMenu(parent)
        addAction = menu.addAction("Add")
        addAction.triggered.connect(self._add)
        menu.addSeparator()
        exitAction = menu.addAction("Exit")
        exitAction.triggered.connect(self._quit)
        self.setContextMenu(menu)

    def _add(self):
        print("add")
        name, directory, ok = ProjectDialog.getProjectNameAndDirectory()
        if ok:
            print("name={}".format(name))
            print("directory={}".format(directory))
        else:
            print("cancel")

    def _quit(self):
        self.config.save()
        QCoreApplication.instance().quit()


def main():
    config = Config()

    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    w = QWidget()
    trayIcon = VSCodeTrayIcon(QtGui.QIcon("logviewer.svg"),
                              config,
                              w)

    trayIcon.show()
    rc = app.exec_()

    del trayIcon
    del w
    del app

    sys.exit(rc)


if __name__ == '__main__':
    main()
