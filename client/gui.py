from PyQt6.QtWidgets import (
    QVBoxLayout,
    QWidget,
    QApplication,
    QTabWidget,
    )
from PyQt6.QtGui import QKeySequence, QShortcut, QFont

import sys
import qdarktheme

from widgets import Info, Table, Tree, TableModel
from model import Item
from form import CustomForm
from editor_db import Editor


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Таргет")
        self.vbox = QVBoxLayout()
        self.setLayout(self.vbox)
        self.vbox.setContentsMargins(0, 0, 0, 0)
        self.tabs = QTabWidget()
        self.vbox.addWidget(self.tabs, stretch=10)
        self.tabs.currentChanged.connect(self.reload_tab)

        
        editor = Editor()
        self.tabs.addTab(editor, 'Editor')

        # info = Info('measure')
        # measure = Item('measure')
        # err = measure.get(1)
        # if not err:
        #     info.set_value(measure.value)
        # self.tabs.addTab(info, 'Одиниця виміру')

        # mes_tbl_model = TableModel('measure')
        # mes_tbl = Table(mes_tbl_model)
        # err = measure.get_all()
        # if not err:
        #     mes_tbl.set_values(measure.values)
        # self.tabs.addTab(mes_tbl, 'Одиниці виміру')

        # mg_form = CustomForm('material_group')
        # mg = Item('material_group')
        # err = mg.get(3)
        # if not err:
        #     mg_form.set_value(mg.value)
        # self.tabs.addTab(mg_form, 'Форма Група матеріалів')

       
        # mg_table = Table(TableModel('material_group'))
        # err = mg.get_all()
        # if not err:
        #     mg_table.set_values(mg.values)
        # self.tabs.addTab(mg_table, 'Група матеріалів')

        # mg_tree = Tree('material_group')
        # mg_tree.set_values(mg.values)
        # self.tabs.addTab(mg_tree, 'Група матеріалів')

        # mg_info = Info('material_group')
        # mg1 = Item('material_group')
        # err = mg1.get(3)
        # if not err:
        #     mg_info.set_value(mg1.value)
        # self.tabs.addTab(mg_info, 'Група матеріалів')


    def reload_tab(self, index):
        w = self.tabs.widget(index)
        w.reload_widget()
    

class MainWindow():
    def __init__(self):
        self.qt_app = QApplication(sys.argv)
        self.window = Window()
        color = "#99BCBC"
        qss = """
        QToolTip {
            background-color: black;
            color: white;
            border: black solid 1px
                }
        """
        qdarktheme.setup_theme(custom_colors={'primary': color}, additional_qss=qss)
        font = QFont()
        QApplication.instance().setFont(font)
        font.setPointSize(10)

    def run(self):
        self.window.show()
        sys.exit(self.qt_app.exec())
