from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QInputDialog, QPushButton, QMainWindow, QLabel, QFileDialog, QApplication
import pyqtgraph as pg
from pyqtgraph import PlotWidget
import numpy as np 
import sys
from pyqtgraph import PlotWidget
import pyautogui
from PIL import ImageGrab
import time
import wfdb
import Signal_Class
import Graph_Class



class Ui_MainWindow(object):

    def __init__(self): 
        # Be careful there is a difference between Graph_1 and Graph_One. The first one is an object of the class we created, but the second one is the name
        # of the plot widget of the Top Graph.
        self.Graph_1 = Graph_Class.Graph(1, self)
        self.Graph_2 = Graph_Class.Graph(2, self)
        self.Snapshots_Count = 0

    def Take_Snapshot(self):
        #Shortcut to take screenshot
        pyautogui.hotkey("win", "shift", "s")
        #wait till user takes screenshot
        time.sleep(6)
        snapshot = ImageGrab.grabclipboard()    
		# Save the image to Snapshots folder
        snapshot.save(f'Snapshots/image{self.Snapshots_Count}.png', 'PNG')
    
   #TODO Update the function based on having 2 buttons
    def Browse_Signals(self, Graph_Number):
        File_Path, _ = QFileDialog.getOpenFileName(self.Load1_Button, "Browse Signal", "" , "All Files (*)")
        Record = wfdb.rdrecord(File_Path[:-4])
        Y_Coordinates = list(Record.p_signal[:,0])
        X_Coordinates = list(np.arange(len(Y_Coordinates)))
        Sample_Signal = Signal_Class.Signal(col = "g", X_List=X_Coordinates, Y_list=Y_Coordinates, graph = Graph_Number)
        self.Graph_1.Graph_Window = self.Graph_One
        self.Graph_2.Graph_Window = self.Graph_Two
        if Graph_Number == 1:
            self.Graph_1.Signals.append(Sample_Signal)
            self.Graph_1.Plot_Signal(Sample_Signal)
        else:
            self.Graph_2.Signals.append(Sample_Signal)
            self.Graph_2.Plot_Signal(Sample_Signal)
        # self.graphicsView.plot(Record.p_signal)
        # self.timer1 = QtCore.QTimer()
        # self.timer1.timeout.connect(lambda: self.update_plot(1, X_Coordinates, Y_Coordinates))
        # self.timer1.start(1000)  # update every second


    def Move_Signal(self, number):
        if number == 1:
            self.Graph_1.Update_Current_Channel()
            #First we grab the signal currently selected by the channel combo box
            signal = self.Graph_1.Signals[self.Graph_1.Current_Channel - 1]
            # Secondly we remove the singal from its current graph
            self.Graph_1.Remove_Signal()
            # Thirdly we add to the other graph a new daugher (our signal :)
            self.Graph_2.Add_Signal(signal)
        else:
            self.Graph_2.Update_Current_Channel()
            #First we grab the signal currently selected by the channel combo box
            signal = self.Graph_2.Signals[self.Graph_2.Current_Channel - 1]
            # Secondly we remove the singal from its current graph
            self.Graph_2.Remove_Signal()
            # Thirdly we add to the other graph a new daugher (our signal :)
            self.Graph_1.Add_Signal(signal)

               
    def update_plot(self, number, x, y):
        # Code to get new data and update the plot
        if number == 1:
            for i in range(len(x)):
                self.graphicsView.plot(x[i], y[i])

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1635, 853)
        MainWindow.setStyleSheet("background-color: #1e1e2f;\n"
"color:white;")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(610, -10, 381, 51))
        self.textBrowser.setStyleSheet("border:none;")
        self.textBrowser.setObjectName("textBrowser")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(40, 40, 1561, 641))
        self.groupBox.setStyleSheet("")
        self.groupBox.setObjectName("groupBox")
        self.Graph_One = PlotWidget(self.groupBox)
        self.Graph_One.setGeometry(QtCore.QRect(220, 30, 1031, 251))
        self.Graph_One.setObjectName("Graph_One")
        self.Channels_of_Graph_1 = QtWidgets.QComboBox(self.groupBox)
        self.Channels_of_Graph_1.setGeometry(QtCore.QRect(1280, 60, 221, 31))
        self.Channels_of_Graph_1.setStyleSheet("background-color:#3366ff;")
        self.Channels_of_Graph_1.setObjectName("comboBox_3")
        self.Channels_of_Graph_1.addItem("") 
        self.horizontalScrollBar = QtWidgets.QScrollBar(self.groupBox)
        self.horizontalScrollBar.setEnabled(False)
        self.horizontalScrollBar.setGeometry(QtCore.QRect(220, 290, 1041, 16))
        self.horizontalScrollBar.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalScrollBar.setObjectName("horizontalScrollBar")
        self.pushButton_8 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_8.setGeometry(QtCore.QRect(10, 130, 191, 31))
        self.pushButton_8.setStyleSheet("background-color:#3366ff;")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Assets/pause-play.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_8.setIcon(icon)
        self.pushButton_8.setObjectName("pushButton_8")
        self.pushButton_9 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_9.setGeometry(QtCore.QRect(10, 180, 191, 31))
        self.pushButton_9.setStyleSheet("background-color:#3366ff;")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("Assets/rewind.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_9.setIcon(icon1)
        self.pushButton_9.setObjectName("pushButton_9")
        self.pushButton_13 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_13.setGeometry(QtCore.QRect(1280, 110, 101, 31))
        self.pushButton_13.setStyleSheet("background-color:#3366ff;")
        self.pushButton_13.setObjectName("pushButton_13")
        self.pushButton_19 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_19.setGeometry(QtCore.QRect(1390, 110, 111, 31))
        self.pushButton_19.setStyleSheet("background-color:#3366ff;")
        self.pushButton_19.setObjectName("pushButton_19")
        self.Add_Channel_of_Graph_1 = QtWidgets.QPushButton(self.groupBox, clicked=lambda: self.Graph_1.Add_Channel())
        self.Add_Channel_of_Graph_1.setGeometry(QtCore.QRect(1390, 160, 111, 31))
        self.Add_Channel_of_Graph_1.setStyleSheet("background-color:#3366ff;")
        self.Add_Channel_of_Graph_1.setObjectName("pushButton_20")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(1320, 240, 111, 21))
        self.label.setObjectName("label")
        self.lcdNumber = QtWidgets.QLCDNumber(self.groupBox)
        self.lcdNumber.setGeometry(QtCore.QRect(1480, 260, 64, 23))
        self.lcdNumber.setObjectName("lcdNumber")
        self.horizontalSlider = QtWidgets.QSlider(self.groupBox)
        self.horizontalSlider.setGeometry(QtCore.QRect(1270, 260, 201, 21))
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.Graph_Two = PlotWidget(self.groupBox)
        self.Graph_Two.setGeometry(QtCore.QRect(220, 330, 1031, 251))
        self.Graph_Two.setObjectName("Graph_2")
        self.horizontalScrollBar_2 = QtWidgets.QScrollBar(self.groupBox)
        self.horizontalScrollBar_2.setEnabled(False)
        self.horizontalScrollBar_2.setGeometry(QtCore.QRect(220, 590, 1041, 16))
        self.horizontalScrollBar_2.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalScrollBar_2.setObjectName("horizontalScrollBar_2")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(1340, 30, 111, 16))
        self.label_3.setObjectName("label_3")
        self.pushButton_22 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_22.setGeometry(QtCore.QRect(1390, 420, 111, 31))
        self.pushButton_22.setStyleSheet("background-color:#3366ff;")
        self.pushButton_22.setObjectName("pushButton_22")
        self.Channels_of_Graph_2 = QtWidgets.QComboBox(self.groupBox)
        self.Channels_of_Graph_2.setGeometry(QtCore.QRect(1280, 370, 221, 31))
        self.Channels_of_Graph_2.setStyleSheet("background-color:#3366ff;")
        self.Channels_of_Graph_2.setObjectName("comboBox_4")
        self.Channels_of_Graph_2.addItem("")
        self.Move_of_Graph_2 = QtWidgets.QPushButton(self.groupBox, clicked=lambda: self.Move_Signal(2))
        self.Move_of_Graph_2.setGeometry(QtCore.QRect(1280, 470, 101, 31))
        self.Move_of_Graph_2.setStyleSheet("background-color:#3366ff;")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("Assets/move-to.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Move_of_Graph_2.setIcon(icon2)
        self.Move_of_Graph_2.setObjectName("Graph2_Move")
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(1340, 340, 111, 16))
        self.label_4.setObjectName("label_4")
        self.pushButton_14 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_14.setGeometry(QtCore.QRect(1280, 420, 101, 31))
        self.pushButton_14.setStyleSheet("background-color:#3366ff;")
        self.pushButton_14.setObjectName("pushButton_14")
        self.Add_Channel_of_Graph_2 = QtWidgets.QPushButton(self.groupBox, clicked=lambda: self.Graph_2.Add_Channel())
        self.Add_Channel_of_Graph_2.setGeometry(QtCore.QRect(1390, 470, 111, 31))
        self.Add_Channel_of_Graph_2.setStyleSheet("background-color:#3366ff;")
        self.Add_Channel_of_Graph_2.setObjectName("pushButton_23")
        self.lcdNumber_2 = QtWidgets.QLCDNumber(self.groupBox)
        self.lcdNumber_2.setGeometry(QtCore.QRect(1480, 570, 64, 23))
        self.lcdNumber_2.setObjectName("lcdNumber_2")
        self.horizontalSlider_2 = QtWidgets.QSlider(self.groupBox)
        self.horizontalSlider_2.setGeometry(QtCore.QRect(1270, 570, 201, 21))
        self.horizontalSlider_2.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_2.setObjectName("horizontalSlider_2")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(1320, 550, 111, 21))
        self.label_2.setObjectName("label_2")
        self.pushButton_10 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_10.setGeometry(QtCore.QRect(10, 300, 191, 31))
        self.pushButton_10.setStyleSheet("background-color:#3366ff;")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("Assets/link1.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_10.setIcon(icon3)
        self.pushButton_10.setObjectName("pushButton_10")
        self.checkBox_2 = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_2.setGeometry(QtCore.QRect(1340, 200, 111, 20))
        self.checkBox_2.setObjectName("checkBox_2")
        self.checkBox_4 = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_4.setGeometry(QtCore.QRect(1350, 510, 111, 20))
        self.checkBox_4.setObjectName("checkBox_4")
        self.Load1_Button = QtWidgets.QPushButton(self.groupBox, clicked=lambda: self.Browse_Signals(1))
        self.Load1_Button.setGeometry(QtCore.QRect(10, 80, 191, 31))
        self.Load1_Button.setStyleSheet("background-color:#3366ff;")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("Assets/load1.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Load1_Button.setIcon(icon4)
        self.Load1_Button.setObjectName("Load1_Button")
        self.Move_of_Graph_1 = QtWidgets.QPushButton(self.groupBox, clicked=lambda: self.Move_Signal(1))
        self.Move_of_Graph_1.setGeometry(QtCore.QRect(1280, 160, 101, 31))
        self.Move_of_Graph_1.setStyleSheet("background-color:#3366ff;")
        self.Move_of_Graph_1.setIcon(icon2)
        self.Move_of_Graph_1.setObjectName("Graph1_Move")
        self.pushButton_25 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_25.setGeometry(QtCore.QRect(10, 520, 191, 31))
        self.pushButton_25.setStyleSheet("background-color:#3366ff;")
        self.pushButton_25.setIcon(icon1)
        self.pushButton_25.setObjectName("pushButton_25")
        self.pushButton_15 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_15.setGeometry(QtCore.QRect(10, 470, 191, 31))
        self.pushButton_15.setStyleSheet("background-color:#3366ff;")
        self.pushButton_15.setIcon(icon)
        self.pushButton_15.setObjectName("pushButton_15")
        self.Load2_Button = QtWidgets.QPushButton(self.groupBox, clicked=lambda: self.Browse_Signals(2))
        self.Load2_Button.setGeometry(QtCore.QRect(10, 420, 191, 31))
        self.Load2_Button.setStyleSheet("background-color:#3366ff;")
        self.Load2_Button.setIcon(icon4)
        self.Load2_Button.setObjectName("Load2_Button")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(40, 690, 1561, 101))
        self.groupBox_2.setObjectName("groupBox_2")
        self.pushButton_11 = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_11.setGeometry(QtCore.QRect(10, 110, 101, 31))
        self.pushButton_11.setStyleSheet("background-color:#3366ff;")
        self.pushButton_11.setObjectName("pushButton_11")
        self.checkBox = QtWidgets.QCheckBox(self.groupBox_2)
        self.checkBox.setGeometry(QtCore.QRect(470, 160, 81, 20))
        self.checkBox.setObjectName("checkBox")
        self.checkBox_3 = QtWidgets.QCheckBox(self.groupBox_2)
        self.checkBox_3.setGeometry(QtCore.QRect(910, 160, 81, 20))
        self.checkBox_3.setObjectName("checkBox_3")
        self.pushButton_12 = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_12.setGeometry(QtCore.QRect(130, 110, 101, 31))
        self.pushButton_12.setStyleSheet("background-color:#3366ff;")
        self.pushButton_12.setObjectName("pushButton_12")
        self.pushButton_21 = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_21.setGeometry(QtCore.QRect(760, 150, 101, 31))
        self.pushButton_21.setStyleSheet("background-color:#3366ff;")
        self.pushButton_21.setObjectName("pushButton_21")
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_2.setGeometry(QtCore.QRect(260, 100, 61, 31))
        self.pushButton_2.setStyleSheet("background-color:#3366ff;")
        self.pushButton_2.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("Assets/zoom-out.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_2.setIcon(icon5)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_17 = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_17.setGeometry(QtCore.QRect(1310, 50, 221, 31))
        self.pushButton_17.setStyleSheet("background-color:#3366ff;")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("Assets/export.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_17.setIcon(icon6)
        self.pushButton_17.setObjectName("pushButton_17")
        self.Snapshot_Button = QtWidgets.QPushButton(self.groupBox_2, clicked=lambda: self.Take_Snapshot())
        self.Snapshot_Button.setGeometry(QtCore.QRect(10, 50, 221, 31))
        self.Snapshot_Button.setStyleSheet("background-color:#3366ff;")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("Assets/snap1.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Snapshot_Button.setIcon(icon7)
        self.Snapshot_Button.setObjectName("Snapshot_Button")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1635, 26))
        self.menubar.setObjectName("menubar")
        self.menuAbout = QtWidgets.QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionLoad_Signal = QtWidgets.QAction(MainWindow)
        self.actionLoad_Signal.setObjectName("actionLoad_Signal")
        self.menubar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(MainWindow)
        self.horizontalSlider.valueChanged['int'].connect(self.lcdNumber.display) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Signal Viewer"))
        self.textBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt; font-weight:600;\">Live Signal Viewer</span></p></body></html>"))
        self.groupBox.setTitle(_translate("MainWindow", "Channels"))
        self.Channels_of_Graph_1.setItemText(0, _translate("MainWindow", "Channel 1"))
        self.pushButton_8.setText(_translate("MainWindow", "   Play         "))
        self.pushButton_9.setText(_translate("MainWindow", "  Rewind     "))
        self.pushButton_13.setText(_translate("MainWindow", "Edit Label"))
        self.pushButton_19.setText(_translate("MainWindow", "Select Color"))
        self.Add_Channel_of_Graph_1.setText(_translate("MainWindow", "Add Channel"))
        self.label.setText(_translate("MainWindow", "Cine Speed"))
        self.label_3.setText(_translate("MainWindow", "Graph 1"))
        self.pushButton_22.setText(_translate("MainWindow", "Select Color"))
        self.Channels_of_Graph_2.setItemText(0, _translate("MainWindow", "Channel 1"))
        self.Move_of_Graph_1.setText(_translate("MainWindow", "  Move"))
        self.label_4.setText(_translate("MainWindow", "Graph 2"))
        self.pushButton_14.setText(_translate("MainWindow", "Edit Label"))
        self.Add_Channel_of_Graph_2.setText(_translate("MainWindow", "Add Channel"))
        self.label_2.setText(_translate("MainWindow", "Cine Speed"))
        self.pushButton_10.setText(_translate("MainWindow", "  Link Graphs"))
        self.checkBox_2.setText(_translate("MainWindow", "Hide Signal"))
        self.checkBox_4.setText(_translate("MainWindow", "Hide Signal"))
        self.Load1_Button.setText(_translate("MainWindow", "  Load Signal"))
        self.Move_of_Graph_2.setText(_translate("MainWindow", "  Move"))
        self.pushButton_25.setText(_translate("MainWindow", "  Rewind     "))
        self.pushButton_15.setText(_translate("MainWindow", "   Play         "))
        self.Load2_Button.setText(_translate("MainWindow", "  Load Signal"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Controls"))
        self.pushButton_11.setText(_translate("MainWindow", "Link Graphs"))
        self.checkBox.setText(_translate("MainWindow", "Hide"))
        self.checkBox_3.setText(_translate("MainWindow", "Hide"))
        self.pushButton_12.setText(_translate("MainWindow", "Export"))
        self.pushButton_21.setText(_translate("MainWindow", "Add Channel"))
        self.pushButton_17.setText(_translate("MainWindow", "  Export"))
        self.Snapshot_Button.setText(_translate("MainWindow", "   Snapshot"))
        self.menuAbout.setTitle(_translate("MainWindow", "About"))
        self.actionLoad_Signal.setText(_translate("MainWindow", "Load Signal"))



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
