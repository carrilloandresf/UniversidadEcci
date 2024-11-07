from PyQt5 import QtWidgets, QtCore, QtGui

class TestWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test Window")
        layout = QtWidgets.QVBoxLayout()
        label = QtWidgets.QLabel("This is a test label")
        button = QtWidgets.QPushButton("Test Button")
        layout.addWidget(label)
        layout.addWidget(button)
        self.setLayout(layout)

app = QtWidgets.QApplication([])
window = TestWindow()
window.show()
app.exec_()
