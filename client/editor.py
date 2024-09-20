# -*- coding: utf-8 -*-

import json
from datetime import datetime
from widgets import (
    ProtoWidget,
    Info,
    Table,
    Tree,
    prepare_value_to_str,
    ComboBoxDictSelector,
)

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


ID_ROLE = 100
SORT_ROLE = 101

field_types = {
    "id": {"hum": "Ключ", "def": 0},
    "_id": {"hum": "Посилання", "def": 0},
    "int": {"hum": "Ціле число", "def": 0},
    "float": {"hum": "Число", "def": 0.0},
    "str": {"hum": "Строка", "def": ""},
    "bool": {"hum": "Так/Ні", "def": True},
    "date": {"hum": "Дата", "def": ''},
}
            

class EdProtoWidget(ProtoWidget):
    def get_categories(self):
        return set(v['category'] for v in self.app_model.values())
    
    def get_top_headers(self):
        return [v['hum'] for v in self.hum.values()]
    
    def get_models_by_category(self, category_name: str):
        return {k: v for k, v in self.app_model.items() if v['category'] == category_name}
    
    def get_headers_by_category(self, category_name: str):
        keys = [k for k, v in self.app_model.items() if v['category'] == category_name]
        return {k: self.hum[k] for k in keys}

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
        
        self.category_tabs = EdCategoriesTabs()
        split.addWidget(self.category_tabs)
        self.category_tabs.itemSelected.connect(self.item_selected)
        self.category_tabs.currentChanged.connect(self.category_changed)
        self.category_table = Table(TableJsonModel())
        split.addWidget(self.category_table)

    def item_selected(self, model_name):
        self.current_model = model_name
        self.category_table.set_values(model_name)

    def category_changed(self, index):
        self.category_table.clear()
        
    def create_field(self):
        w = QWidget()
        grid = QGridLayout()
        w.setLayout(grid)
        grid.setContentsMargins(0, 0, 0, 0)
        self.name_widget = QLineEdit()
        self.title_widget = QLineEdit()
        self.type_widget = ComboBoxDictSelector(values=field_types, title_key='hum')
        self.def_widget = QLineEdit()
        grid.addWidget(QLabel('Поле'), 0, 0)
        grid.addWidget(self.name_widget, 0, 1)
        grid.addWidget(QLabel('Назва'), 1, 0)
        grid.addWidget(self.title_widget, 1, 1)
        grid.addWidget(QLabel('Тип'), 2, 0)
        grid.addWidget(self.type_widget, 2, 1)
        grid.addWidget(QLabel('За замовчуванням'), 3, 0)
        grid.addWidget(self.def_widget, 3, 1)
        m = self.hum[self.current_model]['hum']
        dlg = CustomDialog(w, f'{m} - додати поле')
        res = dlg.exec()
        if res:
            t = self.type_widget.value()
            d = self.def_widget.text()
            if t == "id": d = 0
            elif t == "_id": d = 0
            elif t == "int": d = int(d)
            elif t == "float": d = float(d)
            elif t == "bool": d = bool(d)
            elif t == "date": d = ''
            
            m = self.app_model[self.current_model]
            m['fields'][self.name_widget.text()] = {
                'type': t,
                'def': d,
            }
            super().app_model[self.current_model] = m
            h = self.hum[self.current_model]
            h['fields'][self.name_widget.text()] = {'hum': self.title_widget.text()}
            super().hum[self.current_model] = h
            with open ('model.json', "w") as f:
                f.write(json.dumps(self.app_model))

            with open ('hum.json', "w") as f:
                f.write(json.dumps(self.hum))

    def create_key(self):
        w = QWidget()
        grid = QGridLayout()
        w.setLayout(grid)
        grid.setContentsMargins(0, 0, 0, 0)
        self.name_widget = QLabel()
        self.title_widget = QLineEdit()
        self.type_widget = ComboBoxDictSelector(values=field_types, title_key='hum')
        self.def_widget = QLineEdit()
        grid.addWidget(QLabel('Поле'), 0, 0)
        grid.addWidget(self.name_widget, 0, 1)
        grid.addWidget(QLabel('Назва'), 1, 0)
        grid.addWidget(self.title_widget, 1, 1)
        grid.addWidget(QLabel('Тип'), 2, 0)
        grid.addWidget(self.type_widget, 2, 1)
        grid.addWidget(QLabel('За замовчуванням'), 3, 0)
        grid.addWidget(self.def_widget, 3, 1)
        m = self.hum[self.current_model]['hum']
        dlg = CustomDialog(w, f'{m} - додати поле')
        res = dlg.exec()
        if res:
            t = self.type_widget.value()
            d = self.def_widget.text()
            if t == "id": d = 0
            elif t == "_id": d = 0
            elif t == "int": d = int(d)
            elif t == "float": d = float(d)
            elif t == "bool": d = bool(d)
            elif t == "date": d = ''
            
            m = self.app_model[self.current_model]
            m['fields'][self.name_widget.text()] = {
                'type': t,
                'def': d,
            }
            super().app_model[self.current_model] = m
            h = self.hum[self.current_model]
            h['fields'][self.name_widget.text()] = {'hum': self.title_widget.text()}
            super().hum[self.current_model] = h
            with open ('model.json', "w") as f:
                f.write(json.dumps(self.app_model))

            with open ('hum.json', "w") as f:
                f.write(json.dumps(self.hum))
    
    def create_model(self):
        c = self.category_tabs.current_category
        name = askdlg('Вкажіть назву')
        hum = askdlg('Вкажіть заголовок')
        new_model = {
                        "category": c,
                        "fields": {
                            "id": {"type": "id", "def": 0},
                            "name": {"type": "str", "def": ""},
                            "is_active": {"type": "bool", "def": True}
                        },
                        "childern": []
                    }
        super().app_model[name] = new_model
        new_hum = {
            "hum": hum,
            "fields": {
                "id": {"hum": "Номер"},
                "name": {"hum": "Назва"},
                "is_active": {"hum": "Діючий"}
            }
        } 
        super().hum[name] = new_hum
        self.category_tabs.reload()
        with open ('model.json', "w") as f:
            f.write(json.dumps(self.app_model))

        with open ('hum.json', "w") as f:
            f.write(json.dumps(self.hum))
                    

