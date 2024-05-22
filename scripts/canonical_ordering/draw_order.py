from canonical_order_kant import KantCanonicalOrder
import networkx as nx

class DrawCanonicalOrder:
    def __init__(self, co:KantCanonicalOrder) -> None:
        self.co = co


    def get_node_labels(self, node_list):
            labels = {}
            for node_index in node_list:
                labels[node_index] = [self.co.get_node_data(node_index).order]
            return labels

    def get_init_nodes(self):
        init_nodes = []
        for node_index in self.co.G.nodes:
            if self.co.get_node_data(node_index).order != -99 or self.co.get_node_data(node_index).visited != 1:
                init_nodes.append(node_index)

        labels = self.get_node_labels(init_nodes)
        return init_nodes, labels

    def get_relev_nodes(self):
        
        relev_nodes = []
        for node_index in self.co.G.nodes:
            if self.co.get_node_data(node_index).order != -99:
                relev_nodes.append(node_index)

        labels = self.get_node_labels(relev_nodes)
        return relev_nodes, labels
    
    def start(self):
        self.co.initialize_order()
        init_nodes, labels = self.get_init_nodes()
        nx.draw_networkx(self.co.G, self.co.embed, nodelist=init_nodes, node_color="#5d7f14", labels=labels)

    def next_step(self):
        self.co.order_next_node()

        nodes, labels = self.get_relev_nodes()
        nx.draw_networkx(self.co.G, self.co.embed, nodelist=nodes, node_color="#5d7f14", labels=labels)