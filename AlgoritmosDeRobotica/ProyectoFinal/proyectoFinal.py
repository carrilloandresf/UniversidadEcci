from PyQt5 import QtCore, QtGui, QtWidgets
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo
import board
import busio

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Initialize PCA9685
        i2c = busio.I2C(board.SCL, board.SDA)
        self.pca = PCA9685(i2c)
        self.pca.frequency = 50

        # Configure Servos starting from channel 2
        self.servo1 = servo.Servo(self.pca.channels[2], min_pulse=500, max_pulse=2400)
        self.servo2 = servo.Servo(self.pca.channels[3], min_pulse=500, max_pulse=2400)
        self.servo3 = servo.Servo(self.pca.channels[4], min_pulse=500, max_pulse=2400)
        self.servo4 = servo.Servo(self.pca.channels[5], min_pulse=500, max_pulse=2400)
        self.servo5 = servo.Servo(self.pca.channels[6], min_pulse=500, max_pulse=2400)

        self.horizontalSlider = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider.setGeometry(QtCore.QRect(104, 80, 160, 16))
        self.horizontalSlider.setValue(50)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.horizontalSlider.valueChanged.connect(self.create_slider_callback(self.servo1, self.horizontalSlider))
        
        self.horizontalSlider_2 = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider_2.setGeometry(QtCore.QRect(104, 110, 160, 16))
        self.horizontalSlider_2.setValue(50)
        self.horizontalSlider_2.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_2.setObjectName("horizontalSlider_2")
        self.horizontalSlider_2.valueChanged.connect(self.create_slider_callback(self.servo2, self.horizontalSlider_2))
        
        self.horizontalSlider_3 = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider_3.setGeometry(QtCore.QRect(104, 140, 160, 16))
        self.horizontalSlider_3.setValue(50)
        self.horizontalSlider_3.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_3.setObjectName("horizontalSlider_3")
        self.horizontalSlider_3.valueChanged.connect(self.create_slider_callback(self.servo3, self.horizontalSlider_3))
              
        self.horizontalSlider_4 = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider_4.setGeometry(QtCore.QRect(104, 170, 160, 16))
        self.horizontalSlider_4.setValue(50)
        self.horizontalSlider_4.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_4.setObjectName("horizontalSlider_4")
        self.horizontalSlider_4.valueChanged.connect(self.create_slider_callback(self.servo4, self.horizontalSlider_4))
        
        self.horizontalSlider_5 = QtWidgets.QSlider(self.groupBox)
        self.horizontalSlider_5.setGeometry(QtCore.QRect(80, 160, 160, 16))
        self.horizontalSlider_5.setValue(50)
        self.horizontalSlider_5.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_5.setObjectName("horizontalSlider_5")
        self.horizontalSlider_5.valueChanged.connect(self.create_slider_callback(self.servo5, self.horizontalSlider_5))

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(460, 480, 151, 41))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(60, 80, 31, 20))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(60, 110, 31, 20))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(60, 140, 31, 20))
        self.label_4.setObjectName("label_4")

        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(60, 170, 31, 20))
        self.label_5.setObjectName("label_5")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(30, 40, 241, 191))
        self.groupBox.setObjectName("groupBox")

        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(70, 280, 21, 16))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(70, 310, 21, 16))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(70, 340, 21, 16))
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(50, 450, 131, 91))
        self.label_9.setObjectName("label_9")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(90, 280, 41, 22))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(90, 310, 41, 22))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_3.setGeometry(QtCore.QRect(90, 340, 41, 21))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(30, 250, 161, 131))
        self.groupBox_2.setObjectName("groupBox_2")
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setGeometry(QtCore.QRect(330, 50, 211, 151))
        self.groupBox_3.setObjectName("groupBox_3")
        self.pushButton = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton.setGeometry(QtCore.QRect(60, 50, 80, 22))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_2.setGeometry(QtCore.QRect(60, 90, 80, 22))
        self.pushButton_2.setObjectName("pushButton_2")
        self.groupBox_4 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_4.setGeometry(QtCore.QRect(330, 220, 211, 81))
        self.groupBox_4.setObjectName("groupBox_4")
        self.label_10 = QtWidgets.QLabel(self.groupBox_4)
        self.label_10.setGeometry(QtCore.QRect(20, 30, 57, 14))
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(self.groupBox_4)
        self.label_11.setGeometry(QtCore.QRect(20, 60, 57, 14))
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        self.label_12.setGeometry(QtCore.QRect(570, 70, 57, 14))
        self.label_12.setObjectName("label_12")
        self.label_13 = QtWidgets.QLabel(self.centralwidget)
        self.label_13.setGeometry(QtCore.QRect(60, 200, 31, 20))
        self.label_13.setObjectName("label_13")
        self.groupBox.raise_()
        self.horizontalSlider.raise_()
        self.horizontalSlider_2.raise_()
        self.horizontalSlider_3.raise_()
        self.label.raise_()
        self.label_2.raise_()
        self.label_3.raise_()
        self.label_4.raise_()
        self.horizontalSlider_4.raise_()
        self.label_5.raise_()
        self.label_6.raise_()
        self.label_7.raise_()
        self.label_8.raise_()
        self.label_9.raise_()
        self.lineEdit.raise_()
        self.lineEdit_2.raise_()
        self.lineEdit_3.raise_()
        self.groupBox_2.raise_()
        self.groupBox_3.raise_()
        self.groupBox_4.raise_()
        self.label_12.raise_()
        self.label_13.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 19))
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
        self.label.setText(_translate("MainWindow", "Logo Ecci"))
        self.label_2.setText(_translate("MainWindow", "Art1"))
        self.label_3.setText(_translate("MainWindow", "Art2"))
        self.label_4.setText(_translate("MainWindow", "Art3"))
        self.label_5.setText(_translate("MainWindow", "Efec"))
        self.groupBox.setTitle(_translate("MainWindow", "Modo Manual"))
        self.label_6.setText(_translate("MainWindow", "x"))
        self.label_7.setText(_translate("MainWindow", "y"))
        self.label_8.setText(_translate("MainWindow", "z"))
        self.label_9.setText(_translate("MainWindow", "Presentado por:\n"
"Andres Carrillo\n"
"Daniela Rodriguez\n"
"Jeisson Gutierrez\n"
"William Fernandez"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Modo Semiautomatico"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Modo Automatico"))
        self.pushButton.setText(_translate("MainWindow", "Start"))
        self.pushButton_2.setText(_translate("MainWindow", "Stop"))
        self.groupBox_4.setTitle(_translate("MainWindow", "Sensores"))
        self.label_10.setText(_translate("MainWindow", "Sensor1"))
        self.label_11.setText(_translate("MainWindow", "Sensor2"))
        self.label_12.setText(_translate("MainWindow", "Alert"))
        self.label_13.setText(_translate("MainWindow", "Base"))

    def create_slider_callback(self, servo, slider, joint_index):
        def slider_callback():
            value = slider.value()
            self.move_servo(servo, value)
            self.update_simulation(joint_index, value)
        return slider_callback

    def move_servo(self, servo, value):
        # Map the slider value (0-100) to servo angle (0-180)
        angle = (value / 100.0) * 180.0
        servo.angle = angle

    def update_simulation(self, joint_index, value):
        # Map the slider value (0-100) to joint angle (0-180)
        angle = (value / 100.0) * 180.0
        q = self.robot.q
        q[joint_index] = angle * (3.14 / 180)  # Convert degrees to radians
        self.robot.q = q
        self.simulation.step()

    def create_robot(self):
        # Create a 4-DOF robot with rotating base and three additional rotational joints
        link1 = RevoluteDH(d=0, a=0, alpha=0)  # Base rotation
        link2 = RevoluteDH(d=0, a=1, alpha=0)  # Shoulder rotation
        link3 = RevoluteDH(d=0, a=1, alpha=0)  # Elbow rotation
        link4 = RevoluteDH(d=0, a=1, alpha=0)  # Wrist rotation
        return DHRobot([link1, link2, link3, link4], name='4DOF_ROBOT')


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
