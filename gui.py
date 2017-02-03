# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(781, 588)
        self.gridLayout_3 = QtWidgets.QGridLayout(Form)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.graphicsView = PlotWidget(Form)
        self.graphicsView.setObjectName("graphicsView")
        self.horizontalLayout_2.addWidget(self.graphicsView)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.gb_channels = QtWidgets.QGroupBox(Form)
        self.gb_channels.setMaximumSize(QtCore.QSize(200, 16777215))
        self.gb_channels.setObjectName("gb_channels")
        self.gb_channels_layout = QtWidgets.QGridLayout(self.gb_channels)
        self.gb_channels_layout.setObjectName("gb_channels_layout")
        self.verticalLayout.addWidget(self.gb_channels)
        self.btn_chart = QtWidgets.QPushButton(Form)
        self.btn_chart.setObjectName("btn_chart")
        self.verticalLayout.addWidget(self.btn_chart)
        self.btn_openFile = QtWidgets.QPushButton(Form)
        self.btn_openFile.setObjectName("btn_openFile")
        self.verticalLayout.addWidget(self.btn_openFile)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.gridLayout_3.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.gb_channels.setTitle(_translate("Form", "Channels"))
        self.btn_chart.setText(_translate("Form", "Redraw ECG"))
        self.btn_openFile.setText(_translate("Form", "Open file"))

from pyqtgraph import PlotWidget
