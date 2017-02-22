# -*- coding: utf-8 -*-
import logging
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
        QWidget, QTableView,
        QDialog, QLabel, QFrame, QFileDialog, QGridLayout,
        QPushButton, QLineEdit, QDialogButtonBox,
        QHBoxLayout, QVBoxLayout)


logger = logging.getLogger(__name__)


class ManageDialog(QDialog):

    def __init__(self, parent=None):
        """Constructor."""
        super(ManageDialog, self).__init__(parent)

        self.initUI()

    def initUI(self):
        """Initialize UI."""
        self.setMinimumSize(200, 100)
        self.setWindowTitle(self.tr("Manage"))

        frameStyle = QFrame.Sunken | QFrame.Panel

        # TableView for displaying all projects
        self.tableView = QTableView()
        self.tableView.resizeColumnsToContents()

        # Right side buttons for add/edit/delete items in left tableview
        self.addButton = QPushButton(self.tr("Add"))
        # self.addButton.clicked.connect(self.setExistingDirectory)
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

    @staticmethod
    def showManageDialog(parent=None):
        dialog = ManageDialog(parent)
        result = dialog.exec_()
        return result == QDialog.Accepted