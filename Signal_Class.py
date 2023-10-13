from PyQt5 import QtCore

class Signal:
    def __init__(self, col, X_List, Y_list, graphWdg, graphObj):
        self.pause = False #to control movement of the signal
        self.hidden_lines = []  # Add this line to initialize the list
        self.legend = None
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
            # Update the scrollbar's maximum value and position
            self.Graph_Object.UI_Window.horizontalScrollBar.valueChanged.disconnect(self.Graph_Object.UI_Window.scroll_signal)
            self.Graph_Object.UI_Window.horizontalScrollBar.setMaximum(len(self.X_Coordinates))
            self.Graph_Object.UI_Window.horizontalScrollBar.setValue(self.i)
            self.Graph_Object.UI_Window.horizontalScrollBar.valueChanged.connect(self.Graph_Object.UI_Window.scroll_signal)

    
    
    def toggle_play_pause(self):
        self.pause = not self.pause
    
    
    def Update_Cine_Speed(self, speed_value):
        self.speed = speed_value
        if speed_value == 0:
            self.speed = 1
            