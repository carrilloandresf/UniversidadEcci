# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import os

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(799, 614)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # ComboBox para seleccionar el robot
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(470, 20, 161, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.comboBox.setFont(font)
        self.comboBox.setStyleSheet("background-color: rgb(170, 85, 255);\n"
                                    "\n"
                                    "background-color: rgb(0, 85, 0);\n"
                                    "\n"
                                    "alternate-background-color: rgb(255, 0, 127);")
        self.comboBox.setPlaceholderText("")
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")

        # Label para descripción
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(310, 110, 401, 91))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(170, 0, 127);")
        self.label.setWordWrap(True)
        self.label.setObjectName("label")

        # Label para imagen del robot
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(340, 210, 300, 300))
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")

        # Label para el nombre del robot seleccionado
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(30, 250, 200, 200))
        font = QtGui.QFont()
        font.setPointSize(20)  # Aumentar tamaño del texto
        self.label_3.setFont(font)
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")

        # Label para los integrantes del grupo
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(70, 270, 150, 150))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("background-color: rgb(255, 170, 127);\n"
                                   "\n"
                                   "background-color: rgb(255, 255, 255);\n"
                                   "\n"
                                   "background-color: rgb(0, 0, 0);")
        self.label_4.setObjectName("label_4")

        # Logo de la universidad
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(30, 20, 200, 150))
        pixmap = QtGui.QPixmap("path/to/your/logo.png")  # Asegúrate de colocar la ruta correcta de la imagen
        self.label_5.setPixmap(pixmap.scaled(200, 150, QtCore.Qt.KeepAspectRatio))
        self.label_5.setObjectName("label_5")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 799, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.comboBox.currentIndexChanged.connect(self.update_robot_info)  # Conectar el comboBox a la función
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Selector de Robots"))
        self.comboBox.setItemText(0, _translate("MainWindow", "CARTESIANO"))
        self.comboBox.setItemText(1, _translate("MainWindow", "CILINDRICO"))
        self.comboBox.setItemText(2, _translate("MainWindow", "ESFÉRICO"))
        self.label.setText(_translate("MainWindow", "SELECCIONE UNA OPCION DE ROBOT PARA VISUALIZAR LAS CARACTERISTICAS:"))
        self.label_4.setText(_translate("MainWindow", "INGTEGRANTES:\n"
                                                      "\n"
                                                      "Daniela Rodriguez\n"
                                                      "\n"
                                                      "Felipe Carrillo\n"
                                                      "\n"
                                                      "Jeisson Gutierrez\n"
                                                      "\n"
                                                      "Julian Fernandez"))

    def update_robot_info(self):
        # Datos de los robots
        robot_data = {
            "CARTESIANO": {
                "articulaciones": "3 art lineales",
                "imagen": "cartesiano.png"
            },
            "CILINDRICO": {
                "articulaciones": "1 art rot y 2 lin",
                "imagen": "cilindrico.png"
            },
            "ESFÉRICO": {
                "articulaciones": "2 art rot y 1 lin",
                "imagen": "esferico.png"
            }
        }

        # Obtener la opción seleccionada
        robot_seleccionado = self.comboBox.currentText()

        # Actualizar label_3 con las articulaciones
        self.label_3.setText(robot_data[robot_seleccionado]["articulaciones"])

        # Actualizar label_2 con la imagen correspondiente
        image_path = robot_data[robot_seleccionado]["imagen"]
        if os.path.exists(image_path):  # Verificar si la imagen existe
            pixmap = QtGui.QPixmap(image_path)
            self.label_2.setPixmap(pixmap.scaled(300, 300, QtCore.Qt.KeepAspectRatio))
        else:
            self.label_2.setText("Imagen no encontrada")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
