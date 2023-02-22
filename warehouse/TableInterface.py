import typing
from datetime import date

from alchemy_models import Base

from PyQt5.QtWidgets import QStyledItemDelegate

import alchemy_models

from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex


class TableModel(QAbstractTableModel):

    def __init__(self, data, headers:list = None):
        super().__init__()
        self._headers = headers
        self._data = data

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self._data)

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return len(self._data[0])

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]

    def headerData(self, col: int, orientation: Qt.Orientation, role: int = ...) -> typing.Any:
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if self._headers:
                return self._headers[col]
            return self._data[0][col]
        if orientation == Qt.Vertical and role == Qt.DisplayRole:
            return str(col+1)
        return


class BaseDelegate(QStyledItemDelegate):
    def displayText(self, value: typing.Any, locale) -> str:
        if isinstance(value, (Base, date)):
            return str(value)

        return super().displayText(value, locale)


def main():
    pass


if __name__ == '__main__':
    # t = TableModel([[1, 2, 3], [4, 5, 6]])
    # print(create_client_table())
    pass