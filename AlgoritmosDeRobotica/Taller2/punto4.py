# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'punto4.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(789, 715)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(-30, 350, 831, 151))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.slider_volt = QtWidgets.QSlider(self.horizontalLayoutWidget)
        self.slider_volt.setMinimum(1)
        self.slider_volt.setMaximum(20)
        self.slider_volt.setOrientation(QtCore.Qt.Qt::Orientation::Vertical)
        self.slider_volt.setObjectName("slider_volt")
        self.horizontalLayout.addWidget(self.slider_volt)
        self.slider_cap = QtWidgets.QSlider(self.horizontalLayoutWidget)
        self.slider_cap.setMinimum(1)
        self.slider_cap.setMaximum(100)
        self.slider_cap.setOrientation(QtCore.Qt.Qt::Orientation::Vertical)
        self.slider_cap.setObjectName("slider_cap")
        self.horizontalLayout.addWidget(self.slider_cap)
        self.slider_res = QtWidgets.QSlider(self.horizontalLayoutWidget)
        self.slider_res.setMinimum(1)
        self.slider_res.setMaximum(1000)
        self.slider_res.setOrientation(QtCore.Qt.Qt::Orientation::Vertical)
        self.slider_res.setObjectName("slider_res")
        self.horizontalLayout.addWidget(self.slider_res)
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(60, 290, 661, 51))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_volt = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Century Schoolbook")
        font.setPointSize(16)
        font.setBold(True)
        self.label_volt.setFont(font)
        self.label_volt.setMouseTracking(False)
        self.label_volt.setStyleSheet("background-color: rgb(84, 154, 186);\n"
"background-color: rgb(255, 85, 255);")
        self.label_volt.setAlignment(QtCore.Qt.Qt::AlignmentFlag::AlignCenter)
        self.label_volt.setWordWrap(True)
        self.label_volt.setObjectName("label_volt")
        self.horizontalLayout_2.addWidget(self.label_volt)
        self.label_cap = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Century Schoolbook")
        font.setPointSize(16)
        font.setBold(True)
        self.label_cap.setFont(font)
        self.label_cap.setStyleSheet("background-color: rgb(84, 154, 186);\n"
"background-color: rgb(255, 85, 127);")
        self.label_cap.setAlignment(QtCore.Qt.Qt::AlignmentFlag::AlignCenter)
        self.label_cap.setWordWrap(True)
        self.label_cap.setObjectName("label_cap")
        self.horizontalLayout_2.addWidget(self.label_cap)
        self.label_res = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Century Schoolbook")
        font.setPointSize(16)
        font.setBold(True)
        self.label_res.setFont(font)
        self.label_res.setStyleSheet("background-color: rgb(84, 154, 186);\n"
"background-color: rgb(170, 85, 127);")
        self.label_res.setAlignment(QtCore.Qt.Qt::AlignmentFlag::AlignCenter)
        self.label_res.setWordWrap(True)
        self.label_res.setObjectName("label_res")
        self.horizontalLayout_2.addWidget(self.label_res)
        self.horizontalLayoutWidget_3 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(80, 540, 621, 132))
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_2 = QtWidgets.QLabel(self.horizontalLayoutWidget_3)
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_4.addWidget(self.label_2)
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget_3)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setAutoFillBackground(False)
        self.label.setStyleSheet("color: rgb(255, 85, 127);")
        self.label.setAlignment(QtCore.Qt.Qt::AlignmentFlag::AlignCenter)
        self.label.setObjectName("label")
        self.horizontalLayout_4.addWidget(self.label)
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(220, 30, 341, 221))
        self.widget.setObjectName("widget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 789, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_volt.setText(_translate("MainWindow", "VOLTAJE (V)"))
        self.label_cap.setText(_translate("MainWindow", "CAPACITANCIA (uF)"))
        self.label_res.setText(_translate("MainWindow", "RESISTENCIA (ohms)"))
        self.label.setText(_translate("MainWindow", "INTEGRANTES:\n"
"Felipe Carrillo\n"
"Daniela Rodriguez\n"
"Jeisson Gutierrez\n"
"Julian Pinzon"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())