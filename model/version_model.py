import datetime
import time

from libs import db
from PySide2 import QtWidgets, QtGui, QtCore


class VersionModel(QtCore.QAbstractTableModel):
    def __init__(self, data, symlink:int = None, parent=None):
        super().__init__(parent)
        self.__data = data
        self.symlink = symlink
        # COLUMN HEADER NAME
        self.__header = ['USER', 'DEPART', 'CACHE_NAME', 'NOTE', 'UPDATED_TIME']

    def data(self, index, role=...):
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            data = self.__data[index.row()][index.column()]
            if isinstance(data, datetime.datetime):
                return f'{data.year}-{data.month}-{data.day}  {data.hour}:{data.minute}'
            elif not isinstance(data, str):
                return str(data)
            return data

        if role == QtCore.Qt.BackgroundRole:
            if index.row() == self.symlink:
                return QtGui.QColor('green')

        if role == QtCore.Qt.TextColorRole:
            if index.row() == self.symlink:
                return QtGui.QColor('white')

    def columnCount(self, parent=...):
        return len(self.__data[0])

    def rowCount(self, parent=...):
        return len(self.__data)

    def headerData(self, section, orientation, role=...):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return self.__header[section]
            elif orientation == QtCore.Qt.Vertical:
                return str((int(section) + 1))


class ControllerMVC(QtWidgets.QDialog):
    def __init__(self, fid: int, link: int, parent=None):
        super().__init__(parent)
        self.f_id = fid
        self.link = link
        self.__db = db.DBVersionUp()
        self.view = QtWidgets.QTableView()
        self.model = VersionModel(self.get_data(), symlink=self.link)

        vlayout = QtWidgets.QVBoxLayout(self)
        vlayout.addWidget(self.view)

        self.view.setModel(self.model)
        self.view.verticalHeader().setDefaultSectionSize(40)
        self.view.setColumnWidth(0, 80)
        self.view.setColumnWidth(1, 80)
        self.view.setColumnWidth(2, 500)
        self.view.setColumnWidth(3, 300)
        self.view.setColumnWidth(4, 100)
        self.resize(900, 150)

    def set_data_from_db(self):
        st = time.time()
        self.view.setModel(self.model)
        et = time.time()
        print(et - st)

    def get_data(self):
        cus_lst = list()
        d = self.__db.get_cache_id_by_fid(self.f_id)

        # create data
        for i, cid in enumerate(d):
            cnote = self.__db.get_note_by_cid(cid)[0]
            uinfo = self.__db.get_uid_date_by_cid(cid)
            uname = self.__db.get_user_by_uid(uinfo[2])[0][0]
            udepart = self.__db.get_depart_by_name(uname)[0][0]
            udate = uinfo[3]
            cpath = self.__db.get_cpath_by_cid(cid)[0]
            # print('\nuinfo;', uinfo, '\nuname:', uname,
            #       '\nudepart:', udepart, '\nudate:', udate, '\ncpath:', cpath)
            # print('note:', cnote)
            custom = (uname, udepart, cpath, cnote, udate)
            cus_lst.append(custom)
        return cus_lst


if __name__ == '__main__':
    pass
