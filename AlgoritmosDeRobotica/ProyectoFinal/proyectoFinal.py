from PyQt5 import QtCore, QtGui, QtWidgets
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo
import board
import busio
from roboticstoolbox import DHRobot, RevoluteDH

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

        # Create robot instance
        self.robot = self.create_robot()

        # Setup UI components
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

        # Create sliders and connect to servos
        self.horizontalSlider = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider.setGeometry(QtCore.QRect(104, 80, 160, 16))
        self.horizontalSlider.setValue(50)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.horizontalSlider.valueChanged.connect(self.create_slider_callback(self.servo1, self.horizontalSlider, 0))

        self.horizontalSlider_2 = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider_2.setGeometry(QtCore.QRect(104, 110, 160, 16))
        self.horizontalSlider_2.setValue(50)
        self.horizontalSlider_2.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_2.setObjectName("horizontalSlider_2")
        self.horizontalSlider_2.valueChanged.connect(self.create_slider_callback(self.servo2, self.horizontalSlider_2, 1))

        self.horizontalSlider_3 = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider_3.setGeometry(QtCore.QRect(104, 140, 160, 16))
        self.horizontalSlider_3.setValue(50)
        self.horizontalSlider_3.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_3.setObjectName("horizontalSlider_3")
        self.horizontalSlider_3.valueChanged.connect(self.create_slider_callback(self.servo3, self.horizontalSlider_3, 2))

        self.horizontalSlider_4 = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider_4.setGeometry(QtCore.QRect(104, 170, 160, 16))
        self.horizontalSlider_4.setValue(50)
        self.horizontalSlider_4.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_4.setObjectName("horizontalSlider_4")
        self.horizontalSlider_4.valueChanged.connect(self.create_slider_callback(self.servo4, self.horizontalSlider_4, 3))

        self.horizontalSlider_5 = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider_5.setGeometry(QtCore.QRect(104, 200, 160, 16))
        self.horizontalSlider_5.setValue(50)
        self.horizontalSlider_5.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_5.setObjectName("horizontalSlider_5")
        self.horizontalSlider_5.valueChanged.connect(self.create_slider_callback(self.servo5, self.horizontalSlider_5, 4))

        # Additional UI components (no changes made here)
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(70, 280, 21, 16))
        self.label_6.setObjectName("label_6")
        # (... other UI components ...)

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
        # (... other translations ...)

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
        # Ensure the robot and simulation attributes are defined before calling this
        if hasattr(self, 'robot'):
            angle = (value / 100.0) * 180.0
            q = self.robot.q
            q[joint_index] = angle * (3.14 / 180)  # Convert degrees to radians
            self.robot.q = q
            # Call step method if self.simulation is properly defined
            if hasattr(self, 'simulation'):
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