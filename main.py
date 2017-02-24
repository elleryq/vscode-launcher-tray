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


class VSCodeTray(QSystemTrayIcon):
    """Visual Studio Code tray."""

    def __init__(self, icon, parent=None):
        """Constructor."""
        QSystemTrayIcon.__init__(self, icon, parent)

        self.config = Config()
        self.menu = None
        self._load_menu()

    def _add_project_in_menu(self, menu, project):
        """Add project in menu.

        Args:
            menu (QMenu): The QMenu instance.
            project (dict): The project, which is a dict, contains {'name': "", 'directory': ""}
        """
        action = menu.addAction(project['name'])
        action.triggered.connect(partial(
            self._launch_vscode, project['name'], project['directory']))
        action.setProperty("project_name", project['name'])
        action.setProperty("project_directory", project['directory'])
        action.setProperty("type", "dynamic")

    def _load_menu(self):
        """According to config to load menu."""
        if self.menu:
            self.menu.clear()

        menu = QMenu()
        addAction = menu.addAction(self.tr("Add"))
        addAction.triggered.connect(self._add)
        addAction = menu.addAction(self.tr("Manage"))
        addAction.triggered.connect(self._manage)

        menu.addSeparator()

        exitAction = menu.addAction(self.tr("Exit"))
        exitAction.triggered.connect(self._quit)

        menu.addSeparator()
        for project in self.config.get_projects():
            self._add_project_in_menu(menu, project)

        self.setContextMenu(menu)
        self.menu = menu

    def _enumerate_menu(self, menu):
        """Enumerate menu, for debug."""
        for action in menu.actions():
            if action.isSeparator():
                print("separator")
            elif action.menu():
                print("(submenu) action {}".format(action.text()))
                self.enumerate_menu(action.menu)
            else:
                print("action {}".format(action.text()))

    def _update_menu(self):
        """Update menu if project is not in menu."""

        # Add menu if project is not in menu
        config_projects = self.config.get_projects()
        for project in self.config.get_projects():
            if not self._find_project_in_menu(project):
                self._add_project_in_menu(self.menu, project)

        # Add action to delete list if project is not in config
        delete_list = []
        for action in self.menu.actions():
            if action.property("type") and action.property("type") == "dynamic":
                if not action.property("project_name"):
                    continue
                if not self.config.find_project(action.property("project_name")):
                    delete_list.append(action)

        # Remove actions in delete list
        for action in delete_list:
            self.menu.removeAction(action)

    def _find_project_in_menu(self, project):
        """Find project in menu.

        Args:
            project (dict): The project, which is a dict, contains {'name': "", 'directory': ""}
        Return:
            bool: If found, return True.
        """
        for action in self.menu.actions():
            if action.property("type") and action.property("type") == "dynamic":
                if not action.property("project_name"):
                    continue
                if not action.property("project_directory"):
                    continue
                if action.property("project_name") == project['name']:
                    return True
        return False

    def _add(self):
        name, directory, ok = ProjectDialog.getProjectNameAndDirectory()
        config_projects = self.config.get_projects()
        if ok:
            self._add_project_in_menu(self.menu, {
                "name": name,
                "directory": directory
            })
            found = next((x for x in config_projects if x['name'] == name), {})
            if not found:
                config_projects.append({"name": name, 'directory': directory})
            else:
                # TODO: Alert
                pass

    def _manage(self):
        """Launch manage dialog."""
        dirty, ok = ManageDialog.showManageDialog()
        if ok and dirty:
            self._update_menu()

    def _quit(self):
        """Quit."""
        self.config.save()
        QCoreApplication.instance().quit()

    def _launch_vscode(self, name, directory):
        """Launch Visual Studio Code in specified directory."""
        process = QProcess()
        process.startDetached("code", [directory])


def main():
    """Main entry."""
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    w = QWidget()
    trayIcon = VSCodeTray(QtGui.QIcon("code.png"),
                              w)

    trayIcon.show()
    rc = app.exec_()

    del trayIcon
    del w
    del app

    sys.exit(rc)


if __name__ == '__main__':
    main()
