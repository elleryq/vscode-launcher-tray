#!/usr/bin/env python3
import sys
import logging
from functools import partial
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QProcess
from PyQt5.QtWidgets import (
        QDialog, QWidget, QSystemTrayIcon, QMenu, QApplication,
        QPushButton, QLabel, QFrame, QFileDialog, QGridLayout,
        QLineEdit, QDialogButtonBox, QVBoxLayout)
from PyQt5.QtCore import QCoreApplication
from vscode_launcher_tray import Config

logger = logging.getLogger(__name__)


class ProjectDialog(QDialog):

    def __init__(self, parent=None):
        """Constructor."""
        super(ProjectDialog, self).__init__(parent)

        self.initUI()

    def initUI(self):
        """Initialize UI."""
        self.setMinimumSize(200, 100)
        self.setWindowTitle(self.tr("Manage"))

        frameStyle = QFrame.Sunken | QFrame.Panel

        self.directoryLabel = QLabel()
        self.directoryLabel.setFrameStyle(frameStyle)
        self.directoryButton = QPushButton(self.tr("Open Project directory"))
        self.directoryButton.clicked.connect(self.setExistingDirectory)
        self.projectNameLabel = QLabel()
        self.projectNameLabel.setText(self.tr("Project name"))
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
                self.tr("Open project directory"),
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
        addAction = menu.addAction(self.tr("Manage"))
        addAction.triggered.connect(self._add)

        menu.addSeparator()

        exitAction = menu.addAction(self.tr("Exit"))
        exitAction.triggered.connect(self._quit)

        menu.addSeparator()
        for project in self._get_projects_from_config():
            action = menu.addAction(project['name'])
            action.triggered.connect(partial(
                self._launch_vscode, project['name'], project['directory']))

        self.setContextMenu(menu)
        self.menu = menu

    def _get_projects_from_config(self):
        if 'projects' not in self.config:
            self.config['projects'] = []
        return self.config['projects']

    def _add(self):
        print("add")
        name, directory, ok = ProjectDialog.getProjectNameAndDirectory()
        config_projects = self._get_projects_from_config()
        if ok:
            action = self.menu.addAction(name)
            action.triggered.connect(partial(
                self._launch_vscode, name, directory))
            found = next((x for x in config_projects if x['name'] == name), {})
            if not found:
                config_projects.append({"name": name, 'directory': directory})
            else:
                # TODO: Alert
                pass

    def _quit(self):
        self.config.save()
        QCoreApplication.instance().quit()

    def _launch_vscode(self, name, directory):
        process = QProcess()
        process.startDetached("code", [directory])


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
