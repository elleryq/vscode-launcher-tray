#!/usr/bin/env python3
import os
import sys
import json
import logging
from PyQt5 import QtGui, Qt
from PyQt5.QtWidgets import (
        QDialog, QWidget, QSystemTrayIcon, QMenu, QApplication,
        QPushButton, QLabel, QFrame, QFileDialog, QGridLayout,
        QLineEdit)
from PyQt5.QtCore import QCoreApplication


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
        except (FileNotFoundError, json.decoder.JSONDecodeError) as ex:
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
        self.addButton = QPushButton("Add")
        # self.addButton.clicked.connect(self.setExistingDirectory)
        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.clicked.connect(self.close)

        layout = QGridLayout()
        layout.setColumnStretch(1, 1)
        layout.setColumnMinimumWidth(1, 250)

        layout.addWidget(self.directoryButton, 0, 0)
        layout.addWidget(self.directoryLabel, 0, 1)
        layout.addWidget(self.projectNameLabel, 1, 0)
        layout.addWidget(self.projectNameLineEdit, 1, 1)
        layout.addWidget(self.addButton, 2, 0)
        layout.addWidget(self.cancelButton, 2, 1)

        self.setLayout(layout)

    def setExistingDirectory(self):
        options = QFileDialog.DontResolveSymlinks | QFileDialog.ShowDirsOnly
        directory = QFileDialog.getExistingDirectory(self,
                "QFileDialog.getExistingDirectory()",
                self.directoryLabel.text(), options=options)
        if directory:
            self.directoryLabel.setText(directory)

    def get_project_name_and_directory(self):
        # self.show
        pass

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
        self.project_dialog.show()

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
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
