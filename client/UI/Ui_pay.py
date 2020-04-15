# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\coding\python\ransomware\UI\pay.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_PayWindow(object):
    def setupUi(self, PayWindow):
        PayWindow.setObjectName("PayWindow")
        PayWindow.resize(328, 362)
        self.centralwidget = QtWidgets.QWidget(PayWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 310, 311, 31))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setText("")
        self.label.setScaledContents(True)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(40, 60, 251, 231))
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 10, 311, 31))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setText("")
        self.label_3.setScaledContents(True)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        PayWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(PayWindow)
        QtCore.QMetaObject.connectSlotsByName(PayWindow)

    def retranslateUi(self, PayWindow):
        _translate = QtCore.QCoreApplication.translate
        PayWindow.setWindowTitle(_translate("PayWindow", "支付"))
