class NodeCanonicalOrder:
    def __init__(self, index:int,) -> None:
        self.index = index # node index in the graph .. 
        self.order = -99

        self.mark = False
        self.visited = 1
        self.chords = 0


    def __repr__(self):
        return f"NodeCanonicalOrder({self.__dict__})"
    
    def add_node_to_order(self, order):
        self.update_mark()
        self.update_order(order)
    
    
    def update_mark(self):
        self.mark = True

    def update_order(self, order):
        self.order = order
    
    def update_visited(self):
        self.visited +=1


    def update_chords(self, num_chords):
        self.chords = num_chords
        # need to have the exterior face of subgraph induced by V- {u < V | Mark(u) == true}
        # need to see the chords within this graph 
        # need to see the number indicdent to this node 
