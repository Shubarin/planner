# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_designs/upd_wnd.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Upd_Form(object):
    def setupUi(self, Upd_Form):
        Upd_Form.setObjectName("Upd_Form")
        Upd_Form.resize(511, 388)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Upd_Form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_web_con = QtWidgets.QLabel(Upd_Form)
        self.label_web_con.setText("")
        self.label_web_con.setObjectName("label_web_con")
        self.verticalLayout.addWidget(self.label_web_con)
        self.label_4 = QtWidgets.QLabel(Upd_Form)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.dateEdit = QtWidgets.QDateEdit(Upd_Form)
        self.dateEdit.setDate(QtCore.QDate(2021, 1, 1))
        self.dateEdit.setObjectName("dateEdit")
        self.verticalLayout.addWidget(self.dateEdit)
        self.upd_btn = QtWidgets.QPushButton(Upd_Form)
        self.upd_btn.setObjectName("upd_btn")
        self.verticalLayout.addWidget(self.upd_btn)
        self.label = QtWidgets.QLabel(Upd_Form)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.textEdit = QtWidgets.QTextEdit(Upd_Form)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout.addWidget(self.textEdit)
        self.label_2 = QtWidgets.QLabel(Upd_Form)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.textEdit_2 = QtWidgets.QTextEdit(Upd_Form)
        self.textEdit_2.setObjectName("textEdit_2")
        self.verticalLayout.addWidget(self.textEdit_2)
        self.label_3 = QtWidgets.QLabel(Upd_Form)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("background-color: rgb(252, 0, 6);\n"
"color: rgb(250, 255, 255);")
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(Upd_Form)
        QtCore.QMetaObject.connectSlotsByName(Upd_Form)

    def retranslateUi(self, Upd_Form):
        _translate = QtCore.QCoreApplication.translate
        Upd_Form.setWindowTitle(_translate("Upd_Form", "Обновление"))
        self.label_4.setText(_translate("Upd_Form", "Выберите год:"))
        self.dateEdit.setDisplayFormat(_translate("Upd_Form", "yyyy"))
        self.upd_btn.setText(_translate("Upd_Form", "Обновить"))
        self.label.setText(_translate("Upd_Form", "Добавлено:"))
        self.label_2.setText(_translate("Upd_Form", "Удалено:"))
        self.label_3.setText(_translate("Upd_Form", "НЕ ЗАБУДЬТЕ ПЕРЕНЕСТИ ОТЧЕТЫ С НОВЫХ ПРАЗДНИЧНЫХ ДНЕЙ!!!"))
