# -*- coding: utf-8 -*-

import json
from datetime import datetime
from widgets import (
    ProtoWidget,
    Info,
    DTable,
    TableModel,
    Tree,
    prepare_value_to_str,
    ComboBoxDictSelector,
)

from form import CustomForm, CustomDialog

from PyQt6.QtCore import (
    Qt,
    QDate,
    pyqtSignal,
    QEvent,
    QModelIndex,
    )
from PyQt6.QtGui import QStandardItemModel, QStandardItem, QKeyEvent
from PyQt6.QtWidgets import (
    QLabel,
    QPushButton,
    QWidget,
    QLineEdit,
    QTextEdit,
    QCheckBox,
    QSpinBox,
    QDoubleSpinBox,
    QVBoxLayout,
    QHBoxLayout,
    QCalendarWidget,
    QSplitter,
    QApplication,
    QGridLayout,
    QTabWidget,
    QTableView,
    QHeaderView,
    QAbstractItemView,
    QTreeWidget,
    QTreeWidgetItem,
    )

from dialogs import error, askdlg, CustomDialog
from model import Item

class Editor(QWidget, ProtoWidget):
    def __init__(self):
        super().__init__()
        self.current_model = ''
        self.vbox = QVBoxLayout()
        self.setLayout(self.vbox)
        self.vbox.setContentsMargins(0, 0, 0, 0)
        controls = QWidget()
        self.vbox.addWidget(controls, 1)
        
        self.hbox = QHBoxLayout()
        self.hbox.setContentsMargins(0, 0, 0, 0)
        controls.setLayout(self.hbox)
        create_btn = QPushButton('Створити')
        self.hbox.addWidget(create_btn)
        create_btn.clicked.connect(self.create_model)
        self.hbox.addWidget(create_btn)
        create_field_btn = QPushButton('Додати поле')
        self.hbox.addWidget(create_field_btn)
        create_field_btn.clicked.connect(self.create_field)
        create_key_btn = QPushButton('Додати ключ')
        self.hbox.addWidget(create_key_btn)
        create_field_btn.clicked.connect(self.create_key)
        self.hbox.addStretch()
        
        split = QSplitter(Qt.Orientation.Horizontal)
        self.vbox.addWidget(split, 10)
        
        self.field_type_tab = DTable(TableModel('s_field_type'))
        split.addWidget(self.field_type_tab)
        
        ft = Item('s_field_type')
        err = ft.get_all()
        if not err:
            self.field_type_tab.set_values(ft.values)
        
        self.category_table = DTable(TableModel('s_category'))
        split.addWidget(self.category_table)
        self.category_table.reload()
        self.category_table.actionInvoked.connect(self.category_action)
        
        self.models_tab = DTable(TableModel('s_model'))
        split.addWidget(self.models_tab)
        self.models_tab.reload()
        
        self.fields_table = DTable(TableModel('s_field'))
        split.addWidget(self.fields_table)
        self.fields_table.reload()

    def category_action(self, action:str, category: dict):
        if action == 'create':
            form = CustomForm('s_category')
            form.hide_save_btn()
            dlg = CustomDialog(widget=form, title='Створити')
            res = dlg.exec()
            if res:
                category_item = Item('s_category')
                form.get_value()
                category_item.value = form.value
                err = category_item.create()
                if err:
                    error(err)
                    return
            self.category_table.reload()

    def create_model(self):
        form = CustomForm('s_model')
        form.hide_save_btn()
        dlg = CustomDialog(widget=form, title='Створити')
        res = dlg.exec()
        if res:
            print('Creating...')

    def create_field(self):
        pass
    
    def create_key(self):
        pass