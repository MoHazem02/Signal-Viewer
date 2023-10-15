from PyQt5 import QtCore
import statistics
class Signal:
    def __init__(self, col, X_List, Y_list, graphWdg, graphObj):
        self.pause = False #to control movement of the signal
        self.hidden_lines = []  # Add this line to initialize the list
        self.legend = None
        self.legend_text = None
        self.legend_color = None
        self.X_Coordinates = X_List
        self.Y_Coordinates = Y_list
        self.hide = False
        self.running = True
        self.color = col
        self.Old_Color = col
        self.Graph_Widget = graphWdg
        self.Graph_Object = graphObj
        self.X = []
        self.Y = []
        self.i = 0
        self.speed = 1
        self.Max_Value = 0
        self.Min_Value = 9999999999999999
        self.Duration = 0
        self.Mean = 0
        self.Standard_Deviation = 0
        #Each signal corresponds to a channel, initially channel 1

    def Hide_Signal(self):
        self.data_line.setVisible(False)
        self.hide = True

    def Unhide_Signal(self):
        self.data_line.setVisible(True)
        self.hide = False
        
    def Change_Graph_Number(self):
        if self.Graph_Object.graph_number == 1:
            self.Graph_Object.graph_number = 2
        else:
            self.Graph_Object.graph_number = 1

    def Plot_Signal(self):
        
        self.data_line = self.Graph_Widget.plot(self.X_Coordinates[:1], self.Y_Coordinates[:1], self.legend , pen = self.color )
        self.timer = QtCore.QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.Update_Plot_Data)
        self.timer.start()


    def Update_Plot_Data(self):
        
        if not self.pause and self.data_line:
            self.i += self.speed
            self.data_line.setData(self.X_Coordinates[0 : self.i + 1], self.Y_Coordinates[0 : self.i + 1])  # Update the data.
            if not self.hide:
                self.Graph_Widget.getViewBox().setXRange(max(self.X_Coordinates[0 : self.i + 1]) - 100, max(self.X_Coordinates[0 : self.i + 1]))
            
            # Check if the signal has ended
            if self.i >= len(self.X_Coordinates):
                # Enable the Rewind button
                self.Graph_Object.UI_Window.Rewind_1.setEnabled(True)
            
        if self.Graph_Object.graph_number == 1:
            # Update the scrollbar's maximum value and position
            self.Graph_Object.UI_Window.ScrollBar_Top.valueChanged.disconnect(self.Graph_Object.UI_Window.Scroll_Top_Signal)
            self.Graph_Object.UI_Window.ScrollBar_Top.setMaximum(len(self.X_Coordinates))
            self.Graph_Object.UI_Window.ScrollBar_Top.setValue(self.i)
            self.Graph_Object.UI_Window.ScrollBar_Top.valueChanged.connect(self.Graph_Object.UI_Window.Scroll_Top_Signal)
        
        else:

            self.Graph_Object.UI_Window.ScrollBar_Bottom.valueChanged.disconnect(self.Graph_Object.UI_Window.Scroll_Bottom_Signal)
            self.Graph_Object.UI_Window.ScrollBar_Bottom.setMaximum(len(self.X_Coordinates))
            self.Graph_Object.UI_Window.ScrollBar_Bottom.setValue(self.i)
            self.Graph_Object.UI_Window.ScrollBar_Bottom.valueChanged.connect(self.Graph_Object.UI_Window.Scroll_Bottom_Signal)
    
    
    def toggle_play_pause(self):
        self.pause = not self.pause
    
    
    def Update_Cine_Speed(self, speed_value):
        self.speed = speed_value
        
    
    def Creating_Signal_Statistics(self):
        if self.Y_Coordinates:
            for i in range(len(self.Y_Coordinates)):
                if self.Y_Coordinates[i]>self.Max_Value:
                    self.Max_Value=self.Y_Coordinates[i]
                if self.Y_Coordinates[i]<=self.Min_Value:
                    self.Min_Value=self.Y_Coordinates[i]
                                
            self.Standard_Deviation = statistics.stdev(self.Y_Coordinates)
            self.Mean = statistics.mean(self.Y_Coordinates)
            self.Standard_Deviation = f"{self.Standard_Deviation:.6f}"  
            self.Mean = f"{self.Mean:.6f}"   
            self.Duration = f"{self.X_Coordinates[-1]/60:.2f}"      