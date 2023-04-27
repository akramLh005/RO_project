# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 13:59:15 2023

@author: Admin
"""


import gurobipy as gp
from gurobipy import GRB

def tomo_optimization(plants, depots, clients, production_capacity, prod_to_depot_cost, depot_to_client_cost, client_demand, fixed_costs):
    # Create model
    model = gp.Model("Tomo")

    # Add variables
    x = model.addVars(plants, depots, obj=prod_to_depot_cost, name="x")
    y = model.addVars(depots, clients, obj=depot_to_client_cost, name="y")
    z = model.addVars(plants + depots, obj=fixed_costs, vtype=GRB.BINARY, name="z")

    # Add constraints
    model.addConstrs((gp.quicksum(x[p, d] for p in plants) == gp.quicksum(y[d, c] for c in clients) for d in depots), name="DepotBalance")
    model.addConstrs((gp.quicksum(x[p, d] for d in depots) <= production_capacity[plants.index(p)] * z[p] for p in plants), name="ProductionCapacity")
    model.addConstrs((gp.quicksum(y[d, c] for d in depots) >= client_demand[clients.index(c)] for c in clients), name="DemandSatisfaction")

    # Set objective
    model.setObjective(gp.quicksum(z[p] * fixed_costs[plants.index(p)] for p in plants) + gp.quicksum(z[d] * fixed_costs[len(plants) + depots.index(d)] for d in depots) + gp.quicksum(x[p, d] * prod_to_depot_cost[plants.index(p)][depots.index(d)] for p in plants for d in depots) + gp.quicksum(y[d, c] * depot_to_client_cost[depots.index(d)][clients.index(c)] for d in depots for c in clients), GRB.MINIMIZE)

    # Optimize model
    model.optimize()

    # Store the results in a string variable
    if model.status == GRB.Status.OPTIMAL:
        results = "Optimal solution found:\n"
        for p, d in x.keys():
            if x[p, d].x > 1e-6:
                results += f"Produce and transport {x[p, d].x:.2f} tons from {p} to {d}\n"
        for d, c in y.keys():
            if y[d, c].x > 1e-6:
                results += f"Transport {y[d, c].x:.2f} tons from {d} to {c}\n"
        for p in plants:
            if z[p].x > 1e-6:
                results += f"{p} is open\n"
        for d in depots:
            if z[d].x > 1e-6:
                results += f"{d} is open\n"
        results += f"Objective value: {model.objVal:.2f}"
    else:
        results = "No optimal solution found."

    return results




