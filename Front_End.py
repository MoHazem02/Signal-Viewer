from PyQt5 import QtCore, QtGui, QtWidgets
from pyqtgraph import PlotWidget
import sys
import pyautogui
from PIL import ImageGrab
import time
import Graph_Class



class Ui_MainWindow(object):

    def __init__(self): 
        # Be careful there is a difference between Graph_1 and Graph_One. The first one is an object of the class we created, but the second one is the name
        # of the plot widget of the Top Graph.
        self.Graph_1 = Graph_Class.Graph(1, self, None)
        self.Graph_2 = Graph_Class.Graph(2, self, None)
        # Every graph has to be able to access the other one as they can be Linked
        self.Graph_1.Other_Graph = self.Graph_2
        self.Graph_2.Other_Graph = self.Graph_1
        self.Snapshots_Count = 0

    def Take_Snapshot(self):
        #Shortcut to take screenshot
        pyautogui.hotkey("win", "shift", "s")
        #wait till user takes screenshot
        time.sleep(6)
        snapshot = ImageGrab.grabclipboard()    
		# Save the image to Snapshots folder
        snapshot.save(f'Snapshots/image{self.Snapshots_Count}.png', 'PNG')

    def Move_Signal(self, number):
        if number == 1:
            self.Graph_1.Update_Current_Channel()
            signal = self.Graph_1.CHANNELS[self.Graph_1.Current_Channel - 1].Signal
            self.Graph_2.Add_Signal(signal)
            signal.Plot_Signal()  # Start plotting the signal in the new graph
            self.Graph_1.Remove_Signal(self.Graph_1.Current_Channel)
        else:
            self.Graph_2.Update_Current_Channel()
            signal = self.Graph_2.CHANNELS[self.Graph_2.Current_Channel - 1].Signal
            self.Graph_2.Remove_Signal(self.Graph_2.Current_Channel)
            self.Graph_1.Add_Signal(signal)
            signal.Plot_Signal()  # Start plotting the signal in the new graph
            
    def Link_Unlink(self):
        # We basically toggle what is already there
        self.Graph_1.Linked = not self.Graph_1.Linked
        self.Graph_2.Linked = not self.Graph_2.Linked

        plot_item_1 = self.Graph_1.Graph_Window.getPlotItem()
        plot_item_2 = self.Graph_2.Graph_Window.getPlotItem()

        if self.Graph_1.Linked:
            plot_item_2.setXLink(plot_item_1)
        else:
            plot_item_2.setXLink(None)
            
    def reset_checkbox(self):
        self.Graph_1.Update_Current_Channel()
        signal = self.Graph_1.CHANNELS[self.Graph_1.Current_Channel - 1].Signal
        if signal and signal.hide:
            self.Hide_Signal_1.setChecked(True)
        else:
            self.Hide_Signal_1.setChecked(False)
        self.Hide_Signal_1.setEnabled(signal is not None)
        
        
    def rewind_signal_1(self):
        # Rewind the signal
        self.Graph_1.CHANNELS[self.Graph_1.Current_Channel - 1].Signal.i = 0
        self.Graph_1.CHANNELS[self.Graph_1.Current_Channel - 1].Signal.Update_Plot_Data()
        # Disable the Rewind button
        self.Rewind_1.setEnabled(False)
    
    def rewind_signal_2(self):
        # Rewind the signal
        self.Graph_2.CHANNELS[self.Graph_2.Current_Channel - 1].Signal.i = 0
        self.Graph_2.CHANNELS[self.Graph_2.Current_Channel - 1].Signal.Update_Plot_Data()
        # Disable the Rewind button
        self.Rewind_2.setEnabled(False)


        
    def scroll_signal(self, value):
        # Calculate the corresponding index based on the scrollbar's value
        index = min(int(value / self.horizontalScrollBar.maximum() * len(self.Graph_1.CHANNELS[self.Graph_1.Current_Channel - 1].Signal.X_Coordinates)), len(self.Graph_1.CHANNELS[self.Graph_1.Current_Channel - 1].Signal.X_Coordinates) - 1)

        # Update the plot data
        self.Graph_1.CHANNELS[self.Graph_1.Current_Channel - 1].Signal.i = index
        self.Graph_1.CHANNELS[self.Graph_1.Current_Channel - 1].Signal.Update_Plot_Data()

        # Update the X range of the plot
        self.Graph_1.CHANNELS[self.Graph_1.Current_Channel - 1].Signal.Graph_Widget.getViewBox().setXRange(max(self.Graph_1.CHANNELS[self.Graph_1.Current_Channel - 1].Signal.X_Coordinates[0 : index + 1]) - 100, max(self.Graph_1.CHANNELS[self.Graph_1.Current_Channel - 1].Signal.X_Coordinates[0 : index + 1]))


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1635, 853)
        MainWindow.setStyleSheet("background-color: #1e1e2f;\n""color:white;")
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
        
        # Connect the currentIndexChanged signal to a function
        self.Channels_of_Graph_1.currentIndexChanged.connect(self.Graph_1.Reset)
        self.Channels_of_Graph_1.currentIndexChanged.connect(self.reset_checkbox)
        self.horizontalScrollBar = QtWidgets.QScrollBar(self.groupBox)
        self.horizontalScrollBar.setEnabled(False)
        self.horizontalScrollBar.setGeometry(QtCore.QRect(220, 290, 1041, 16))
        self.horizontalScrollBar.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalScrollBar.setObjectName("horizontalScrollBar")
        #self.horizontalScrollBar.valueChanged.disconnect(self.scroll_signal)
        # Connect the scroll bar's valueChanged signal to a function
        self.horizontalScrollBar.valueChanged.connect(self.scroll_signal)
        
        self.Play_Pause_1 = QtWidgets.QPushButton(self.groupBox, clicked = lambda : self.Graph_1.CHANNELS[self.Graph_1.Current_Channel - 1].Signal.toggle_play_pause())
        self.Play_Pause_1.setGeometry(QtCore.QRect(10, 130, 191, 31))
        self.Play_Pause_1.setStyleSheet("background-color:#3366ff;")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Assets/pause-play.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Play_Pause_1.setIcon(icon)
        self.Play_Pause_1.setObjectName("Play_Pause_1")
        self.Rewind_1 = QtWidgets.QPushButton(self.groupBox)
        self.Rewind_1.setGeometry(QtCore.QRect(10, 180, 191, 31))
        self.Rewind_1.setStyleSheet("background-color:#3366ff;")
        
        # Connect the Rewind button's clicked signal to a function
        self.Rewind_1.clicked.connect(self.rewind_signal_1)
        # Disable the Rewind button initially
        self.Rewind_1.setEnabled(False)
        
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("Assets/rewind.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Rewind_1.setIcon(icon1)
        self.Rewind_1.setObjectName("Rewind_1")
        # self.Edit_Button_1 = QtWidgets.QPushButton(self.groupBox)
        # self.Edit_Button_1.setGeometry(QtCore.QRect(1280, 110, 101, 31))
        # self.Edit_Button_1.setStyleSheet("background-color:#3366ff;")
        # self.Edit_Button_1.setObjectName("Edit_Button_1")
        self.Edit_Label_1 = QtWidgets.QPushButton(self.groupBox, clicked = lambda: self.Show_Line_Edit(self.groupBox, 1))
        self.Edit_Label_1.setGeometry(QtCore.QRect(1280, 110, 101, 31))
        self.Edit_Label_1.setStyleSheet("background-color:#3366ff;")
        self.Edit_Label_1.setObjectName("Edit_Label_1")
        self.Select_Color_1 = QtWidgets.QPushButton(self.groupBox, clicked = lambda : self.Graph_1.Change_Color())
        self.Select_Color_1.setGeometry(QtCore.QRect(1280, 150, 101, 31))
        self.Select_Color_1.setStyleSheet("background-color:#3366ff;")
        self.Select_Color_1.setObjectName("Select_Color_1")
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
        self.horizontalSlider.valueChanged.connect(lambda: self.Graph_1.Cine_Speed(self.horizontalSlider.value()))
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
        self.Select_Color_2 = QtWidgets.QPushButton(self.groupBox, clicked = lambda : self.Graph_2.Change_Color())
        self.Select_Color_2.setGeometry(QtCore.QRect(1280, 460, 101, 31))
        self.Select_Color_2.setStyleSheet("background-color:#3366ff;")
        self.Select_Color_2.setObjectName("Select_Color_2")
        self.Channels_of_Graph_2 = QtWidgets.QComboBox(self.groupBox)
        self.Channels_of_Graph_2.setGeometry(QtCore.QRect(1280, 370, 221, 31))
        self.Channels_of_Graph_2.setStyleSheet("background-color:#3366ff;")
        self.Channels_of_Graph_2.setObjectName("comboBox_4")
        self.Channels_of_Graph_2.addItem("")
        self.Move_of_Graph_2 = QtWidgets.QPushButton(self.groupBox, clicked=lambda: self.Move_Signal(2))
        self.Move_of_Graph_2.setGeometry(QtCore.QRect(1280, 500, 101, 31))
        self.Move_of_Graph_2.setStyleSheet("background-color:#3366ff;")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("Assets/move-to.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Move_of_Graph_2.setIcon(icon2)
        self.Move_of_Graph_2.setObjectName("Graph2_Move")
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(1340, 340, 111, 16))
        self.label_4.setObjectName("label_4")
        self.Edit_Button_2 = QtWidgets.QPushButton(self.groupBox)
        self.Edit_Button_2.setGeometry(QtCore.QRect(1280, 420, 101, 31))
        self.Edit_Button_2.setStyleSheet("background-color:#3366ff;")
        self.Edit_Button_2.setObjectName("Edit_Button_2")
        self.Add_Channel_of_Graph_2 = QtWidgets.QPushButton(self.groupBox, clicked=lambda: self.Graph_2.Add_Channel())
        self.Add_Channel_of_Graph_2.setGeometry(QtCore.QRect(1390, 470, 111, 31))
        self.Add_Channel_of_Graph_2.setStyleSheet("background-color:#3366ff;")
        self.Add_Channel_of_Graph_2.setObjectName("pushButton_23")
        self.lcdNumber_2 = QtWidgets.QLCDNumber(self.groupBox)
        self.lcdNumber_2.setGeometry(QtCore.QRect(1480, 570, 64, 23))
        self.lcdNumber_2.setObjectName("lcdNumber_2")
        self.horizontalSlider_2 = QtWidgets.QSlider(self.groupBox)
        self.horizontalSlider_2.valueChanged.connect(lambda: self.Graph_2.Cine_Speed(self.horizontalSlider_2.value()))
        self.horizontalSlider_2.setGeometry(QtCore.QRect(1270, 570, 201, 21))
        self.horizontalSlider_2.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_2.setObjectName("horizontalSlider_2")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(1320, 550, 111, 21))
        self.label_2.setObjectName("label_2")
        self.Link_Button = QtWidgets.QPushButton(self.groupBox, clicked = lambda: self.Link_Unlink())
        self.Link_Button.setGeometry(QtCore.QRect(10, 300, 191, 31))
        self.Link_Button.setStyleSheet("background-color:#3366ff;")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("Assets/link1.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Link_Button.setIcon(icon3)
        self.Link_Button.setObjectName("Link_Button")
        self.Hide_Signal_1 = QtWidgets.QCheckBox(self.groupBox)
        self.Hide_Signal_1.clicked.connect(lambda: self.Graph_1.Toggle_Hide_Unhide())
        self.Hide_Signal_1.setGeometry(QtCore.QRect(1400, 200, 111, 20))
        self.Hide_Signal_1.setObjectName("Hide_Signal_1")
        
       
            
        self.Hide_Signal_2 = QtWidgets.QCheckBox(self.groupBox)
        self.Hide_Signal_2.setGeometry(QtCore.QRect(1400, 510, 111, 20))
        self.Hide_Signal_2.setObjectName("Hide_Signal_2")
        self.Load1_Button = QtWidgets.QPushButton(self.groupBox, clicked=lambda: self.Graph_1.Browse_Signals())
        self.Load1_Button.setGeometry(QtCore.QRect(10, 80, 191, 31))
        self.Load1_Button.setStyleSheet("background-color:#3366ff;")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("Assets/load1.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Load1_Button.setIcon(icon4)
        self.Load1_Button.setObjectName("Load1_Button")
        self.Move_of_Graph_1 = QtWidgets.QPushButton(self.groupBox, clicked=lambda: self.Move_Signal(1))
        self.Move_of_Graph_1.setGeometry(QtCore.QRect(1280, 190, 101, 31))
        self.Move_of_Graph_1.setStyleSheet("background-color:#3366ff;")
        self.Move_of_Graph_1.setIcon(icon2)
        self.Move_of_Graph_1.setObjectName("Graph1_Move")
        self.Rewind_2 = QtWidgets.QPushButton(self.groupBox)
        self.Rewind_2.setGeometry(QtCore.QRect(10, 490, 191, 31))
        self.Rewind_2.setStyleSheet("background-color:#3366ff;")
        self.Rewind_2.clicked.connect(self.rewind_signal_2)
        self.Rewind_2.setEnabled(False)
        self.Rewind_2.setIcon(icon1)
        self.Rewind_2.setObjectName("Rewind_2")
        self.Play_Pause_2 = QtWidgets.QPushButton(self.groupBox, clicked = lambda : self.Graph_2.CHANNELS[self.Graph_2.Current_Channel - 1].Signal.toggle_play_pause())
        self.Play_Pause_2.setGeometry(QtCore.QRect(10, 440, 191, 31))
        self.Play_Pause_2.setStyleSheet("background-color:#3366ff;")
        self.Play_Pause_2.setIcon(icon)
        self.Play_Pause_2.setObjectName("Play_Pause_2")
        self.Load2_Button = QtWidgets.QPushButton(self.groupBox, clicked=lambda: self.Graph_2.Browse_Signals())
        self.Load2_Button.setGeometry(QtCore.QRect(10, 390, 191, 31))
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
        
        # Create the QLineEdit widget for the legend name
        self.lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit.setGeometry(QtCore.QRect(1390, 110, 113, 31))  # Adjust the position and size as needed
        self.lineEdit.setStyleSheet("border: 1px solid blue\n"";")
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setReadOnly(True)  # Make the QLineEdit widget read-only initially
        self.Graph_1.textbox = self.lineEdit

        # Create the "Edit Label" button
        self.Edit_Label_1 = QtWidgets.QPushButton(self.groupBox, clicked = lambda: self.Graph_1.Add_Legend())
        self.Edit_Label_1.setGeometry(QtCore.QRect(1280, 110, 101, 31))  # Adjust the position and size as needed
        self.Edit_Label_1.setStyleSheet("background-color:#3366ff;")
        self.Edit_Label_1.setObjectName("Edit_Label_1")

        # Connect the clicked signal of the "Edit Label" button to the Enable_Line_Edit function
        self.Edit_Label_1.clicked.connect(self.Graph_1.Enable_Line_Edit)

        # Connect the returnPressed signal of the QLineEdit to the add_legend function
        self.lineEdit.returnPressed.connect(self.Graph_1.Add_Legend)

        self.lineEdit_2 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_2.setGeometry(QtCore.QRect(1390, 420, 113, 31))
        self.lineEdit_2.setStyleSheet("border: 1px solid blue\n"";")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.ZoomOutTop = QtWidgets.QPushButton(self.groupBox, clicked = lambda: self.Graph_1.ZoomOut())
        self.ZoomOutTop.setGeometry(QtCore.QRect(10, 230, 51, 31))
        self.ZoomOutTop.setStyleSheet("background-color:#3366ff;")
        self.ZoomOutTop.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("Assets/zoom-out.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ZoomOutTop.setIcon(icon5)
        self.ZoomOutTop.setObjectName("ZoomOutTop")
        self.ZoomInTop = QtWidgets.QPushButton(self.groupBox, clicked = lambda: self.Graph_1.ZoomIn())
        self.ZoomInTop.setGeometry(QtCore.QRect(150, 230, 51, 31))
        self.ZoomInTop.setStyleSheet("background-color:#3366ff;")
        self.ZoomInTop.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("Assets/zoomin.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ZoomInTop.setIcon(icon6)
        self.ZoomInTop.setObjectName("ZoomInTop")
        self.ZoomOutBottom = QtWidgets.QPushButton(self.groupBox, clicked = lambda: self.Graph_2.ZoomOut())
        self.ZoomOutBottom.setGeometry(QtCore.QRect(10, 540, 51, 31))
        self.ZoomOutBottom.setStyleSheet("background-color:#3366ff;")
        self.ZoomOutBottom.setText("")
        self.ZoomOutBottom.setIcon(icon5)
        self.ZoomOutBottom.setObjectName("ZoomOutBottom")
        self.ZoomInBottom = QtWidgets.QPushButton(self.groupBox, clicked = lambda: self.Graph_2.ZoomIn())
        self.ZoomInBottom.setGeometry(QtCore.QRect(150, 540, 51, 31))
        self.ZoomInBottom.setStyleSheet("background-color:#3366ff;")
        self.ZoomInBottom.setText("")
        self.ZoomInBottom.setIcon(icon6)
        self.ZoomInBottom.setObjectName("ZoomInBottom")


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
        self.horizontalSlider.valueChanged['int'].connect(self.lcdNumber.display)
        self.horizontalSlider_2.valueChanged['int'].connect(self.lcdNumber_2.display)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.Graph_1.Graph_Window = self.Graph_One
        self.Graph_2.Graph_Window = self.Graph_Two

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
        self.Play_Pause_1.setText(_translate("MainWindow", "   Play/Pause "))
        self.Rewind_1.setText(_translate("MainWindow", "  Rewind     "))
        # self.Edit_Button_1.setText(_translate("MainWindow", "Edit Label"))
        self.Select_Color_1.setText(_translate("MainWindow", "Select Color"))
        self.Edit_Label_1.setText(_translate("MainWindow", "Edit Label"))
        self.Select_Color_1.setText(_translate("MainWindow", "Select Color"))
        self.Add_Channel_of_Graph_1.setText(_translate("MainWindow", "Add Channel"))
        self.label.setText(_translate("MainWindow", "Cine Speed"))
        self.label_3.setText(_translate("MainWindow", "Graph 1"))
        self.Select_Color_2.setText(_translate("MainWindow", "Select Color"))
        self.Channels_of_Graph_2.setItemText(0, _translate("MainWindow", "Channel 1"))
        self.Move_of_Graph_1.setText(_translate("MainWindow", "  Move"))
        self.label_4.setText(_translate("MainWindow", "Graph 2"))
        self.Edit_Button_2.setText(_translate("MainWindow", "Edit Label"))
        self.Add_Channel_of_Graph_2.setText(_translate("MainWindow", "Add Channel"))
        self.label_2.setText(_translate("MainWindow", "Cine Speed"))
        self.Link_Button.setText(_translate("MainWindow", "    Link / Unlink Graphs"))
        self.Hide_Signal_1.setText(_translate("MainWindow", "Hide Signal"))
        self.Hide_Signal_2.setText(_translate("MainWindow", "Hide Signal"))
        self.Load1_Button.setText(_translate("MainWindow", "  Load Signal"))
        self.Move_of_Graph_2.setText(_translate("MainWindow", "  Move"))
        self.Rewind_2.setText(_translate("MainWindow", "  Rewind     "))
        self.Play_Pause_2.setText(_translate("MainWindow", "   Play/Pause "))
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