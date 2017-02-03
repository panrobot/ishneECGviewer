
import sys
from ecgReader import ECG
from gui import Ui_Form
from PyQt5 import QtCore, QtGui, QtWidgets
from datetime import timedelta, datetime
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange

class appWindow(QtGui.QWidget):
    
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.btn_openFile.clicked.connect(self.getFile)
        
        
    def getFile(self):
        self.filename = QtGui.QFileDialog().getOpenFileName(self, 'Open File', '.', 'ECG files (*.ecg)')
        if self.filename != None:
            self.ecg = ECG(self.filename[0], 'cp1250')
            if self.ecg.numberOfLeads <= 10:
                j = 0
                positions = [(i,j) for i in range(0,self.ecg.numberOfLeads)]
            else:
                positions = [(i,j) for i in range(0,10) for j in range (0,2)]
            if len(positions) > self.ecg.numberOfLeads:
                for k in range(0,len(positions)-self.ecg.numberOfLeads):
                    positions.pop()
            
            for idx, (position, lead) in enumerate(zip(positions, self.ecg.leadsNames)):
                self.checkbox = QtWidgets.QCheckBox(lead, self.ui.gb_channels)
                self.checkbox.setObjectName(lead)
                self.checkbox.stateChanged.connect(self.drawChart)
                self.ui.gb_channels_layout.addWidget(self.checkbox, position[0], position[1])
            checkbox = self.ui.gb_channels.findChild(QtWidgets.QCheckBox, self.ecg.leadsNames[0])
            checkbox.toggle()
            
    def drawChart(self):
        indexes = drange(self.ecg.datetimeStartOfTest, self.ecg.datetimeEndOfTest, timedelta(seconds=1/self.ecg.samplingRate))
        if len(indexes) > len(self.ecg.ecgInChannels[0]):
            indexes = indexes[0:len(self.ecg.ecgInChannels[0])]
        self.ui.graphicsView.plot(indexes, self.ecg.ecgInChannels[0].reshape(-1))
        
        
        

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = appWindow()
    window.show()
    
    sys.exit(app.exec_())
