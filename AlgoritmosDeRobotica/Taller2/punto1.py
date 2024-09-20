import sys
import math
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(489, 326)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(220, 190, 131, 41))
        self.label_5.setSizeIncrement(QtCore.QSize(0, 0))
        self.label_5.setText("")
        self.label_5.setPixmap(QtGui.QPixmap("../../src/img/logo.png"))
        self.label_5.setScaledContents(True)
        self.label_5.setObjectName("label_5")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(30, 20, 71, 21))
        self.textEdit.setObjectName("textEdit")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(20, 60, 191, 91))
        self.groupBox.setObjectName("groupBox")
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_2.setGeometry(QtCore.QRect(100, 30, 91, 21))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton = QtWidgets.QPushButton(self.groupBox)
        self.pushButton.setGeometry(QtCore.QRect(5, 30, 91, 21))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_4 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_4.setGeometry(QtCore.QRect(100, 60, 91, 21))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_3 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_3.setGeometry(QtCore.QRect(5, 60, 91, 21))
        self.pushButton_3.setObjectName("pushButton_3")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(110, 20, 16, 16))
        font = QtGui.QFont()
        font.setBold(True)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(220, 70, 131, 101))
        self.label_6.setObjectName("label_6")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(220, 20, 91, 21))
        font = QtGui.QFont()
        font.setBold(True)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(20, 160, 191, 121))
        self.groupBox_2.setObjectName("groupBox_2")
        self.pushButton_5 = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_5.setGeometry(QtCore.QRect(100, 30, 91, 21))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_6 = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_6.setGeometry(QtCore.QRect(5, 30, 91, 21))
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_7 = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_7.setGeometry(QtCore.QRect(100, 60, 91, 21))
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_8 = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_8.setGeometry(QtCore.QRect(5, 60, 91, 21))
        self.pushButton_8.setObjectName("pushButton_8")
        self.pushButton_9 = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_9.setGeometry(QtCore.QRect(5, 90, 91, 21))
        self.pushButton_9.setObjectName("pushButton_9")
        self.pushButton_10 = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_10.setGeometry(QtCore.QRect(100, 90, 91, 21))
        self.pushButton_10.setObjectName("pushButton_10")
        self.textEdit_2 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_2.setGeometry(QtCore.QRect(130, 20, 71, 21))
        self.textEdit_2.setObjectName("textEdit_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 489, 19))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Connect arithmetic buttons
        self.pushButton.clicked.connect(self.suma)
        self.pushButton_2.clicked.connect(self.resta)
        self.pushButton_3.clicked.connect(self.multiplicacion)
        self.pushButton_4.clicked.connect(self.division)

        # Connect trigonometry buttons
        self.pushButton_5.clicked.connect(self.coseno)
        self.pushButton_6.clicked.connect(self.seno)
        self.pushButton_7.clicked.connect(self.cotangente)
        self.pushButton_8.clicked.connect(self.tangente)
        self.pushButton_9.clicked.connect(self.secante)
        self.pushButton_10.clicked.connect(self.cosecante)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox.setTitle(_translate("MainWindow", "Operaciones aritméticas"))
        self.pushButton_2.setText(_translate("MainWindow", "Resta"))
        self.pushButton.setText(_translate("MainWindow", "Suma"))
        self.pushButton_4.setText(_translate("MainWindow", "División"))
        self.pushButton_3.setText(_translate("MainWindow", "Multiplicación"))
        self.label.setText(_translate("MainWindow", "+"))
        self.label_4.setText(_translate("MainWindow", "Resultado"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Trigonometría Básica"))
        self.pushButton_5.setText(_translate("MainWindow", "Coseno"))
        self.pushButton_6.setText(_translate("MainWindow", "Seno"))
        self.pushButton_7.setText(_translate("MainWindow", "Cotangente"))
        self.pushButton_8.setText(_translate("MainWindow", "Tangente"))
        self.pushButton_9.setText(_translate("MainWindow", "Secante"))
        self.pushButton_10.setText(_translate("MainWindow", "Cosecante"))

    # Arithmetic Operations
    def suma(self):
        try:
            num1 = float(self.textEdit.toPlainText())
            num2 = float(self.textEdit_2.toPlainText())
            resultado = num1 + num2
            self.label_4.setText(str(resultado))
        except ValueError:
            self.label_4.setText("Error")

    def resta(self):
        try:
            num1 = float(self.textEdit.toPlainText())
            num2 = float(self.textEdit_2.toPlainText())
            resultado = num1 - num2
            self.label_4.setText(str(resultado))
        except ValueError:
            self.label_4.setText("Error")

    def multiplicacion(self):
        try:
            num1 = float(self.textEdit.toPlainText())
            num2 = float(self.textEdit_2.toPlainText())
            resultado = num1 * num2
            self.label_4.setText(str(resultado))
        except ValueError:
            self.label_4.setText("Error")

    def division(self):
        try:
            num1 = float(self.textEdit.toPlainText())
            num2 = float(self.textEdit_2.toPlainText())
            if num2 != 0:
                resultado = num1 / num2
                self.label_4.setText(str(resultado))
            else:
                self.label_4.setText("División por 0")
        except ValueError:
            self.label_4.setText("Error")

    # Trigonometric Functions
    def coseno(self):
        try:
            num = float(self.textEdit.toPlainText())
            resultado = math.cos(math.radians(num))
            self.label_4.setText(str(resultado))
        except ValueError:
            self.label_4.setText("Error")

    def seno(self):
        try:
            num = float(self.textEdit.toPlainText())
            resultado = math.sin(math.radians(num))
            self.label_4.setText(str(resultado))
        except ValueError:
            self.label_4.setText("Error")

    def tangente(self):
        try:
            num = float(self.textEdit.toPlainText())
            resultado = math.tan(math.radians(num))
            self.label_4.setText(str(resultado))
        except ValueError:
            self.label_4.setText("Error")

    def cotangente(self):
        try:
            num = float(self.textEdit.toPlainText())
            resultado = 1 / math.tan(math.radians(num))
            self.label_4.setText(str(resultado))
        except ValueError:
            self.label_4.setText("Error")

    def secante(self):
        try:
            num = float(self.textEdit.toPlainText())
            resultado = 1 / math.cos(math.radians(num))
            self.label_4.setText(str(resultado))
        except ValueError:
            self.label_4.setText("Error")

    def cosecante(self):
        try:
            num = float(self.textEdit.toPlainText())
            resultado = 1 / math.sin(math.radians(num))
            self.label_4.setText(str(resultado))
        except ValueError:
            self.label_4.setText("Error")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
