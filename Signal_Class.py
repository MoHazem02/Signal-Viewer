from PyQt5 import QtWidgets,QtCore
class Signal:
    def __init__(self, col, X_List, Y_list, graphNum, graph):
        self.X_Coordinates = X_List
        self.Y_Coordinates = Y_list
        self.hide = False
        self.running = True
        self.color = col
        self.Old_Color = col
        self.graph_number = graphNum
        self.graph = graph
        #Each signal corresponds to a channel, initially channel 1

    def hide_signal(self):
        self.color = "black"
        self.hide = True

    def unhide_signal(self):
        self.color = self.Old_Color
        self.hide = True

    def change_graph_number(self):
        if self.graph_number == 1:
            self.graph_number = 2
        else:
            self.graph_number = 1

    def Plot_Signal(self):
        
        self.data_line = self.graph.plot(self.X_Coordinates, self.Y_Coordinates, pen = 'g')
        self.timer = QtCore.QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()


    def update_plot_data(self):

        self.X_Coordinates = self.X_Coordinates[1:]  # Remove the first y element.
        self.X_Coordinates.append(self.X_Coordinates[-1] + 1)  # Add a new value 1 higher than the last.

        self.Y_Coordinates = self.Y_Coordinates[1:]  # Remove the first
        self.Y_Coordinates.append(self.Y_Coordinates[-1]) 

        self.data_line.setData(self.X_Coordinates, self.Y_Coordinates)  # Update the data.





    
        