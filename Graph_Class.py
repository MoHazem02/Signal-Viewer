from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QFileDialog
import wfdb, Signal_Class
import numpy as np
from Channel_Class import Channel
import fpdf

class Graph:
    def __init__(self, Graph_Number, ui_mainwindow, other_graph, scroll_bar = None, graph_window = None):
        self.hidden_lines = []  # Add this line to initialize the list
        self.textbox = None
        self.channel_count = 1
        self.signal_count = 0
        self.graph_number = Graph_Number
        self.UI_Window = ui_mainwindow
        self.Graph_Window = graph_window
        self.Current_Channel = 1
        self.CHANNELS = []
        self.First_Channel = Channel(1)
        self.CHANNELS.append(self.First_Channel)
        self.Linked = False # Whether the 2 graphs are linked or not
        self.Other_Graph = other_graph # Reference to the other graph
        self.Hidden = False
        self.Scroll_Bar = scroll_bar
        self.Paused = False
        self.Legend = None
        
    
    def Update_Current_Channel(self): 
        if self.graph_number == 1:
            self.Current_Channel = int(str(self.UI_Window.Channels_Top_ComboBox.currentText())[-1])
        else:
            self.Current_Channel = int(str(self.UI_Window.Channels_Bottom_ComboBox.currentText())[-1])


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


            #Set the channel's signal to None
            self.CHANNELS[self.Current_Channel-1].Signal = None
            self.signal_count -= 1
            
            
    def Move_Signal(self):

        #Checks which graph that its move is pressed
        if self.graph_number == 1:
                #Gets the current selected channel
                self.Update_Current_Channel()
                #Store the data of the signal that will be moved
                Temporary_Signal=self.CHANNELS[self.Current_Channel - 1].Signal  
                #Remove the signal of the current selected channel from its graph   
                self.Remove_Signal()
                Temporary_Signal.Graph_Widget = self.Other_Graph.Graph_Window
                Temporary_Signal.Graph_Object = self.Other_Graph
                #Add the signal that will be moved to the other graph       
                self.Other_Graph.Add_Signal(Temporary_Signal)
 
        else:
            self.Update_Current_Channel()
            Temporary_Signal=self.CHANNELS[self.Current_Channel - 1].Signal
            self.Remove_Signal()
            Temporary_Signal.Graph_Widget = self.Other_Graph.Graph_Window
            Temporary_Signal.Graph_Object = self.Other_Graph 
            self.Other_Graph.Add_Signal(Temporary_Signal)

        #Clear both graphs windows before starting plotting
        self.Graph_Window.clear()
        self.Other_Graph.Graph_Window.clear()    

        #Start plotting both graphs signals
        for channel in self.CHANNELS:
            if channel.Signal:
                channel.Signal.Plot_Signal()

        for channel in self.Other_Graph.CHANNELS:
            if channel.Signal:
                channel.Signal.Plot_Signal() 
        
            
    def Add_Signal(self, signal): # add the signal to a channel 
       if signal:
            if self.channel_count == self.signal_count:
                new_Channel = self.Add_Channel()
                new_Channel.Signal = signal
                #Add the new signal to the list of signals
            else:
                for channel in self.CHANNELS:
                    if channel.Signal is None:
                        channel.Signal = signal  
                        #Add the new signal to the list of signals
                        
                        break
            self.signal_count += 1
            
            #clear old signals for plotting all together
            self.Graph_Window.clear()
            if self.signal_count > 1:
                self.Reset_Signal()
            # Plot all signals
            for channel in self.CHANNELS:
                channel.Signal.Plot_Signal()
              

            if self.graph_number == 1:
                self.UI_Window.Horiz_ScrollBar_Top.setEnabled(True)
                self.UI_Window.Color_Top_Button.setEnabled(True)
                self.UI_Window.Edit1_Label_Button.setEnabled(True)
                self.UI_Window.Play1_Button.setEnabled(True)
                self.UI_Window.Move_Top_Button.setEnabled(True)
                self.UI_Window.Hide_Top_Button.setEnabled(True)
                self.UI_Window.Vert_ScrollBar_Top.setEnabled(True)
                self.UI_Window.Label_Top_LineEdit.setEnabled(True)
                self.UI_Window.Rewind1_Button.setEnabled(True)
            else:
                self.UI_Window.Horiz_ScrollBar_Bottom.setEnabled(True)
                self.UI_Window.Color_Bottom_Button_2.setEnabled(True)
                self.UI_Window.Edit2_Label_Button.setEnabled(True)
                self.UI_Window.Play2_Button.setEnabled(True)
                self.UI_Window.Move_Bottom_Button.setEnabled(True)
                self.UI_Window.Hide_Bottom_Button.setEnabled(True)
                self.UI_Window.Vert_ScrollBar_Bottom.setEnabled(True)
                self.UI_Window.Label_Bottom_LineEdit.setEnabled(True)
                self.UI_Window.Rewind2_Button.setEnabled(True)
             

    def Add_Channel(self):
        self.channel_count += 1
        Temporary_String = f"Channel {self.channel_count}"
        if self.graph_number == 1:
            self.UI_Window.Channels_Top_ComboBox.addItem(Temporary_String)
        else:
            self.UI_Window.Channels_Bottom_ComboBox.addItem(Temporary_String) 
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

            self.Graph_Window.clear()
            for channel in self.CHANNELS:
                channel.Signal.Plot_Signal()
                if self.Paused:
                    channel.Signal.data_line.setData(channel.Signal.X_Coordinates[0 : channel.Signal.X_Points_Plotted + 1], 
                                         channel.Signal.Y_Coordinates[0 : channel.Signal.X_Points_Plotted + 1], color = color, name = channel.Signal.legend_text)

           
    

    def Browse_Signals(self):
        File_Path, _ = QFileDialog.getOpenFileName(None, "Browse Signal", "" , "All Files (*)")
        Record = wfdb.rdrecord(File_Path[:-4])
        Y_Coordinates = list(Record.p_signal[:,0])
        X_Coordinates = list(np.arange(len(Y_Coordinates)))
        Sample_Signal = Signal_Class.Signal(col = "g", X_List = X_Coordinates, Y_list = Y_Coordinates, graphWdg = self.Graph_Window, graphObj = self)
            
        self.Add_Signal(Sample_Signal)
        

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
        self.Hidden = not self.Hidden

        self.Update_Current_Channel()
        self.current_channel = self.CHANNELS[self.Current_Channel - 1]
        # Check if the channel has a signal
        if self.current_channel.Signal is not None:
            # Toggle the visibility of the signal
            if self.current_channel.Signal.hide:
                self.current_channel.Signal.Unhide_Signal()
            else:
                self.current_channel.Signal.Hide_Signal()
     


    def Add_Legend(self):
        if self.Legend is None:
            self.Legend = self.Graph_Window.addLegend()
            self.Other_Graph.Legend = self.Other_Graph.Graph_Window.addLegend()
        text = self.textbox.text()
        if text == "":
            return
        self.Update_Current_Channel()
        
        # Get the current signal
        current_signal = self.CHANNELS[self.Current_Channel - 1].Signal

        if current_signal.legend_text:
            self.Legend.removeItem(current_signal.data_line)
            current_signal.legend_text = text
            self.Legend.addItem(current_signal.data_line, text)
        else:    
            current_signal.legend_text = text
            self.Legend.addItem(current_signal.data_line, text)
                        
    
    def Link_Unlink(self):
        # We basically toggle what is already there
        self.Linked = not self.Linked
        self.Other_Graph.Linked = not self.Other_Graph.Linked

        plot_item_1 = self.Graph_Window.getPlotItem()
        plot_item_2 = self.Other_Graph.Graph_Window.getPlotItem()

        _translate = QtCore.QCoreApplication.translate
        if self.Linked: # to link and unlink from 1 and 2
            self.UI_Window.Link_Unlink_Button.setText(_translate("MainWindow", "    Unlink Graphs     "))
            self.Reset_Signal()
            self.Other_Graph.Reset_Signal()
            plot_item_2.setXLink(plot_item_1)
            plot_item_2.setYLink(plot_item_1)
        else:
            plot_item_2.setXLink(None)
            plot_item_1.setYLink(None)
            self.UI_Window.Link_Unlink_Button.setText(_translate("MainWindow", "    Link Graphs     "))
  

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
                self.UI_Window.CineSpeed_Bottom_Slider.setValue(value)
            else:
                self.UI_Window.CineSpeed_Top_Slider.setValue(value)
            
                
    def Reset_Signal(self):

        #If the graphs are linked, reset all signals in both graphs
        if self.Linked:
            self.Graph_Window.clear()
            for channel in self.CHANNELS:
                if channel.Signal:
                    channel.Signal.X_Points_Plotted = 0
                    channel.Signal.Plot_Signal()  # Replot the signal from the beginning

            self.Other_Graph.Graph_Window.clear()
            for channel in self.Other_Graph.CHANNELS:
                if channel.Signal:
                    channel.Signal.X_Points_Plotted = 0
                    channel.Signal.Plot_Signal()  # Replot the signal from the beginning

            return
        
        
        self.Graph_Window.clear()
        for channel in self.CHANNELS:
            if channel.Signal:
                channel.Signal.X_Points_Plotted = 0



        

    def Toggle_Play_Pause(self):
        _translate = QtCore.QCoreApplication.translate
        self.Paused = not self.Paused
        if self.graph_number == 1:
            if self.Paused == False:
                self.UI_Window.Play1_Button.setText(_translate("MainWindow", "   Pause         "))
            else:
                self.UI_Window.Play1_Button.setText(_translate("MainWindow", "   Play         "))
        else:
            if self.Paused == False:
                self.UI_Window.Play2_Button.setText(_translate("MainWindow", "   Pause         "))
            else:
                self.UI_Window.Play2_Button.setText(_translate("MainWindow", "   Play         "))

        for channel in self.CHANNELS:
            channel.Signal.pause = not channel.Signal.pause
            self.Graph_Window.getViewBox().setXRange(max(channel.Signal.X_Coordinates[0 : channel.Signal.X_Points_Plotted + 1]) - 100, max(channel.Signal.X_Coordinates[0 : channel.Signal.X_Points_Plotted + 1]))
        
        if self.Linked:
            for channel in self.Other_Graph.CHANNELS:
                channel.Signal.pause = not channel.Signal.pause
            if self.graph_number == 1:
                if self.Paused == False:
                    self.UI_Window.Play1_Button.setText(_translate("MainWindow", "   Pause         "))
                    self.UI_Window.Play2_Button.setText(_translate("MainWindow", "   Pause         "))
                else:
                    self.UI_Window.Play1_Button.setText(_translate("MainWindow", "   Play         "))
                    self.UI_Window.Play2_Button.setText(_translate("MainWindow", "   Play         "))
            else:
                if self.Paused == False:
                    self.UI_Window.Play1_Button.setText(_translate("MainWindow", "   Pause         "))
                    self.UI_Window.Play2_Button.setText(_translate("MainWindow", "   Pause         "))
                else:
                    self.UI_Window.Play1_Button.setText(_translate("MainWindow", "   Play         "))
                    self.UI_Window.Play2_Button.setText(_translate("MainWindow", "   Play         "))
            

    def Scroll_Signal(self, Scrolling_Coordinates_Value):
        # Calculate the corresponding index based on the scrollbar's value
        index = min(int(Scrolling_Coordinates_Value / self.UI_Window.Horiz_ScrollBar_Top.maximum() * len(self.CHANNELS[self.Current_Channel - 1].Signal.X_Coordinates)), len(self.CHANNELS[self.Current_Channel - 1].Signal.X_Coordinates) - 1)

        # Update the plot data
        self.CHANNELS[self.Current_Channel - 1].Signal.X_Points_Plotted = index
        self.CHANNELS[self.Current_Channel - 1].Signal.Update_Plot_Data()

        # Update the X range of the plot
        self.CHANNELS[self.Current_Channel - 1].Signal.Graph_Widget.getViewBox().setXRange(max(self.CHANNELS[self.Current_Channel - 1].Signal.X_Coordinates[0 : index + 1]) - 100, max(self.CHANNELS[self.Current_Channel - 1].Signal.X_Coordinates[0 : index + 1]))


    def VertScroll_Signal(self, Scrolling_Coordinates_Value):

        # Calculate the corresponding index based on the scrollbar's value
        #index = min(int(Scrolling_Coordinates_Value / self.UI_Window.Vert_ScrollBar_Top.maximum() * len(self.CHANNELS[self.Current_Channel - 1].Signal.Y_Coordinates)), len(self.CHANNELS[self.Current_Channel - 1].Signal.Y_Coordinates) - 1)

        # Update the plot data
        #self.CHANNELS[self.Current_Channel - 1].Signal.i = index
        #self.CHANNELS[self.Current_Channel - 1].Signal.Update_Plot_Data()
        # Update the Y range of the plot
        min_value = -0.4
        max_value = 0.4
        if self.graph_number == 1:
            self.UI_Window.GraphWidget_Top.getViewBox().setYRange(min_value, max_value)
        else:
            self.UI_Window.GraphWidget_Bottom.getViewBox().setYRange(min_value, max_value)


    def Rewind_Signal(self):
        if self.Linked:
            for channel in self.CHANNELS:
                if channel.Signal:
                    channel.Signal.X_Points_Plotted = 0
                    channel.Signal.Update_Plot_Data()

            for channel in self.Other_Graph.CHANNELS:
                if channel.Signal:
                    channel.Signal.X_Points_Plotted = 0
                    channel.Signal.Update_Plot_Data()


        # Rewind the signal
        elif self.CHANNELS[self.Current_Channel - 1].Signal:
            self.CHANNELS[self.Current_Channel - 1].Signal.X_Points_Plotted = 0
            self.CHANNELS[self.Current_Channel - 1].Signal.Update_Plot_Data()



    def Export_PDF(self):
        #Creating the pdf object 
        pdf = fpdf.FPDF()
        #Adding the first page to the pdf
        pdf.add_page()
        #Adding page break with margin = 15 to open another page when limit is reached
        pdf.set_auto_page_break(auto=1,margin=20)
        #Setting the title of the page style
        pdf.set_font('times','B', 22)
        pdf.cell(0, 10, "Signals Data Analysis Report", align="C", ln=1)
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
            pdf.image('Snapshots/image0.png', w=190, h=60)
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
            pdf.image('Snapshots/image1.png', w=190,h=60)
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
        

        
