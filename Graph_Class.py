class Graph:
    def __init__(self, Graph_Number, ui_mainwindow, graph_window = None):
        self.channel_count = 1
        self.signal_count = 0
        self.graph_number = Graph_Number
        self.UI_Window = ui_mainwindow
        self.Graph_Window = graph_window
        self.Current_Channel = 1
        self.Signals = []

    def Increase_Channels(self):
            self.channel_count = (self.channel_count+1)

    def Decrease_Channels(self):
            self.channel_count = (self.channel_count-1)

    def Add_Channel(self):
        self.channel_count += 1
        Temporary_String = f"Channel {self.channel_count}"
        if self.graph_number == 1:
            self.UI_Window.Channels_of_Graph_1.addItem(Temporary_String)
        else:
            self.UI_Window.Channels_of_Graph_2.addItem(Temporary_String) 

    def Plot_Signal(self, signal):
        self.Graph_Window.plot(x = signal.X_Coordinates, y = signal.Y_Coordinates, pen = signal.color)

    def Update_Current_Channel(self):
        if self.graph_number == 1:
            self.Current_Channel = int(str(self.UI_Window.Channels_of_Graph_1.currentText())[-1])
        else:
            self.Current_Channel = int(str(self.UI_Window.Channels_of_Graph_2.currentText())[-1])

    def Remove_Signal(self):
        signal = self.Signals[self.Current_Channel - 1]
        self.Graph_Window.removeItem(signal)
        self.Signals.remove(signal)
        self.Graph_Window.update()
        self.signal_count -= 1


    def Add_Signal(self, signal):
        self.Signals.append(signal)
        if self.channel_count == self.signal_count:
            self.Add_Channel()
        self.Plot_Signal(signal)
        self.signal_count += 1


    

