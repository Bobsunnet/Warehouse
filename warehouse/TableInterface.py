import typing

from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex


class TableModel(QAbstractTableModel):

    def __init__(self, data):
        super().__init__()
        self._data = data

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self._data)

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return len(self._data[0])

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]






def main():
    pass


if __name__ == '__main__':
    t = TableModel([[1,2,3],[4,5,6]])

