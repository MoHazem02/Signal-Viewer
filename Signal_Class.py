from PyQt5 import QtCore
import statistics


class Signal:
    def __init__(self, col, X_List, Y_list, graphWdg, graphObj):
        self.pause = False #to control movement of the signal
        self.hidden_lines = []  # Add this line to initialize the list
        self.legend_text = None
        self.legend_color = None
        self.X_Coordinates = X_List
        self.Y_Coordinates = Y_list
        self.hidden = False
        self.running = True
        self.color = col
        self.Graph_Widget = graphWdg
        self.Graph_Object = graphObj
        self.X = []
        self.Y = []
        self.X_Points_Plotted = 0
        self.speed = 1
        self.Max_Value = 0
        self.Min_Value = float('inf')
        self.Duration = 0
        self.Mean = 0
        self.Standard_Deviation = 0

    def Hide_Signal(self):
        self.data_line.setVisible(False)
        self.hidden = True

    def Unhide_Signal(self):
        self.data_line.setVisible(True)
        self.hidden = False

    def Plot_Signal(self):
        self.data_line = self.Graph_Widget.plot(self.X_Coordinates[:1], self.Y_Coordinates[:1], name=self.legend_text,pen=self.color)
        self.timer = QtCore.QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.Update_Plot_Data)
        self.timer.start()

    def Update_Plot_Data(self):

        if not self.pause and self.data_line:
            self.X_Points_Plotted += self.speed
            self.Graph_Object.Reset_Yaxis()
            self.Graph_Widget.setLimits(xMin=0, xMax=float('inf'))
            self.data_line.setData(self.X_Coordinates[0 : self.X_Points_Plotted + 1], self.Y_Coordinates[0 : self.X_Points_Plotted + 1])  # Update the data.
            if not self.hidden:
                self.Graph_Widget.getViewBox().setXRange(max(self.X_Coordinates[0: self.X_Points_Plotted + 1]) - 100, max(self.X_Coordinates[0: self.X_Points_Plotted + 1]))


            # Check if the signal has ended
            if self.X_Points_Plotted >= len(self.X_Coordinates):

                if self.Graph_Object.graph_number == 1:
                    # Enable the Rewind button
                    self.Graph_Object.UI_Window.Rewind1_Button.setEnabled(True)

                else:
                    # Enable the Rewind button
                    self.Graph_Object.UI_Window.Rewind2_Button.setEnabled(True)

        elif self.pause:
            self.Graph_Widget.setLimits(xMin=0, xMax=self.X_Points_Plotted)
       
        if self.Graph_Object.graph_number == 1 and not self.pause:
            self.Graph_Object.UI_Window.Horiz_ScrollBar_Top.setMaximum(self.X_Points_Plotted)
            self.Graph_Object.UI_Window.Horiz_ScrollBar_Top.setMinimum(0)
        
        if self.Graph_Object.graph_number == 2 and not self.pause:
            self.Graph_Object.UI_Window.Horiz_ScrollBar_Bottom.setMaximum(self.X_Points_Plotted)
            self.Graph_Object.UI_Window.Horiz_ScrollBar_Bottom.setMinimum(0)
        self.Graph_Object.Update_Current_Channel()
        _translate = QtCore.QCoreApplication.translate
        if self.Graph_Object.graph_number == 1:
            if self.hidden:
                self.Graph_Object.UI_Window.Hide_Top_Button.setText(_translate("MainWindow", "   Unhide         "))
            else:
                self.Graph_Object.UI_Window.Hide_Top_Button.setText(_translate("MainWindow", "   Hide         "))
        else:
            if self.hidden:
                self.Graph_Object.UI_Window.Hide_Bottom_Button.setText(_translate("MainWindow", "   Unhide         "))
            else:
                self.Graph_Object.UI_Window.Hide_Bottom_Button.setText(_translate("MainWindow", "   Hide         "))

    
    def Toggle_Play_Pause(self):
        self.pause = not self.pause

    def Update_Cine_Speed(self, speed_value):
        self.speed = speed_value

    def Creating_Signal_Statistics(self):
        if self.Y_Coordinates:
            self.Max_Value = max(self.Y_Coordinates)
            self.Min_Value = min(self.Y_Coordinates)
            self.Standard_Deviation = statistics.stdev(self.Y_Coordinates)
            self.Mean = statistics.mean(self.Y_Coordinates)
            self.Standard_Deviation = f"{self.Standard_Deviation:.3f}"
            self.Mean = f"{self.Mean:.3f}"
            self.Duration = f"{self.X_Coordinates[-1] / 1000:.2f}"