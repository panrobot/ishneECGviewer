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
        Form.resize(912, 914)
        Form.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.gridLayout_3 = QtWidgets.QGridLayout(Form)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.scrollArea = QtWidgets.QScrollArea(Form)
        self.scrollArea.setMinimumSize(QtCore.QSize(760, 900))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 1014, 2014))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.graphicsView = GraphicsLayoutWidget(self.scrollAreaWidgetContents)
        self.graphicsView.setMinimumSize(QtCore.QSize(1000, 2000))
        self.graphicsView.setObjectName("graphicsView")
        self.horizontalLayout.addWidget(self.graphicsView)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout_2.addWidget(self.scrollArea)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.gb_channels = QtWidgets.QGroupBox(Form)
        self.gb_channels.setMaximumSize(QtCore.QSize(200, 16777215))
        self.gb_channels.setObjectName("gb_channels")
        self.gb_channels_layout = QtWidgets.QGridLayout(self.gb_channels)
        self.gb_channels_layout.setObjectName("gb_channels_layout")
        self.verticalLayout.addWidget(self.gb_channels)
        self.btn_allLeads = QtWidgets.QPushButton(Form)
        self.btn_allLeads.setEnabled(False)
        self.btn_allLeads.setMinimumSize(QtCore.QSize(130, 0))
        self.btn_allLeads.setCheckable(True)
        self.btn_allLeads.setObjectName("btn_allLeads")
        self.verticalLayout.addWidget(self.btn_allLeads)
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
        self.btn_allLeads.setText(_translate("Form", "Check All Leads"))
        self.btn_chart.setText(_translate("Form", "Redraw ECG"))
        self.btn_openFile.setText(_translate("Form", "Open file"))

from pyqtgraph import GraphicsLayoutWidget
