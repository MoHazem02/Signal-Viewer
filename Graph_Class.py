class Graph:
    def __init__(self, Graph_Number):
        self.channel_count = 1
        self.graph_number = Graph_Number

    def Increase_Channels(self):
            self.channel_count = (self.channel_count+1)

    def Decrease_Channels(self):
            self.channel_count = (self.channel_count-1)

    

