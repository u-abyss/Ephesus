import matplotlib.pyplot as plt
import networkx as nx

def show_graph(nodes):
    G = nx.Graph()
    for node in nodes:
        nx.add_star(G, node)
    nx.draw_networkx(G, node_size=200, font_size=0, width=0.2, style='dotted')
    plt.show()