# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_designs/filter_db.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Filter_Form(object):
    def setupUi(self, Filter_Form):
        Filter_Form.setObjectName("Filter_Form")
        Filter_Form.resize(608, 431)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Filter_Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.dateEdit = QtWidgets.QDateEdit(Filter_Form)
        self.dateEdit.setObjectName("dateEdit")
        self.gridLayout.addWidget(self.dateEdit, 1, 2, 1, 1)
        self.search_btn = QtWidgets.QPushButton(Filter_Form)
        self.search_btn.setObjectName("search_btn")
        self.gridLayout.addWidget(self.search_btn, 2, 0, 1, 3)
        self.comboBox = QtWidgets.QComboBox(Filter_Form)
        self.comboBox.setObjectName("comboBox")
        self.gridLayout.addWidget(self.comboBox, 1, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(Filter_Form)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)
        self.title_line = QtWidgets.QLineEdit(Filter_Form)
        self.title_line.setObjectName("title_line")
        self.gridLayout.addWidget(self.title_line, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(Filter_Form)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(Filter_Form)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 2, 1, 1)
        self.print_btn = QtWidgets.QPushButton(Filter_Form)
        self.print_btn.setObjectName("print_btn")
        self.gridLayout.addWidget(self.print_btn, 0, 3, 1, 1)
        self.export_btn = QtWidgets.QPushButton(Filter_Form)
        self.export_btn.setObjectName("export_btn")
        self.gridLayout.addWidget(self.export_btn, 1, 3, 1, 1)
        self.tableWidget = QtWidgets.QTableWidget(Filter_Form)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.AnyKeyPressed|QtWidgets.QAbstractItemView.DoubleClicked|QtWidgets.QAbstractItemView.EditKeyPressed|QtWidgets.QAbstractItemView.SelectedClicked)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.gridLayout.addWidget(self.tableWidget, 3, 0, 1, 4)
        self.reset_btn = QtWidgets.QPushButton(Filter_Form)
        self.reset_btn.setObjectName("reset_btn")
        self.gridLayout.addWidget(self.reset_btn, 2, 3, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout)

        self.retranslateUi(Filter_Form)
        QtCore.QMetaObject.connectSlotsByName(Filter_Form)

    def retranslateUi(self, Filter_Form):
        _translate = QtCore.QCoreApplication.translate
        Filter_Form.setWindowTitle(_translate("Filter_Form", "Сформировать график отчетов"))
        self.search_btn.setText(_translate("Filter_Form", "Найти"))
        self.search_btn.setShortcut(_translate("Filter_Form", "Return"))
        self.label_2.setText(_translate("Filter_Form", "Периодичность:"))
        self.label.setText(_translate("Filter_Form", "Название:"))
        self.label_3.setText(_translate("Filter_Form", "Дата"))
        self.print_btn.setText(_translate("Filter_Form", "Печать.."))
        self.print_btn.setShortcut(_translate("Filter_Form", "Meta+P"))
        self.export_btn.setText(_translate("Filter_Form", "Экспорт.."))
        self.export_btn.setShortcut(_translate("Filter_Form", "Meta+S"))
        self.reset_btn.setText(_translate("Filter_Form", "Сбросить"))
