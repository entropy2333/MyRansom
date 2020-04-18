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
        PayWindow.resize(1024, 365)
        self.centralwidget = QtWidgets.QWidget(PayWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(320, 10, 311, 341))
        self.widget.setObjectName("widget")
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setGeometry(QtCore.QRect(30, 70, 251, 231))
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setGeometry(QtCore.QRect(0, 20, 311, 31))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setText("")
        self.label_3.setScaledContents(True)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setGeometry(QtCore.QRect(0, 300, 311, 31))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setText("")
        self.label.setScaledContents(True)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setGeometry(QtCore.QRect(60, 160, 201, 41))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(12)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.widget_2 = QtWidgets.QWidget(self.centralwidget)
        self.widget_2.setGeometry(QtCore.QRect(10, 10, 311, 341))
        self.widget_2.setObjectName("widget_2")
        self.label_5 = QtWidgets.QLabel(self.widget_2)
        self.label_5.setGeometry(QtCore.QRect(10, 40, 281, 41))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.widget_3 = QtWidgets.QWidget(self.centralwidget)
        self.widget_3.setGeometry(QtCore.QRect(9, 10, 621, 341))
        self.widget_3.setObjectName("widget_3")
        self.pushButton_2 = QtWidgets.QPushButton(self.widget_3)
        self.pushButton_2.setGeometry(QtCore.QRect(240, 260, 91, 41))
        self.pushButton_2.setObjectName("pushButton_2")
        self.label_6 = QtWidgets.QLabel(self.widget_3)
        self.label_6.setGeometry(QtCore.QRect(10, 50, 601, 161))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.widget_4 = QtWidgets.QWidget(self.centralwidget)
        self.widget_4.setGeometry(QtCore.QRect(630, 10, 381, 341))
        self.widget_4.setObjectName("widget_4")
        self.listWidget = QtWidgets.QListWidget(self.widget_4)
        self.listWidget.setGeometry(QtCore.QRect(10, 10, 371, 331))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.listWidget.setFont(font)
        self.listWidget.setObjectName("listWidget")
        PayWindow.setCentralWidget(self.centralwidget)
                
        self.tray = QtWidgets.QSystemTrayIcon() #创建系统托盘对象
        self.tray.activated.connect(self.iconActivated) #设置托盘点击事件处理函数
        self.tray_menu = QtWidgets.QMenu(QtWidgets.QApplication.desktop()) #创建菜单
        self.RestoreAction = QtWidgets.QAction(u'马哥勒索 ', self, triggered=self.show) #添加一级菜单动作选项(还原主窗口)
        self.QuitAction = QtWidgets.QAction(u'诚信的一 ', self, triggered=self.show) #添加一级菜单动作选项(退出程序)
        self.tray_menu.addAction(self.RestoreAction) #为菜单添加动作
        self.tray_menu.addAction(self.QuitAction)
        self.tray.setContextMenu(self.tray_menu) #设置系统托盘菜单

        self.retranslateUi(PayWindow)
        QtCore.QMetaObject.connectSlotsByName(PayWindow)

    def retranslateUi(self, PayWindow):
        _translate = QtCore.QCoreApplication.translate
        PayWindow.setWindowTitle(_translate("PayWindow", "支付"))
        self.pushButton.setText(_translate("PayWindow", "刷新二维码"))
        self.label_5.setText(_translate("PayWindow", "马哥勒索"))
        self.pushButton_2.setText(_translate("PayWindow", "关闭"))
        self.label_6.setText(_translate("PayWindow", "马哥勒索期待与您的下一次相遇"))
