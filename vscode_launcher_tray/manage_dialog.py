# -*- coding: utf-8 -*-
import logging
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
        QWidget, QTableView,
        QDialog, QLabel, QFrame, QFileDialog, QGridLayout,
        QPushButton, QLineEdit, QDialogButtonBox,
        QHBoxLayout, QVBoxLayout)
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from .project_dialog import ProjectDialog
from .config import Config


logger = logging.getLogger(__name__)


class ManageDialog(QDialog):

    def __init__(self, parent=None):
        """Constructor."""
        super(ManageDialog, self).__init__(parent)
        self.config = Config()

        self.initUI()

    def initUI(self):
        """Initialize UI."""
        self.setMinimumSize(640, 480)
        self.setWindowTitle(self.tr("Manage"))

        frameStyle = QFrame.Sunken | QFrame.Panel

        # TableView for displaying all projects
        self.tableView = QTableView()

        # TableView model
        model = QStandardItemModel(self.tableView)
        model.setColumnCount(2)
        headerNames = ["Name", "Directory"]
        model.setHorizontalHeaderLabels(headerNames)

        # Load data into model
        for project in self.config.get_projects():
            model.appendRow([
                QStandardItem(project['name']),
                QStandardItem(project['directory'])])
        self.tableView.setModel(model)
        self.tableView.resizeColumnsToContents()

        # Right side buttons for add/edit/delete items in left tableview
        self.addButton = QPushButton(self.tr("Add"))
        self.addButton.clicked.connect(self._add)
        self.deleteButton = QPushButton(self.tr("Delete"))
        self.editButton = QPushButton(self.tr("Edit"))

        button_group_layout = QVBoxLayout()
        button_group_layout.addWidget(self.addButton)
        button_group_layout.addWidget(self.deleteButton)
        button_group_layout.addWidget(self.editButton)

        widget = QWidget()
        widget.setLayout(button_group_layout)

        # OK and Cancel buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        # Add them together
        # Upper widget contains a tableview in left side, buttons in right side
        # Bottom widget contains OK/Cancel
        major_layout = QHBoxLayout()
        major_layout.addWidget(self.tableView)
        major_layout.addWidget(widget)
        layout = QVBoxLayout()
        widget = QWidget()
        widget.setLayout(major_layout)
        layout.addWidget(widget)
        layout.addWidget(buttons)

        self.setLayout(layout)

    def _add(self):
        name, directory, ok = ProjectDialog.getProjectNameAndDirectory()
        # config_projects = self._get_projects_from_config()
        if ok:
            pass
            # action = self.menu.addAction(name)
            # action.triggered.connect(partial(
            #     self._launch_vscode, name, directory))
            # found = next((x for x in config_projects if x['name'] == name), {})
            # if not found:
            #     config_projects.append({"name": name, 'directory': directory})
            # else:
            #     TODO: Alert
            #    pass

    @staticmethod
    def showManageDialog(parent=None):
        dialog = ManageDialog(parent)
        result = dialog.exec_()
        return result == QDialog.Accepted