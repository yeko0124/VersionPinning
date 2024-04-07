import functools
import os

from PySide2 import QtGui, QtWidgets, QtCore

import hou
import importlib
import pathlib

from model import version_model
# from view import version_view

import qtawesome as qta
from libs import db
from ui import version_track_ui

importlib.reload(version_track_ui)


class TableWidget(QtWidgets.QWidget, version_track_ui.Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)


class VersionTable(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.final_path = pathlib.Path.home()/'workspace/final/'
        w = QtWidgets.QWidget()
        self.__vbox_layout = QtWidgets.QVBoxLayout()

        self.final_dir_btn = QtWidgets.QPushButton('Open Final Directory')
        self.final_dir_btn.setIcon(qta.icon('msc.file-symlink-directory'))
        self.__vbox_layout.addWidget(self.final_dir_btn)

        self.__widget_lst = list()
        self.__db = db.DBVersionUp()
        self.setup_widget()

        w.setLayout(self.__vbox_layout)
        self.setCentralWidget(w)

        self.final_dir_btn.clicked.connect(self.open_final_dir)

    def open_final_dir(self):
        path, ext = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Open Dir', self.final_path)
        print(path, ext)

    def setup_widget(self):
        f_name = self.__db.get_final_name()
        f_id = self.__db.get_final_id()
        for i, n in enumerate(f_name):
            label_name = n[0]
            self.widget = TableWidget()
            self.widget.label.setText(label_name)
            self.__vbox_layout.addWidget(self.widget)
            self.set_combobox(f_id[i])
            self.widget.comboBox.addItems(self.com_lst)
            tooltip_lst = self.set_tooltips_lst(f_id[i])  # final id
            self.set_com_tooltip(tooltip_lst)

            self.widget.pushButton__open.setIcon(qta.icon('fa5s.folder-open'))
            self.widget.pushButton__reload.setIcon(qta.icon('mdi.reload'))

            c_ver = self.cur_ver()
            self.widget.comboBox.setCurrentIndex(c_ver)
            self.widget.pushButton__reload.clicked.connect(functools.partial(self.reload_symbolic_link, f_id[i]))
            self.widget.pushButton__open.clicked.connect(functools.partial(self.open_link, f_id[i]))
            self.widget.toolButton_info.clicked.connect(functools.partial(self.open_info, f_id[i]))
            self.__widget_lst.append(self.widget)

    def cur_ver(self) -> int:
        c_ver = 0
        name = self.widget.label.text()
        cpath = self.final_path + name
        try:
            tpath = os.path.realpath(cpath)
            print(f'연결된 링크>>> {tpath}')
            c_vers = self.__db.get_id_by_cfile(tpath)
            # print(c_vers)
            c_lst = self.__db.get_one_cache_path(c_vers)
            for i, v in enumerate(c_lst):
                print(i, v[0])
                if v[0] == tpath:
                    c_ver = i
        except FileNotFoundError:
            print('no symlink')
        return c_ver

    def open_info(self, f_id):
        w: TableWidget = self.__widget_lst[f_id-1]
        # link 걸린 것만 컬러값을 주기 위해서 인덱스를 받아서 MVC로 전달
        link = w.comboBox.currentIndex()
        ctrl = version_model.ControllerMVC(f_id, link)
        ctrl.exec_()

    def set_com_tooltip(self, lst):
        for index, note in enumerate(lst):
            tooltip = f'Note\n{note}'
            self.widget.comboBox.setItemData(index, tooltip, QtCore.Qt.ToolTipRole)

    # 직접 링크를 연결 >> 심볼릭 링크 코드 중복 이유
    def reload_symbolic_link(self, f_id):
        w: TableWidget = self.__widget_lst[f_id-1]
        v_num = w.comboBox.currentIndex()
        path = self.__db.get_one_cache_path(f_id)

        src_path = pathlib.Path(path[v_num][0])
        print(w.label.text())
        dst_final = self.final_path/w.label.text()
        print(dst_final)
        if os.path.exists(dst_final):
            os.remove(dst_final)
            print('remove complete')

        print('link start!!!!')
        os.symlink(src_path, dst_final)
        print('complete')

    def open_link(self, f_id):
        w: TableWidget = self.__widget_lst[f_id-1]
        v_num = w.comboBox.currentIndex()
        path = self.__db.get_one_cache_path(f_id)
        print(path[v_num][0])

    def set_combobox(self, f_id):
        cnt = 1
        self.com_lst = list()
        fid = self.__db.get_cache_files()  # [1, 1, 2, 2, 2, 1, 3, 1, 3]
        for file_id in fid:
            if f_id == file_id:
                self.com_lst.append(f'version{cnt}')
                cnt += 1
            else:
                continue

    # cache file table에서 파일 아이디에 맞는 id를 이용하여 note list를 생성
    def set_tooltips_lst(self, f_id):
        self.ref_lst = list()
        cache_id = self.__db.get_cache_id_by_fid(f_id)
        # print(cache_id)
        note = list()
        for cid in cache_id:
            try:
                n = self.__db.get_note_by_cid(cid)[0]
                note.append(n)
            except TypeError:
                continue
        return note


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    version_table = VersionTable()
    version_table.show()
    app.exec_()