# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 01:57:25 2023

@author: makni
"""

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import pandas as pd
import numpy as np
import tkinter as tk
from PIL import ImageTk, Image


def create_logistic_graph(transport_costs_matrix):
    G = nx.DiGraph()

    for origin, row in transport_costs_matrix.iterrows():
        for dest, cost in row.iteritems():
            if not pd.isna(cost):
                G.add_edge(origin, dest, weight=cost)

    return G


def plot_logistic_graph(G):
    fig = plt.Figure()
    canvas = FigureCanvas(fig)
    ax = fig.add_subplot(111)

    pos = nx.circular_layout(G)
    edge_labels = {(i, j): f'{G.edges[i, j]["weight"]}' for i, j in G.edges}

    nx.draw(G, pos, with_labels=True, node_size=3000, node_color='lightblue', font_size=12, ax=ax)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=12, ax=ax)

    canvas.draw()

    return fig

def display_logistic_graph(transport_costs_matrix):
    # Create the GUI window
    root = tk.Tk()
    root.title("Logistic Graph")

    G = create_logistic_graph(transport_costs_matrix)
    fig = plot_logistic_graph(G)
    fig.savefig("logistic_graphh.png")

    # Load the image in a Tkinter object and display it in a Label widget
    image = Image.open("logistic_graphh.png")
    image = image.resize((300, 300), Image.ANTIALIAS)
    image = ImageTk.PhotoImage(image)
    label = tk.Label(root, image=image)
    label.pack()


    root.mainloop()


transport_costs_matrix = pd.DataFrame(
            [
                [np.nan, 5, 3, 5, 5, 20, 20],
                [9, np.nan, 9, 1, 1, 8, 15],
                [0.4, 8, np.nan, 1, 0.5, 10, 12],
                [np.nan, np.nan, np.nan, np.nan, 1.2, 2, 12],
                [np.nan, np.nan, np.nan, 8, np.nan, 2, 12],
                [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 1],
                [np.nan, np.nan, np.nan, np.nan, np.nan, 7, np.nan],
            ],
            columns=["A", "B", "C", "D1", "D2", "E", "F"],
            index=["A", "B", "C", "D1", "D2", "E", "F"],
        )
display_logistic_graph(transport_costs_matrix)
