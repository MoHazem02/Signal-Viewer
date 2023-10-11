class Signal:
    def __init__(self, col, X_List, Y_list, graph):
        self.X_Coordinates = X_List
        self.Y_Coordinates = Y_list
        self.hide = False
        self.running = True
        self.color = col
        self.Old_Color = col
        self.graph_number = graph
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



    
        