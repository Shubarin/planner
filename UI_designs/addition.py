# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_designs/addition.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Info_Form(object):
    def setupUi(self, Info_Form):
        Info_Form.setObjectName("Info_Form")
        Info_Form.resize(665, 417)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Info_Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.print_btn = QtWidgets.QPushButton(Info_Form)
        self.print_btn.setObjectName("print_btn")
        self.gridLayout.addWidget(self.print_btn, 0, 1, 1, 1)
        self.export_btn = QtWidgets.QPushButton(Info_Form)
        self.export_btn.setObjectName("export_btn")
        self.gridLayout.addWidget(self.export_btn, 1, 1, 1, 1)
        self.tableWidget = QtWidgets.QTableWidget(Info_Form)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.gridLayout.addWidget(self.tableWidget, 0, 0, 3, 1)
        self.horizontalLayout.addLayout(self.gridLayout)

        self.retranslateUi(Info_Form)
        QtCore.QMetaObject.connectSlotsByName(Info_Form)

    def retranslateUi(self, Info_Form):
        _translate = QtCore.QCoreApplication.translate
        Info_Form.setWindowTitle(_translate("Info_Form", "Подробнее"))
        self.print_btn.setText(_translate("Info_Form", "Печать.."))
        self.print_btn.setShortcut(_translate("Info_Form", "Meta+P"))
        self.export_btn.setText(_translate("Info_Form", "Экспорт..."))
        self.export_btn.setShortcut(_translate("Info_Form", "Meta+S"))
