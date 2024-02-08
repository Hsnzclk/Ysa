from PyQt5 import QtCore, QtWidgets, QtGui
import sys

import pandas as pd
pd.options.display.float_format = '${:,.3f}'.format  
class PandasModel(QtCore.QAbstractTableModel): 
    def __init__(self, df = pd.DataFrame(), parent=None): 
        QtCore.QAbstractTableModel.__init__(self, parent=parent)
        self._df = df

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        if orientation == QtCore.Qt.Horizontal:
            try:
                return self._df.columns.tolist()[section]
            except (IndexError, ):
                return QtCore.QVariant()
        elif orientation == QtCore.Qt.Vertical:
            try:
                # return self.df.index.tolist()
                return self._df.index.tolist()[section]
            except (IndexError, ):
                return QtCore.QVariant()

    def data(self, index, role):
        row = index.row()
        column = index.column()
        if role == QtCore.Qt.DisplayRole:
            return QtCore.QVariant(str(self._df.iloc[index.row(), index.column()]))
        if role == QtCore.Qt.BackgroundRole:
            if str(self._df.iloc[row][column])=='Doğru':
                return QtGui.QBrush(QtGui.QColor('green'))
            elif str(self._df.iloc[row][column])=='Yanlış':
                return QtGui.QBrush(QtGui.QColor('red'))
            else:
                return QtCore.QVariant()
        elif not index.isValid():
            return QtCore.QVariant()
        else:
            return QtCore.QVariant()

        

    def setData(self, index, value, role):
        row = self._df.index[index.row()]
        col = self._df.columns[index.column()]
        if hasattr(value, 'toPyObject'):
            # PyQt4 gets a QVariant
            value = value.toPyObject()
        else:
            # PySide gets an unicode
            dtype = self._df[col].dtype
            if dtype != object:
                value = None if value == '' else dtype.type(value)
        self._df.set_value(row, col, value)
        return True

    def rowCount(self, parent=QtCore.QModelIndex()): 
        return len(self._df.index)

    def columnCount(self, parent=QtCore.QModelIndex()): 
        return len(self._df.columns)

    def sort(self, column, order):
        colname = self._df.columns.tolist()[column]
        self.layoutAboutToBeChanged.emit()
        self._df.sort_values(colname, ascending= order == QtCore.Qt.AscendingOrder, inplace=True)
        self._df.reset_index(inplace=True, drop=True)
        self.layoutChanged.emit()
