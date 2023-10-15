from PyQt5 import QtCore, QtGui, QtWidgets
from pyqtgraph import PlotWidget
from PyQt5.QtWidgets import QFileDialog
import wfdb, Signal_Class
import numpy as np
from Channel_Class import Channel
import fpdf
from fpdf import FPDF

class Graph:
    def __init__(self, Graph_Number, ui_mainwindow, other_graph, scroll_bar = None ,graph_window = None):
        self.signals = []  # Add this line to initialize the list
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
        self.Scroll_Bar = scroll_bar
        
    
    def Update_Current_Channel(self): 
        if self.graph_number == 1:
            self.Current_Channel = int(str(self.UI_Window.Channels_of_Graph_1.currentText())[-1])
        else:
            self.Current_Channel = int(str(self.UI_Window.Channels_of_Graph_2.currentText())[-1])

    def Remove_Signal(self):
        
        self.Update_Current_Channel()

        # Check if the channel has a signal
        if self.CHANNELS[self.Current_Channel-1].Signal:
            # Remove the signal's line from the plot
            self.Graph_Window.removeItem(self.CHANNELS[self.Current_Channel-1].Signal.data_line)
            # Disable the auto-range feature
            self.Graph_Window.getViewBox().setAutoPan(False)

            # Reset the x-axis
            self.Graph_Window.getViewBox().setXRange(0, 1)


            # Remove the signal's legend from the plot
            if self.CHANNELS[self.Current_Channel-1].Signal.legend:
                for item in self.CHANNELS[self.Current_Channel-1].Signal.legend.items:
                    if item[1].text == self.CHANNELS[self.Current_Channel-1].Signal.data_line.name():
                       self.CHANNELS[self.Current_Channel-1].Signal.legend.removeItem(item[1].text)
                       break

            self.signals.remove(self.CHANNELS[self.Current_Channel-1].Signal)
            #Set the channel's signal to None
            self.CHANNELS[self.Current_Channel-1].Signal = None
            self.signal_count -= 1
            #self.reset_signal
            


    def Add_Signal(self, signal): # add the signal to a channel 
       if signal:
            if self.channel_count == self.signal_count:
                new_Channel = self.Add_Channel()
                new_Channel.Signal = signal
                new_Channel.Signal.Graph_Widget = self.Graph_Window
                new_Channel.Signal.Graph_Object = self
                #Add the new signal to the list of signals
                self.signals.append( new_Channel.Signal)
            else:
                for channel in self.CHANNELS:
                    if channel.Signal is None:
                        channel.Signal = signal  
                        channel.Signal.Graph_Widget = self.Graph_Window
                        channel.Signal.Graph_Object = self 
                        #Add the new signal to the list of signals
                        self.signals.append(channel.Signal)
                        break
        
            self.signal_count += 1


            if self.graph_number == 1:
                self.UI_Window.horizontalScrollBar.setEnabled(True)
                self.Enable_Line_Edit()
            else:
                self.UI_Window.horizontalScrollBar_2.setEnabled(True)
                self.Enable_Line_Edit()
            

            # Add the new signal to the list of signals
            # self.signals.append(signal)
            # Reset the current signal and clear the plot window
            self.reset_signal()
                
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
            self.Graph_Window.clear()
            # Set the selected color to the line
            self.Update_Current_Channel()
            signal = self.CHANNELS[self.Current_Channel - 1].Signal
            signal.color = color
            signal.data_line.setPen(color)  # Change the color of the line directly
            for channel in self.CHANNELS:
                channel.Signal.Plot_Signal()
                # Add the signal to the plot with the legend name
                channel.Signal.data_line = self.Graph_Window.plot(pen=channel.Signal.color, name=channel.Signal.legend_text)
            #signal.data_line.legend_color.setPen(color)      
            
    def Browse_Signals(self):
        File_Path, _ = QFileDialog.getOpenFileName(None, "Browse Signal", "" , "All Files (*)")
        Record = wfdb.rdrecord(File_Path[:-4])
        Y_Coordinates = list(Record.p_signal[:,0])
        X_Coordinates = list(np.arange(len(Y_Coordinates)))
        Sample_Signal = Signal_Class.Signal(col = "g", X_List = X_Coordinates, Y_list = Y_Coordinates, graphWdg = self.Graph_Window, graphObj = self)
            
        self.Add_Signal(Sample_Signal)
        #clear old signals for plotting all together
        self.Graph_Window.clear()
        # Plot all signals
        for channel in self.CHANNELS:
            channel.Signal.Plot_Signal()
            if channel.Signal.legend_text:
                channel.Signal.data_line = self.Graph_Window.plot(pen=channel.Signal.color, name=channel.Signal.legend_text)
            #self.update_legend(channel.Signal)
     
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
        
    def update_legend(self, current_signal): # remove this again
        if current_signal.legend_text:
            self.Graph_Window.clear()
             # Add the signal to the plot with the legend name
            current_signal.data_line = self.Graph_Window.plot(pen=current_signal.color, name=current_signal.legend_text)
            # Add a legend to the plot
            current_signal.legend = self.Graph_Window.addLegend()
            # Store the legend color in the signal
            current_signal.legend_color = current_signal.color
            for channel in self.CHANNELS:
                channel.Signal.Plot_Signal()
               
        

    def Add_Legend(self):
        text = self.textbox.text()
        current_signal = None
        self.Update_Current_Channel()
        # Get the current signal
        if self.Current_Channel:
            current_signal = self.CHANNELS[self.Current_Channel - 1].Signal
        else:
            return
        # Check if a current signal was found
        if current_signal is not None and current_signal.legend is None:
            # Create a name for the legend
            current_signal.legend_text = text 
            #self.update_legend(current_signal)
             # Add the signal to the plot with the legend name
            current_signal.data_line = self.Graph_Window.plot(pen=current_signal.color, name=current_signal.legend_text)
            # Add a legend to the plot
            current_signal.legend = self.Graph_Window.addLegend()
            # Store the legend color in the signal
            current_signal.legend_color = current_signal.color
        else:
            # Update the text of the legend
            # Check if a current signal was found
            if current_signal is not None:
                current_signal.legend_text = text
                # Remove the old legend
                if current_signal.legend:
                    self.Graph_Window.removeItem(current_signal.legend)
                    # Clear the plot window
                    self.Graph_Window.clear()
                    for channel in self.CHANNELS:
                        channel.Signal.Plot_Signal()
                        # Add the signal to the plot with the legend name
                        channel.Signal.data_line = self.Graph_Window.plot(pen=channel.Signal.color, name=channel.Signal.legend_text)
                    # Add a legend to the plot
                    current_signal.legend = self.Graph_Window.addLegend()
                    # Store the legend color in the signal
                    current_signal.legend_color = current_signal.color
                    #current_signal.Update_Plot_Data()
                    #self.update_legend(current_signal)
                  
        
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
            
                
    def reset_signal(self):
        # Reset the current signal if another signal is add
        # self.Update_Current_Channel()
        # current_signal = self.CHANNELS[self.Current_Channel - 1].Signal
        # if current_signal is not None:
        #     current_signal.i = 0
        for channel in self.CHANNELS:
            if channel.Signal:
                channel.Signal.i = 0

        # Clear the plot window
        self.Graph_Window.clear()

        # If the graphs are linked, reset all signals in both graphs
        if self.UI_Window.Graph_1.Linked:
            for channel in self.UI_Window.Graph_1.CHANNELS:
                if channel.Signal is not None:
                    channel.Signal.i = 0
                    channel.Signal.Plot_Signal()  # Replot the signal from the beginning

            for channel in self.UI_Window.Graph_2.CHANNELS:
                if channel.Signal is not None:
                    channel.Signal.i = 0
                    channel.Signal.Plot_Signal()  # Replot the signal from the beginning
        
    def toggle_play_pause(self):
        for sig in self.signals:
            sig.pause = not sig.pause
        
        if self.Linked:
            for channel in self.Other_Graph.CHANNELS:
                channel.Signal.pause = not channel.Signal.pause


    def Export_PDF(self):
        #Creating the pdf object 
        pdf = fpdf.FPDF()
        #Adding the first page to the pdf
        pdf.add_page()
        #Adding page break with margin = 15 to open another page when limit is reached
        pdf.set_auto_page_break(auto=1,margin=20)
        #Setting the title of the page style
        pdf.set_font('times','B', 22)
        pdf.cell(0,10,"Signals Data Analysis Report",align="C",ln=1)
        #Updating the current channel number to know which channel is displayed in both graphs
        self.Update_Current_Channel()
        self.Other_Graph.Update_Current_Channel()
        #Checks if the current has a signal 
        if self.CHANNELS[self.Current_Channel-1].Signal :
            #Creating the statistics of the signal
            self.CHANNELS[self.Current_Channel-1].Signal.Creating_Signal_Statistics()
            #Setting the title of the signal style
            pdf.set_font('times','U', 16)
            pdf.cell(0,30,f"Signal of Graph {self.graph_number} Channel {self.Current_Channel} Data: ")
            #Positoning of the image
            pdf.set_xy(10,50)
            pdf.image('Snapshots/Image 0.png', w=190,h=60)
            pdf.ln(10)

            pdf.set_font('times','', 12)
            table_data = [['Maximum Value', 'Minimum Value', 'Mean','Standard Deviation','Duration'], 
                        [self.CHANNELS[self.Current_Channel-1].Signal.Max_Value, self.CHANNELS[self.Current_Channel-1].Signal.Min_Value, 
                        self.CHANNELS[self.Current_Channel-1].Signal.Mean,self.CHANNELS[self.Current_Channel-1].Signal.Standard_Deviation,
                        f"{self.CHANNELS[self.Current_Channel-1].Signal.Duration} min"]]

            # Create a header row
            for header in table_data[0]:
                pdf.cell(38, 10, header, border=1, align='C')
                
            pdf.ln()

            # Iterate over the table data and write each cell to the PDF
            for row in table_data[1:]:
                for cell in row:
                    pdf.cell(38, 10, str(cell), border=1, align='C')

            pdf.ln(10)



        if self.Other_Graph.CHANNELS[self.Other_Graph.Current_Channel-1].Signal :
            self.Other_Graph.CHANNELS[self.Other_Graph.Current_Channel-1].Signal.Creating_Signal_Statistics()  
            pdf.set_font('times','U', 16)
            pdf.cell(0,30,f"Signal of Graph {self.Other_Graph.graph_number} Channel {self.Other_Graph.Current_Channel} Data: ")
            pdf.set_xy(10,170)
            pdf.image('Snapshots/Image 1.png', w=190,h=60)
            pdf.ln(10)

            pdf.set_font('times','', 12)
            table_data = [['Maximum Value', 'Minimum Value', 'Mean','Standard Deviation','Duration'], 
                        [self.Other_Graph.CHANNELS[self.Current_Channel-1].Signal.Max_Value, self.Other_Graph.CHANNELS[self.Current_Channel-1].Signal.Min_Value, 
                        self.Other_Graph.CHANNELS[self.Current_Channel-1].Signal.Mean,self.Other_Graph.CHANNELS[self.Current_Channel-1].Signal.Standard_Deviation,
                        f"{self.Other_Graph.CHANNELS[self.Current_Channel-1].Signal.Duration} min"]]

        
            for header in table_data[0]:
                pdf.cell(38, 10, header, border=1, align='C')
                
            pdf.ln()

            
            for row in table_data[1:]:
                for cell in row:
                    pdf.cell(38, 10, str(cell), border=1, align='C')

            pdf.ln(10)

        pdf.output('Signals Data Analysis Report.pdf')


    # def Scroll_Signal(self,Scrolling_Coordinates_Value):
   
    #         # Calculate the corresponding index based on the scrollbar's value
    #         index = min(int(Scrolling_Coordinates_Value / self.Scroll_Bar.maximum() * len(self.CHANNELS[self.Current_Channel - 1].Signal.X_Coordinates)), len(self.CHANNELS[self.Current_Channel - 1].Signal.X_Coordinates) - 1)

    #         # Update the plot data
    #         self.CHANNELS[self.Current_Channel - 1].Signal.i = index
    #         self.CHANNELS[self.Current_Channel - 1].Signal.Update_Plot_Data()

    #         # Update the X range of the plot
    #         self.CHANNELS[self.Current_Channel - 1].Signal.Graph_Widget.getViewBox().setXRange(max(self.CHANNELS[self.Current_Channel - 1].Signal.X_Coordinates[0 : index + 1]) - 100, max(self.CHANNELS[self.Current_Channel - 1].Signal.X_Coordinates[0 : index + 1]))    
        
                

        

        

