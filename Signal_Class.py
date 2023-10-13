from PyQt5 import QtCore

class Signal:
    def __init__(self, col, X_List, Y_list, graphNum, graph):
        self.legend = None
        self.legend = None
        self.X_Coordinates = X_List
        self.Y_Coordinates = Y_list
        self.hide = False
        self.running = True
        self.color = col
        self.Old_Color = col
        self.graph_number = graphNum
        self.graph = graph
        self.X = []
        self.Y = []
        self.i = 0
        self.speed = 1
        #Each signal corresponds to a channel, initially channel 1

    def Hide_Signal(self):
        self.graph.removeItem(self.data_line)
        self.hide = True
        #self.data_line.setVisible(False)
        #self.hide = True

    def Unhide_Signal(self):
        if self.data_line in self.hidden_lines:
            self.graph.addItem(self.data_line)  # Add the data_line back to the graph
            self.hidden_lines.remove(self.data_line)  # Remove the data_line from the list
            self.hide = False
        #self.data_line.setVisible(True)
        #self.hide = False
        
    def Change_Graph_Number(self):
        if self.graph_number == 1:
            self.graph_number = 2
        else:
            self.graph_number = 1

    def Plot_Signal(self):
        
        self.data_line = self.graph.plot(self.X_Coordinates[:1], self.Y_Coordinates[:1], self.legend , pen = self.color )
        self.timer = QtCore.QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.Update_Plot_Data)
        self.timer.start()


    def Update_Plot_Data(self):

        self.i += self.speed
        self.data_line.setData(self.X_Coordinates[0 : self.i + 1], self.Y_Coordinates[0 : self.i + 1])  # Update the data.
        self.graph.getViewBox().setXRange(max(self.X_Coordinates[0 : self.i + 1])-100, max(self.X_Coordinates[0 : self.i + 1]))

    def Update_Cine_Speed(self, speed_value):
        self.speed = speed_value