class EdCategoriesTabs(QTabWidget, EdProtoWidget):
    itemSelected = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.current_category = list(self.hum['categories'].keys())[0]
        self.setTabPosition(QTabWidget.TabPosition.West)
        for c in self.hum['categories'].keys():
            tree = EdCategoryTree(c)
            tree.itemSelected.connect(self.item_selected)
            self.addTab(tree, self.hum['categories'][c])
        self.currentChanged.connect(self.current_changed)

    def item_selected(self, model_name: str):
        self.itemSelected.emit(model_name)

    def current_changed(self, index: int) -> None:
        self.current_category = list(self.hum['categories'].keys())[index]
        self.currentWidget().reload()

    def reload(self):
        self.currentWidget().reload()

class EdCategoryTree(QTreeWidget, EdProtoWidget):
    itemSelected = pyqtSignal(str)
    def __init__(self, category_name: str):
        super().__init__()
        self.name = category_name
        # self.models = self.get_models_by_category(self.name)
        self.headers = self.get_headers_by_category(self.name)

        self.setColumnCount(1)
        self.setHeaderLabels(('Назва',))
        header = self.header()
        header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.currentItemChanged.connect(self.cur_changed)
        # self.itemClicked.connect(self.cur_changed)
        # self.itemDoubleClicked.connect(self.value_dblclicked)
        self.reload()

    def reload(self):
        self.headers = self.get_headers_by_category(self.name)
        self.clear()
        self.dataset = {}
        if not self.headers:
            return
        parent_item = self.invisibleRootItem()
        for k, v in self.headers.items():
            data_item = QTreeWidgetItem()
            data_item.setText(0, v['hum'])
            data_item.setData(0, ID_ROLE, k)
            parent_item.addChild(data_item)

    def cur_changed(self, current, previous):
    # def cur_changed(self, item, column):
        if not current: # or current == previous:
            return
        model_name = current.data(0, ID_ROLE)
        self.itemSelected.emit(model_name)


# data format

class TableJsonModel(QStandardItemModel, EdProtoWidget):
    def __init__(self):
        super().__init__()
        self.headers = ("Поле", "Назва", "Тип", "За замовчуванням")
        self.setHorizontalHeaderLabels(self.headers)
        self.setSortRole(SORT_ROLE)
        self.current = ''

    def set_values(self, model_name):
        self.clear()
        self.current = model_name
        values = self.app_model[model_name]['fields']
        self.setHorizontalHeaderLabels(self.headers)
        for k, v in values.items():
            row = [
               QStandardItem(k),
               QStandardItem(self.hum[model_name]['fields'][k]['hum']),
               QStandardItem(field_types[v['type']]['hum']),
               QStandardItem(str(v['def'])), 
            ]
            row[0].setData(k, ID_ROLE)
            self.appendRow(row)

    # def make_item(self, value, field):
    #     fields = self.get_fields()
    #     default = fields[field]['def'] if field in fields else ''
    #     txt = prepare_value_to_str(default, value)
    #     item = QStandardItem(txt)
    #     item.setData(value, SORT_ROLE)
    #     item.setEditable(False)
    #     return item
    
    def get_row_value(self, row):
        print(self.current, self.item(row).text())
        return {'model': self.current, 'field': self.item(row).text()}
