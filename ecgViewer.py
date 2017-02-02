
import sys
from ecgReader import ECG
from gui import Ui_Form
from PyQt5 import QtCore, QtGui, QtWidgets


class appWindow(QtGui.QWidget):
    
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = appWindow()
    window.show()
    sys.exit(app.exec_())
