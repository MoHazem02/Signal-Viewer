from PyQt5 import QtWidgets,QtCore

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
        #Each signal corresponds to a channel, initially channel 1

    def hide_signal(self):
        self.data_line.setVisible(False)
        self.hide = True

    def unhide_signal(self):
        self.data_line.setVisible(True)
        self.hide = False
        
    def change_graph_number(self):
        if self.graph_number == 1:
            self.graph_number = 2
        else:
            self.graph_number = 1

    def Plot_Signal(self):
        
        self.data_line = self.graph.plot(self.X_Coordinates[:1], self.Y_Coordinates[:1], self.legend , pen = self.color )
        self.timer = QtCore.QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()


    def update_plot_data(self):

        self.i += 1
        self.data_line.setData(self.X_Coordinates[0 : self.i + 1], self.Y_Coordinates[0 : self.i + 1])  # Update the data.

