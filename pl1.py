# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 13:36:52 2023

@author: Admin
"""
from gurobipy import *

def pl1_gestion_optimale_d_une_zone_agricole(total_area, crop_data, total_labor, total_water, total_machine_time):
    # Initialize model
    model = Model("PL1_Gestion_optimale_d_une_zone_agricole")

    # Decision variables
    area = model.addVars(crop_data.keys(), lb=0, ub=total_area, name="area")
    # Constraints
    model.addConstr(sum(area[c] for c in crop_data.keys()) <= total_area, "total_area_constraint")
    model.addConstr(sum(crop_data[c]["labor"] * area[c] for c in crop_data.keys()) <= total_labor, "total_labor_constraint")
    model.addConstr(sum(crop_data[c]["water"] * area[c] for c in crop_data.keys()) <= total_water, "total_water_constraint")
    model.addConstr(sum(crop_data[c]["machine_time"] * area[c] for c in crop_data.keys()) <= total_machine_time, "total_machine_time_constraint")

    # Objective function
    revenue = sum(crop_data[c]["price"] * crop_data[c]["yield"] * area[c] for c in crop_data.keys()) - sum((crop_data[c]["salary"] * crop_data[c]["labor"] * area[c]) + (crop_data[c]["fixed_cost"] * area[c]) for c in crop_data.keys())
    model.setObjective(revenue, GRB.MAXIMIZE)

    # Solve the model
    model.optimize()

    # Print results
    result = {}
    for c in crop_data.keys():
        result[c] = area[c].x

    return result, model.objVal
# Example usage
total_area = 1000
crop_data = {
    "Blé": {"yield": 75, "price": 60, "labor": 2, "machine_time": 30, "water": 3000, "salary": 500, "fixed_cost": 250},
    "Orge": {"yield": 60, "price": 50, "labor": 1, "machine_time": 24, "water": 2000, "salary": 500, "fixed_cost": 180},
    "Mais": {"yield": 55, "price": 66, "labor": 2, "machine_time": 20, "water": 2500, "salary": 600, "fixed_cost": 190},
    "Bet-sucre": {"yield": 50, "price": 110, "labor": 3, "machine_time": 28, "water": 3800, "salary": 700, "fixed_cost": 310},
    "Tournesol": {"yield": 60, "price": 60, "labor": 2, "machine_time": 25, "water": 3200, "salary": 550, "fixed_cost": 320},
}
total_labor = 3000
total_water = 25000000
total_machine_time = 24000

areas, revenue = pl1_gestion_optimale_d_une_zone_agricole(total_area, crop_data, total_labor, total_water, total_machine_time)

print("Optimal solution:")
for c in crop_data.keys():
    print(f"Area for {c}: {areas[c]} hectares")
print(f"Total revenue: {revenue} UM")


