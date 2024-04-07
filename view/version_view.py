
from PySide2 import QtWidgets, QtCore, QtGui


class TodoView(QtWidgets.QTableView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.alternatingRowColors()


if __name__ == '__main__':
    pass