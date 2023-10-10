class Graph:
    def __init__(self, Graph_Number, ui_mainwindow):
        self.channel_count = 1
        self.graph_number = Graph_Number
        self.UI_Window = ui_mainwindow

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


    

