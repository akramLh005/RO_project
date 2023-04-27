# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 20:19:46 2023

@author: Admin
"""

import gurobipy as gp
from gurobipy import *
centrales = ['C1', 'C2', 'C3']
villes = ['V1', 'V2', 'V3', 'V4']

offre = {
    'C1': 35,
    'C2': 50,
    'C3': 40
}

augmented_demande = {
    'V1': 50,
    'V2': 25,
    'V3': 35,
    'V4': 35
}

cout_transport = {
    ('C1', 'V1'): 8,
    ('C1', 'V2'): 6,
    ('C1', 'V3'): 10,
    ('C1', 'V4'): 9,
    ('C2', 'V1'): 9,
    ('C2', 'V2'): 12,
    ('C2', 'V3'): 13,
    ('C2', 'V4'): 7,
    ('C3', 'V1'): 14,
    ('C3', 'V2'): 9,
    ('C3', 'V3'): 16,
    ('C3', 'V4'): 5
}
penalite={
    'V1': 20,
    'V2': 25,
    'V3': 22,
    'V4': 35  
    }
m = gp.Model()
x = m.addVars(centrales, villes,name='x')


z = m.addVars(villes, vtype=GRB.BINARY, name="z")
m.addConstrs((gp.quicksum(x[i,j] for i in centrales) >= augmented_demande[j] * z[j] for j in villes), name="meet_demand")
m.setObjective(
    gp.quicksum(cout_transport[i,j]*x[i,j] for i in centrales for j in villes) +
    gp.quicksum(penalite[j]*augmented_demande[j]*(1 - z[j]) for j in villes),
    sense=gp.GRB.MINIMIZE
)
for i in centrales:
    m.addConstr(gp.quicksum(x[i,j] for j in villes) <= offre[i], name=f"offre_{i}")

m.optimize()


if m.status == gp.GRB.OPTIMAL:
    for i in centrales:
        for j in villes:
            if x[i,j].x > 0:
                print(f"{i} -> {j} : {x[i,j]}")
    print(f"Coût total : {m.objVal}")
else:
    print("Pas de solution trouvée.")