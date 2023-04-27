# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 13:52:34 2023

@author: Admin
"""

import gurobipy as gp
from gurobipy import GRB
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import pandas as pd
import numpy as np


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



def optimize_distribution(capacities, client_demands, transport_costs_matrix):
    # Create the model
    m = gp.Model("distribution")

    # Add decision variables
    nodes = transport_costs_matrix.index
    x = {}
    for i in nodes:
        for j in nodes:
            if not np.isnan(transport_costs_matrix.at[i, j]):
                x[i, j] = m.addVar(vtype=GRB.CONTINUOUS, name=f"x_{i}_{j}")

    # Set the objective function
    m.setObjective(sum(x[i, j] * transport_costs_matrix.at[i, j] for i, j in x.keys()), GRB.MINIMIZE)

    # Add constraints
    # Capacity constraints
    for i, capacity in zip(['A', 'B', 'C'], capacities):
        m.addConstr(sum(x[i, j] for j in nodes if (i, j) in x) <= capacity, f"capacity_{i}")

    # Demand constraints
    for j, demand in zip(['E', 'F'], client_demands):
        m.addConstr(sum(x[i, j] for i in nodes if (i, j) in x) >= demand, f"demand_{j}")

    # Flow constraints
    for depot in ['D1', 'D2']:
        m.addConstr(sum(x[i, depot] for i in nodes if (i, depot) in x) ==
                   sum(x[depot, j] for j in nodes if (depot, j) in x), f"flow_{depot}")

    # Max transport constraints
    for i, j in x.keys():
        m.addConstr(x[i, j] <= 200, f"max_transport_{i}_{j}")

    # Optimize the model
    m.optimize()

    # Collect the optimal solution
    if m.status == GRB.Status.OPTIMAL:
        solution = []
        for i, j in x.keys():
            if x[i, j].x > 0:
                solution.append((i, j, x[i, j].x))
        return solution, m.objVal
    else:
        return None, None

# Test the function with the provided data
capacities = [200, 300, 100]
client_demands = [400, 180]

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

solution, obj_val = optimize_distribution(capacities, client_demands, transport_costs_matrix)

if solution is not None:
    print("Optimal solution found:")
    for i, j, x_val in solution:
        print(f"Transport {x_val} tonnes from {i} to {j}")
    print("Objective value:", obj_val)
else:
    print("No optimal solution found.")


# Test the function with the provided data
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

G = create_logistic_graph(transport_costs_matrix)
fig = plot_logistic_graph(G)
fig.savefig("logistic_graph.png")