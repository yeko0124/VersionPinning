import hou
import json
import sys

import qtawesome as qta
from PySide2 import QtWidgets, QtCore, QtGui


sys.path.append('/Users/yeko/Desktop/netflix_TD/Final_project/libs/hou_lib/file_path.json')


class TreeGroup(QtWidgets.QDialog):
    def __init__(self, parent=hou.qt.mainWindow()):
        super().__init__(parent)
        self.setWindowTitle("Output File Directory")
        self.setGeometry(self.geometry().width()*2, 400, 300, 500)
        self.parent_keys = []

        vbox_lay = QtWidgets.QVBoxLayout(self)
        self.tree_view = QtWidgets.QTreeView(self)
        vbox_lay.addWidget(self.tree_view)

        self.model = QtGui.QStandardItemModel()
        self.tree_view.setModel(self.model)

        self.load_json_data()
        self.tree_view.clicked.connect(self.set_output)

    def set_output(self, index):
        item = self.model.itemFromIndex(index)
        self.parent_keys.clear()
        while item:
            self.parent_keys.append(item.text())
            item = item.parent()
        self.parent_keys.reverse()

        pre_lop = hou.parm('lopoutput').eval()
        ext = pre_lop.split('/')[-1]
        ext_lst: list = ext.split('_')

        lop = '$HIP/'+'/'.join(self.parent_keys)
        lop.replace(' ', '')
        name = lop.split('/')[-1]
        depart = '/'.join(lop.split('/')[-2:-1]).lower()
        slop = lop.split('/')[:-1]
        lopout = '/'.join(slop)+f'/{ext_lst[0]}_{depart}'+'_v001.usdnc'

        hou.parm('username').set(name)
        hou.parm('lopoutput').set(lopout)
        self.accept()

    def load_json_data(self):
        with open('/Users/yeko/Desktop/netflix_TD/Final_project/libs/hou_lib/file_path.json') as f:
            json_data = json.load(f)
        self.add_json_item(self.model.invisibleRootItem(), json_data)
        self.tree_view.expandAll()

    def add_json_item(self, parent_item, data):
        if isinstance(data, dict):
            for key, value in data.items():
                icon = self.get_icon(key)
                if icon:
                    item = QtGui.QStandardItem(icon, str(key))
                else:
                    item = QtGui.QStandardItem(str(key))
                parent_item.appendRow(item)
                self.add_json_item(item, value)
        elif isinstance(data, list):
            for value in data:
                self.add_json_item(parent_item, value)
        else:
            item = QtGui.QStandardItem(str(data))
            parent_item.appendRow(item)
            item.setForeground(QtGui.QBrush(QtGui.QColor("yellow")))

    def get_icon(self, key):
        if key == 'shot':
            return qta.icon('mdi.movie-open')
        elif key == 'DPP':
            return qta.icon('mdi.movie-edit')
        elif key == 'JEP':
            return qta.icon('mdi6.movie-open-plus')
        elif 'EP' in key:
            return qta.icon('fa.file-movie-o')
        elif key == 'Modeling':
            return qta.icon('fa5s.shapes')
        elif key == 'Texturing':
            return qta.icon('mdi.texture')
        elif key == 'Rigging':
            return qta.icon('ei.person')
        elif key == 'Rendering':
            return qta.icon('fa.film')
        elif key == 'Animation':
            return qta.icon('mdi.animation-play')
        elif key == 'Effects':
            return qta.icon('fa.star')
        elif key == 'Lighting':
            return qta.icon('ph.sun-fill')
        elif key == 'Asset':
            return qta.icon('mdi6.chart-bubble')
        return None


tg = TreeGroup()
tg.exec_()
