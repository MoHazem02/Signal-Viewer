from PyQt5 import QtWidgets
from pyqtgraph import PlotDataItem
from PyQt5.QtWidgets import QFileDialog
import wfdb, Signal_Class
import numpy as np
from Channel_Class import Channel



class Graph:
    def __init__(self, Graph_Number, ui_mainwindow, graph_window = None):
        self.channel_count = 1
        self.signal_count = 0
        self.graph_number = Graph_Number
        self.UI_Window = ui_mainwindow
        self.Graph_Window = graph_window
        self.Current_Channel = 1
        self.CHANNELS = []
        self.Signal_Plotter = None
        self.First_Channel = Channel(1)
        self.CHANNELS.append(self.First_Channel)

    def Plot_Signal(self, signal):
        self.Graph_Window.plot(x = signal.X_Coordinates, y = signal.Y_Coordinates, pen = signal.color, name="temp_Signal")
        

    def Update_Current_Channel(self): 
        if self.graph_number == 1:
            self.Current_Channel = int(str(self.UI_Window.Channels_of_Graph_1.currentText())[-1])
        else:
            self.Current_Channel = int(str(self.UI_Window.Channels_of_Graph_2.currentText())[-1])

    def Remove_Signal(self, signal):
        #self.Graph_Window.removeItem(signal)
        #self.Graph_Window.clear()
        PlotDataItem = self.Signal_Plotter.getPlotItem()
        self.Signal_Plotter.removeItem(PlotDataItem)
        self.Signals.remove(signal)
        self.Graph_Window.update()
        self.signal_count -= 1


    def Add_Signal(self, signal):
        if self.channel_count == self.signal_count:
            new_Channel = self.Add_Channel()
            new_Channel.Signal = signal
        else:
            for channel in self.CHANNELS:
                if channel.Signal is None:
                    channel.Signal = signal     
                    break
        self.signal_count += 1
        if self.graph_number == 1:
            self.UI_Window.horizontalScrollBar.setEnabled(True)
        else:
            self.UI_Window.horizontalScrollBar_2.setEnabled(True)

                
    def Add_Channel(self):
        self.channel_count += 1
        Temporary_String = f"Channel {self.channel_count}"
        if self.graph_number == 1:
            self.UI_Window.Channels_of_Graph_1.addItem(Temporary_String)
        else:
            self.UI_Window.Channels_of_Graph_2.addItem(Temporary_String) 
        new_Channel = Channel(self.channel_count)
        self.CHANNELS.append(new_Channel)
        return new_Channel

    
    def change_color(self):
        
        color = QtWidgets.QColorDialog.getColor()

        if color.isValid():
            # Set the selected color to the line
            self.Update_Current_Channel()
            signal = self.CHANNELS[self.Current_Channel - 1].Signal
            signal.color = color
            self.Plot_Signal(signal)


    def Browse_Signals(self):
        File_Path, _ = QFileDialog.getOpenFileName(None, "Browse Signal", "" , "All Files (*)")
        Record = wfdb.rdrecord(File_Path[:-4])
        Y_Coordinates = list(Record.p_signal[:,0])
        X_Coordinates = list(np.arange(len(Y_Coordinates)))
        Sample_Signal = Signal_Class.Signal(col = "g", X_List = X_Coordinates, Y_list = Y_Coordinates, graph = self.graph_number)
        self.Add_Signal(Sample_Signal)
        self.Plot_Signal(Sample_Signal)   
     

    def ZoomIn(self):
        pass


    def ZoomOut(self):
        pass