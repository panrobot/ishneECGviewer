
import sys
from ecgReader import ECG
from gui import Ui_Form
from PyQt5 import QtCore, QtGui, QtWidgets
from datetime import timedelta, datetime
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange
import time
import pyqtgraph as pg
import numpy as np
import pandas as pd

class CustomViewBox(pg.ViewBox):
    def __init__(self, *args, **kwds):
        pg.ViewBox.__init__(self, *args, **kwds)
        self.setMouseMode(self.RectMode)
        
    ## reimplement right-click to zoom out
    def mouseClickEvent(self, ev):
        if ev.button() == QtCore.Qt.RightButton:
            self.autoRange()
            
    def mouseDragEvent(self, ev):
        if ev.button() == QtCore.Qt.RightButton:
            ev.ignore()
        else:
            pg.ViewBox.mouseDragEvent(self, ev)

class CAxisTime(pg.AxisItem):
    ## Formats axis label to human readable time.
    # @param[in] values List of \c time_t.
    # @param[in] scale Not used.
    # @param[in] spacing Not used.
    def tickStrings(self, values, scale, spacing):
        strns = []
        for x in values:
            try:
                strns.append(time.strftime("%d-%b\n %H:%M:%S", time.localtime(x)))    # time_t --> time.struct_time
            except ValueError:  # Windows can't handle dates before 1970
                strns.append('')
        return strns

class DateAxis(pg.AxisItem):
    def tickStrings(self, values, scale, spacing):
        strns = []
        rng = int(max(values) - min(values))
        
        #if rng < 120:
        #    return pg.AxisItem.tickStrings(self, values, scale, spacing)
        if rng < 3600*24:
            string = r'%H:%M:%S'
            label1 = r'%b %d -'
            label2 = r' %b %d, %Y'
        elif rng >= 3600*24 and rng < 3600*24*30:
            string = r'%d'
            label1 = r'%b - '
            label2 = r'%b, %Y'
        elif rng >= 3600*24*30 and rng < 3600*24*30*24:
            string = r'%b'
            label1 = r'%Y -'
            label2 = r' %Y'
        elif rng >=3600*24*30*24:
            string = r'%Y'
            label1 = ''
            label2 = ''
        for x in values:
            try:
                strns.append(time.strftime(string, time.localtime(x)))
                #strns.append(datetime.fromtimestamp(x).strftime(string))
            except ValueError:  ## Windows can't handle dates before 1970
                strns.append('')
        try:
            label = time.strftime(label1, time.localtime(min(values)))+time.strftime(label2, time.localtime(max(values)))
            #label = datetime.fromtimestamp(min(values)).strftime(label1)+datetime.fromtimestamp(max(values)).strftime(label2)
        except ValueError:
            label = ''
        #self.setLabel(text=label)
        return strns

class appWindow(QtGui.QWidget):
    
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.btn_openFile.clicked.connect(self.getFile)
        self.ui.btn_chart.clicked.connect(self.drawChart)
        
        
    def getFile(self):
        self.filename = QtGui.QFileDialog().getOpenFileName(self, 'Open File', '.', 'ECG files (*.ecg)')
        if self.filename != None:
            self.ecg = ECG(self.filename[0], 'cp1250')
            self.setWindowTitle('ECG test of {0} {1} taken {2:%Y-%b-%d %H:%M:%S}'.format(self.ecg.patientFirstName, self.ecg.patientLastName, self.ecg.datetimeStartOfTest))
            if self.ecg.numberOfLeads <= 10:
                j = 0
                positions = [(i,j) for i in range(0,self.ecg.numberOfLeads)]
            else:
                positions = [(i,j) for i in range(0,10) for j in range (0,2)]
            if len(positions) > self.ecg.numberOfLeads:
                for k in range(0,len(positions)-self.ecg.numberOfLeads):
                    positions.pop()
            axis = CAxisTime(orientation='bottom')
            self.plot = pg.PlotItem(axisItems={'bottom': axis}, enableMenu=False)
            self.curves = []
            self.leads = {}
            for idx, (position, lead) in enumerate(zip(positions, self.ecg.leadsNames)):
                #c = pg.PlotCurveItem(pen=(idx, self.ecg.numberOfLeads*1.3), name=lead)
                self.leads[lead] = idx
                #self.plot.addItem(c)
                #c.setPos(0,idx*6)
                #self.curves.append(c)
                self.checkbox = QtWidgets.QCheckBox(lead, self.ui.gb_channels)
                self.checkbox.setObjectName(lead)
                #self.checkbox.stateChanged.connect(self.drawChart)
                self.ui.gb_channels_layout.addWidget(self.checkbox, position[0], position[1])
            checkbox = self.ui.gb_channels.findChild(QtWidgets.QCheckBox, self.ecg.leadsNames[0])
            checkbox.toggle()
            
    def drawChart(self):
        leads = []
        for chbox in self.ui.gb_channels.findChildren(QtWidgets.QCheckBox):
            if chbox.isChecked():
                leads.append(self.leads[chbox.objectName()])
        #indexes = drange(self.ecg.datetimeStartOfTest, self.ecg.datetimeEndOfTest, timedelta(seconds=1/self.ecg.samplingRate))
        Freq = str(int((1/self.ecg.samplingRate)*10**9)) + 'N'
        #indexes = np.arange(self.ecg.datetimeStartOfTest, self.ecg.datetimeEndOfTest,timedelta(seconds=1/self.ecg.samplingRate))
        indexes = np.arange(self.ecg.datetimeStartOfTest.timestamp(), self.ecg.datetimeEndOfTest.timestamp(),1/self.ecg.samplingRate)
        if len(indexes) > len(self.ecg.ecgInChannels[0]):
            indexes = indexes[0:len(self.ecg.ecgInChannels[0])]
        #self.ui.graphicsView.plot(indexes, self.ecg.ecgInChannels[0].reshape(-1))
        
        step = 20*self.ecg.samplingRate
        winsize = 100000 / step * 100
        #winsize = int(len(indexes) / step)*100
        self.ui.graphicsView.setMinimumSize(QtCore.QSize(1000,winsize))
        ecg = self.ecg.ecgInChannels[6].reshape(-1)
        self.ui.graphicsView.clear()
        #len(indexes)-step
        
        for idx, i in enumerate(range(0, 100000, step)):
             axis1 = DateAxis(orientation='bottom')
             axis = CAxisTime(orientation='bottom')
             for n, lead in enumerate(leads):
                 c = pg.PlotCurveItem(pen=(n, self.ecg.numberOfLeads*1.3), name=lead)
                 c.setData(x=indexes[i:i+step-1:2], y=ecg[i:i+step-1:2])
                 self.plot.addItem(c)
                 c.setPos(0,2*(n+1)*self.ecg.leadsResolution[0])
             self.plot = self.ui.graphicsView.addPlot(row=idx, col=0, axisItems={'bottom': axis}, enableMenu=False)
             #p = self.ui.graphicsView.addPlot(axisItems={'bottom': axis}, enableMenu=False, name=self.ecg.leadNamesDict[lead])
             self.plot.setYRange(-2*self.ecg.leadsResolution[0]*len(leads), 2*self.ecg.leadsResolution[0]*len(leads))
             self.plot.setXRange(indexes[i], indexes[i+step-1])
             self.plot.disableAutoRange()
             self.plot.setMouseEnabled(x=False, y=False)
             #p.plot(x=indexes[i:i+step-1:2], y=ecg[i:i+step-1:2])
             #self.ui.graphicsView.nextRow()
             
        
            
        
            
            
        
        
        

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = appWindow()
    window.show()
    
    sys.exit(app.exec_())
