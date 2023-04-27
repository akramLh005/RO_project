# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 13:45:51 2023

@author: Admin
"""

from gurobipy import *
def pl3_planification(days, min_required, work_days=5, rest_days=2):
    # Initialize model
    model = Model("PL3_Planification_des_besoins_en_ressources_humaines")
    # Decision variables
    employees = model.addVars(days, lb=0, vtype=GRB.INTEGER, name="employees")
    # Constraints
    for i in range(days):
        model.addConstr(quicksum(employees[(i - j) % days] for j in range(work_days)) >= min_required[i], f"staffing_constraint_{i}")
    # Objective function
    total_employees = quicksum(employees[i] for i in range(days))
    model.setObjective(total_employees, GRB.MINIMIZE)
    # Solve the model
    model.optimize()
    # Get results
    results = {}
    
    for i in range(days):
        results[f"employees_starting_day_{i+1}"] = employees[i].x
    results["total_employees"] = model.objVal
    return results
    # Example usage
days = 7
min_required = [17, 13, 15, 19, 14, 16, 11]
print(pl3_planification(days, min_required))