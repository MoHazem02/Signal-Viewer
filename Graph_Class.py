from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
import wfdb, Signal_Class
import numpy as np
from Channel_Class import Channel

class Graph:
    def __init__(self, Graph_Number, ui_mainwindow, other_graph, graph_window = None ):
        #self.Signal = Signal 
        self.hidden_lines = []  # Add this line to initialize the list
        self.textbox = None
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
        self.Linked = False # Whether the 2 graphs are linked or not
        self.Other_Graph = other_graph # Reference to the other graph
        self.Current_Frame = 0
        
    
    def Update_Current_Channel(self): 
        if self.graph_number == 1:
            self.Current_Channel = int(str(self.UI_Window.Channels_of_Graph_1.currentText())[-1])
        else:
            self.Current_Channel = int(str(self.UI_Window.Channels_of_Graph_2.currentText())[-1])

    def Remove_Signal(self, channel_number):
        # Get the channel
        channel = self.CHANNELS[channel_number - 1]

        # Check if the channel has a signal
        if channel.Signal is not None:
            # Remove the signal's line from the plot
            self.Graph_Window.removeItem(channel.Signal.data_line)
            # Disable the auto-range feature
            self.Graph_Window.getViewBox().setAutoPan(False)

            # Reset the x-axis
            self.Graph_Window.getViewBox().setXRange(0, 1)

            # Remove the signal's legend from the plot
            if channel.Signal.legend:
                for item in channel.Signal.legend.items:
                    if item[1].text == channel.Signal.data_line.name():
                        channel.Signal.legend.removeItem(item[1].text)
                        break

            # Set the channel's signal to None
            channel.Signal = None

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
            self.Enable_Line_Edit()
        else:
            self.UI_Window.horizontalScrollBar_2.setEnabled(True)
            self.Enable_Line_Edit()
                
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

    def Change_Color(self):
        
        color = QtWidgets.QColorDialog.getColor()

        if color.isValid():
            # Set the selected color to the line
            self.Update_Current_Channel()
            signal = self.CHANNELS[self.Current_Channel - 1].Signal
            signal.color = color
            signal.data_line.setPen(color)  # Change the color of the line directly
            #signal.data_line.legend_color.setPen(color)      
            
    def Browse_Signals(self):
        File_Path, _ = QFileDialog.getOpenFileName(None, "Browse Signal", "" , "All Files (*)")
        Record = wfdb.rdrecord(File_Path[:-4])
        Y_Coordinates = list(Record.p_signal[:,0])
        X_Coordinates = list(np.arange(len(Y_Coordinates)))
        Sample_Signal = Signal_Class.Signal(col = "g", X_List = X_Coordinates, Y_list = Y_Coordinates, graphWdg = self.Graph_Window, graphObj = self)
        self.Add_Signal(Sample_Signal)
        Sample_Signal.Plot_Signal() 
     
    def ZoomIn(self):
        self.Graph_Window.getViewBox().scaleBy((0.9, 0.9))
        if self.Linked:
            self.Other_Graph.Graph_Window.getViewBox().scaleBy((0.9, 0.9))

    def ZoomOut(self):
        self.Graph_Window.getViewBox().scaleBy((1.1, 1.1))
        if self.Linked:
            self.Other_Graph.Graph_Window.getViewBox().scaleBy((1.1, 1.1))     

    def Toggle_Hide_Unhide(self):
        # Get the current channel
        self.Update_Current_Channel()
        self.current_channel = self.CHANNELS[self.Current_Channel - 1]
        # Check if the channel has a signal
        if self.current_channel.Signal is not None:
            # Toggle the visibility of the signal
            if self.current_channel.Signal.hide:
                self.current_channel.Signal.Unhide_Signal()
                if self.graph_number == 1:
                    self.UI_Window.Hide_Signal_1.setChecked(False)
                else:
                    self.UI_Window.Hide_Signal_2.setChecked(False)
            else:
                self.current_channel.Signal.Hide_Signal()
                if self.graph_number == 1:
                    self.UI_Window.Hide_Signal_1.setChecked(True)
                else:
                    self.UI_Window.Hide_Signal_2.setChecked(True)
        else:
            pass

    def Add_Legend(self):
        text = self.textbox.text()
        current_signal = None
        # Get the current signal
        if self.Current_Channel:
            # TODO Each Channel has a signal, don't HASH  #mafrod done, bs hazem recheck
            current_signal = self.CHANNELS[self.Current_Channel - 1].Signal
        else:
            print("No current channel selected.")
            return

        # Check if a current signal was found
        if current_signal is not None:
            # Create a name for the legend
            legend_name = text 

            # Add the signal to the plot with the legend name
            current_signal.data_line = self.Graph_Window.plot(pen=current_signal.color, name=legend_name)

            # Add a legend to the plot
            self.Legend = self.Graph_Window.addLegend()

            # Store the legend in the signal
            current_signal.legend = self.Legend
            current_signal.legend_color = current_signal.color
        else:
            print("No signal found in the current channel.")      
        
    def Enable_Line_Edit(self):
        if self.textbox is not None:
            self.textbox.setReadOnly(False)  # Make the QLineEdit widget editable
            self.textbox.show()  # Make the lineEdit widget visible
        else:
            print("lineEdit widget does not exist")
  
    def Reset(self):
        self.textbox.setReadOnly(True) #reset the textbox until user add a signal
        #self.Toggle_Hide_Unhide()

    def Cine_Speed(self, value):
        for channel in self.CHANNELS:
            channel.Signal.Update_Cine_Speed(value)
        
        if self.Linked:
            for channel in self.Other_Graph.CHANNELS:
                channel.Signal.Update_Cine_Speed(value)
            
            if self.graph_number == 1:
                self.UI_Window.horizontalSlider_2.setValue(value)
            else:
                self.UI_Window.horizontalSlider.setValue(value)
            
                

        

        

