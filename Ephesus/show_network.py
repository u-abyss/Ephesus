import matplotlib.pyplot as plt
import networkx as nx
from artist import similar_artists_arr

def show_graph(nodes):
    G = nx.Graph()
    for node in nodes:
        nx.add_star(G, node)
    nx.draw_networkx(G, node_size=200, font_size=0, width=0.2, style='dotted')
    plt.show()


nodes = [
    ["testdfasda", 3, 4, 5],
    [2, 3, 3, 10],
    [3, 9, 23, 6],
    [4, 1, 4, 10],
]

show_graph(similar_artists_arr)
# show_graph(nodes)