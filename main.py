#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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
from vscode_launcher_tray import (
    Config, ProjectDialog, ManageDialog)

logger = logging.getLogger(__name__)


class VSCodeTrayIcon(QSystemTrayIcon):

    def __init__(self, icon, config=None, parent=None):
        QSystemTrayIcon.__init__(self, icon, parent)

        self.config = config
        self.project_dialog = ProjectDialog(parent)

        menu = QMenu(parent)
        addAction = menu.addAction(self.tr("Add"))
        addAction.triggered.connect(self._add)
        addAction = menu.addAction(self.tr("Manage"))
        addAction.triggered.connect(self._manage)

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

    def _manage(self):
        ok = ManageDialog.showManageDialog()

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
    trayIcon = VSCodeTrayIcon(QtGui.QIcon("code.png"),
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
