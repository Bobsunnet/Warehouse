import typing
from datetime import date

from alchemy_models import Base

from PyQt5.QtWidgets import QStyledItemDelegate, QTableView

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

    def setData(self, index: QModelIndex, value: typing.Any, role: int = Qt.EditRole) -> bool:
        if index.isValid() and role == Qt.EditRole:
            #if no value was entered
            if not value:
                return False
            self._data[index.row()][index.column()] = value
            self.dataChanged.emit(index, index)
            return True

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        return super().flags(index) | Qt.ItemIsEditable


class BaseDelegate(QStyledItemDelegate):
    def displayText(self, value: typing.Any, locale) -> str:
        if isinstance(value, (Base, date)):
            return str(value)

        return super().displayText(value, locale)


class TableWidget(QTableView):
    def __init__(self):
        super().__init__()

        self._filter_column = None

    def setFilterColumn(self, f_column:int):
        ''' CUSTOM METHOD
        Hides "filtered"(mainly the last one) column from view
        :param f_column: column index
        :return:
        '''
        if self._filter_column and f_column != self._filter_column:
            self.showColumn(self._filter_column)
        self._filter_column = f_column
        self.hideColumn(self._filter_column)

    def clearFilterColumn(self):
        '''
        CUSTOM METHOD
        clear's filter from view
        :return:
        '''
        if self._filter_column:
            self.showColumn(self._filter_column)
        self._filter_column = None



def main():
    pass


if __name__ == '__main__':
    # t = TableModel([[1, 2, 3], [4, 5, 6]])
    # print(create_client_table())
    pass