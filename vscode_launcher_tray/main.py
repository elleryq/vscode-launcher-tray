#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
vscode_launcher_tray.
"""
import os
import sys
import logging
import signal
import shutil
from functools import partial
from PyQt5 import QtGui
from PyQt5.QtCore import QProcess, QTranslator, QLocale, QLibraryInfo, Qt
from PyQt5.QtWidgets import (
    QWidget, QSystemTrayIcon, QMenu,
    QApplication, QMessageBox)
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
        manageAction = menu.addAction(self.tr("Manage"))
        manageAction.triggered.connect(self._manage)
        aboutAction = menu.addAction(self.tr("About"))
        aboutAction.triggered.connect(self._about)

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
        for project in config_projects:
            if not self._find_project_in_menu(project):
                self._add_project_in_menu(self.menu, project)

        # Add action to delete list if project is not in config
        delete_list = []
        for action in self.menu.actions():
            if action.property("type") and action.property("type") == "dynamic":
                if not action.property("project_name"):
                    continue
                if not self.config.is_project_existed(
                        action.property("project_name")):
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

    def _manage(self):
        """Launch manage dialog."""
        dirty, ok = ManageDialog.showManageDialog()
        if ok and dirty:
            self._update_menu()

    def _about(self):
        """Launch about dialog."""
        QMessageBox.about(None, "vscode-launcher-tray", """vscode-launcher-tray

Homepage: https://github.com/elleryq/vscode-launcher-tray
Author: Yan-ren Tsai""")

    def _quit(self):
        """Quit."""
        self.config.save()
        QCoreApplication.instance().quit()

    def _launch_vscode(self, name, directory):
        """Launch Visual Studio Code in specified directory."""
        process = QProcess()
        vscode_path = shutil.which("code")
        if vscode_path:
            process.startDetached(
                vscode_path, [], directory)
        else:
            QMessageBox.information(
                self,
                "Information",
                "You need to install Visual Studio Code.",
                QMessageBox.Ok)


def main():
    """Main entry."""
    # Accept ctrl-c
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    app = QApplication(sys.argv)

    # i18n
    translator = QTranslator()
    translator.load("qt_" + QLocale.system().name(),
            QLibraryInfo.location(QLibraryInfo.TranslationsPath))
    app.installTranslator(translator);

    app_translator = QTranslator()
    app_translator.load(
        QLocale.system().name(),
        os.path.join(
            os.path.dirname(__file__),
            "translations"))
    app.installTranslator(app_translator)

    # Don't quit on last window closed
    app.setQuitOnLastWindowClosed(False)

    pixmaps_dir = os.path.join(
        os.path.dirname(__file__),
        "pixmaps"
    )
    pixmap = os.path.join(pixmaps_dir, "vscode-launcher-tray.png")

    w = QWidget()
    trayIcon = VSCodeTray(QtGui.QIcon(pixmap), w)

    trayIcon.show()
    rc = app.exec_()

    del trayIcon
    del w
    del app

    sys.exit(rc)
