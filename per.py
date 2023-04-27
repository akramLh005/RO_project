import tkinter
from tkinter import ttk
import customtkinter
import os
import numpy as np
import pandas as pd

from PIL import ImageTk, Image
from pl1 import pl1_gestion_optimale_d_une_zone_agricole
from pl2 import optimize_petroleum_mix
from pl3 import pl3_planification 
from pl4 import pl4_gestion_de_la_production
from pl5_1 import optimal_electricity_supply 
#from pl5_2 import optimal_electricity_supply_with_penalties 
#from pl6 import optimize_distribution
#, test_data 
from pl7 import optimize_assignment
from pl8 import dijkstra
from pl9 import tomo_optimization
#from pl6_graph import display_logistic_graph

customtkinter.set_appearance_mode("light")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green

def matrix_dimensions(matrix):
    if not matrix or not isinstance(matrix, list):
        raise ValueError("Invalid input: Expected a non-empty 2D matrix (list of lists).")
    rows = len(matrix)
    columns = len(matrix[0])
    return rows, columns


class CustomTable(tkinter.Frame):
    def __init__(self, parent, rows, columns, default_values=None, row_headers=None, column_headers=None):
        tkinter.Frame.__init__(self, parent)
        self.entries = []

        if column_headers:
            for j, header in enumerate(column_headers):
                label = customtkinter.CTkLabel(self, text=header)
                label.grid(row=0, column=j+1)

        if row_headers:
            for i, header in enumerate(row_headers):
                label = customtkinter.CTkLabel(self, text=header)
                label.grid(row=i+1, column=0)

        for i in range(rows):
            current_row = []
            for j in range(columns):
                entry = customtkinter.CTkEntry(self,width=50)
                if default_values and default_values[i][j]:
                    entry.insert(0, default_values[i][j])
                entry.grid(row=i+1, column=j+1)  # Update the row and column indices to account for headers
                current_row.append(entry)
            self.entries.append(current_row)

    def get_table_values(self):
        values = []
        for row_entries in self.entries:
            row_values = [entry.get() for entry in row_entries]
            values.append(row_values)
        return values

import tkinter
from PIL import Image, ImageTk

class home(tkinter.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Change the background color of the frame
        self.configure(bg="white")

        # Load and resize the image
        image = Image.open("image.png")
        image = image.resize((500, 500), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)

        # Create an image label
        self.image_label = tkinter.Label(self, image=photo, bg="white")
        self.image_label.image = photo
        self.image_label.grid(row=0, column=1, rowspan=2, padx=(20, 0), pady=(20, 0), sticky="nsew")

        # Create title label with updated font, size, and style
        title = tkinter.Label(self, text="PLs' Solver", font=("Helvetica", 24, "bold"), pady=20, bg="white")
        title.grid(row=0, columnspan=3, pady=(20, 0))

        # Create textbox with updated font, size, and style
        self.textbox = customtkinter.CTkTextbox(self, width=600, height=500)
        self.textbox.grid(row=1, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.textbox.insert("0.0", "\n\n" + "L'interface que nous avons développée pour notre projet de recherche opérationnelle permettra de présenter de manière claire et concise les neuf problèmes linéaires (PL) que nous avons travaillés sur les deux séries de PL fournies. En somme, cette interface permettra de présenter efficacement notre travail sur les PL et de faciliter la saisie des variables nécessaires pour la résolution des problèmes.\n\nTeam:\n\nMariem Makni \n\nWissal Fnaich \n\nAkram Lahmer \n\nKoussay Ghouari" * 1)
        self.textbox.configure(font=("Helvetica", 14, "bold"))

        """# Create a textbox for names with updated font, size, and style
        self.names_textbox = customtkinter.CTkTextbox(self, width=200)
        self.names_textbox.grid(row=1, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        names = "Mariem Makni \n\nWissal Fnaich \n\nAkram Lahmer \n\nKoussay Ghouari"
        self.names_textbox.insert("0.0", names)
        self.names_textbox.configure(font=("Helvetica", 14, "bold"))"""

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")


class MyFrame1(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        crop_data = {
            "Blé": {"yield": 75, "price": 60, "labor": 2, "machine_time": 30, "water": 3000, "salary": 500, "fixed_cost": 250},
            "Orge": {"yield": 60, "price": 50, "labor": 1, "machine_time": 24, "water": 2000, "salary": 500, "fixed_cost": 180},
            "Mais": {"yield": 55, "price": 66, "labor": 2, "machine_time": 20, "water": 2500, "salary": 600, "fixed_cost": 190},
            "Bet-sucre": {"yield": 50, "price": 110, "labor": 3, "machine_time": 28, "water": 3800, "salary": 700, "fixed_cost": 310},
            "Tournesol": {"yield": 60, "price": 60, "labor": 2, "machine_time": 25, "water": 3200, "salary": 550, "fixed_cost": 320},
        }
        
        # table inputs
        column_headers = ["Parameter", "Value"]
        row_headers = [
            "total_area",
            "total_labor",
            "total_water",
            "total_machine_time",
        ]
        default_values = [["1000"], ["3000"], ["25000000"], ["24000"]]

        rows, columns = matrix_dimensions(default_values)
        self.table = CustomTable(
            self,
            rows,
            columns,
            default_values,
            row_headers=row_headers,
            column_headers=column_headers,
        )
        self.table.grid(row=0, column=2, padx=20, pady=10)

        # get values from the table
        def get_values(self):
            global total_area, total_labor, total_water, total_machine_time
            table_values = self.table.get_table_values()
            total_area = float(table_values[0][0])
            total_labor = float(table_values[1][0])
            total_water = float(table_values[2][0])
            total_machine_time = float(table_values[3][0])

        self.getvals = customtkinter.CTkButton(
            self, text="update table values", command=lambda: get_values(self)
        )
        self.getvals.grid(row=2, column=2, padx=20, pady=10)

        # button to call the solver function and display the results
        def diplay_results():
            areas, revenue = pl1_gestion_optimale_d_une_zone_agricole(
                total_area, crop_data, total_labor, total_water, total_machine_time
            )
            # Create a string representation of the dictionary
            optimal_solution = (
                "Optimal solution:\n"
                + "\n".join(
                    [f"Area for {c}: {areas[c]} hectares" for c in crop_data.keys()]
                )
                + f"\nTotal revenue: {revenue} UM"
            )
            results_text = tkinter.StringVar(value=optimal_solution)
            # Create a new CTkLabel with the string representation as the text
            results_label = customtkinter.CTkLabel(
                self,
                textvariable=results_text,
                width=120,
                height=25,
                fg_color=("white", "gray20"),
                corner_radius=8,
            )
            results_label.grid(row=0, column=10, padx=20, pady=10)

        self.solvebutton = customtkinter.CTkButton(
            self, text="solve", command=diplay_results
        )
        self.solvebutton.grid(row=2, column=10, padx=20, pady=10)



class MyFrame2(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        

        # table inputs

        #set the table in the GUI
        ##set the headers
        column_headers=["valeur"]
        row_headers=["Le nombre de barils de pétrole brut de type 1", "Le nombre de barils de pétrole brut de type 2", "Le niveau de qualité d'un baril de type 1", "Le niveau de qualité d'un baril de type 2", "Le niveau minimum de qualité de la gazoline", "Le niveau minimum de qualité du pétrole de chauffage", "Le prix de vente d'un baril de gazoline", "Le prix de vente d'un baril de pétrole de chauffage", "Les frais de marketing d'un baril de gazoline en dinars", "Les frais de marketing d'un baril de pétrole de chauffage en dinars"]

        ##set the default values
        global default_values 
        default_values = [[5000],[10000],[10],[5],[8],[6],[25],[20],[0.2],[0.1]]
        ##create the table and set it in the GUI
        rows, columns = matrix_dimensions(default_values)
        self.table = CustomTable(self, rows, columns, default_values, row_headers=row_headers, column_headers=column_headers)
        self.table.grid(row=0, column=2, padx=20, pady=10)


        #get values from the table
        def get_values(self):
            global table_values
            table_values = self.table.get_table_values()
            global brut1 , brut2, qualite_brut1, qualite_brut2, qualite_gazoline , qualite_petrole_chauffage, prix_gazoline, prix_petrole_chauffage, frais_marketing_gazoline, frais_marketing_petrole_chauffage
            vars =[]
            for i in range(10):
                vars.append(table_values[i][0])
            print(vars)
            for i in range(len(vars)):
                vars[i]= float(vars[i])
            brut1 = vars[0]
            brut2 = vars[1]
            qualite_brut1 = vars[2]
            qualite_brut2 = vars[3]
            qualite_gazoline = vars[4]
            qualite_petrole_chauffage = vars[5]
            prix_gazoline = vars[6]
            prix_petrole_chauffage = vars[7]
            frais_marketing_gazoline = vars[8]
            frais_marketing_petrole_chauffage = vars[9]


        self.getvals = customtkinter.CTkButton(self, text="update table values", command=lambda: get_values(self))
        self.getvals.grid(row=2, column=2, padx=20, pady=10)


        # button to call the solver function and display the results
        def diplay_results():
            results = optimize_petroleum_mix(brut1, brut2, qualite_brut1, qualite_brut2, qualite_gazoline, qualite_petrole_chauffage, prix_gazoline, prix_petrole_chauffage, frais_marketing_gazoline, frais_marketing_petrole_chauffage)
            # Create a string representation of the dictionary
            dict_str = "\n".join([f"{key}: {value}" for key, value in results.items()])
            results_text = tkinter.StringVar(value=dict_str)
            # Create a new CTkLabel with the string representation as the text
            results_label = customtkinter.CTkLabel(self,textvariable=results_text,width=120,height=25,fg_color=("white", "gray20"),corner_radius=8)
            results_label.grid(row=0, column=10, padx=20, pady=10)
        self.solvebutton = customtkinter.CTkButton(self, text="solve", command=diplay_results)
        self.solvebutton.grid(row=2, column=10, padx=20, pady=10)


class MyFrame3(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # table inputs
        column_headers = ["Parameter", "Value"]
        row_headers = [
            "days",
            "min_required",
            "work_days",
            "rest_days",
        ]
        default_values = [["7"], ["17,13,15,19,14,16,11"], ["5"], ["2"]]

        rows, columns = matrix_dimensions(default_values)
        self.table = CustomTable(
            self,
            rows,
            columns,
            default_values,
            row_headers=row_headers,
            column_headers=column_headers,
        )
        self.table.grid(row=2, column=10, padx=20, pady=10)

        # get values from the table
        def get_values(self):
            global days, min_required, work_days, rest_days
            table_values = self.table.get_table_values()
            days = int(table_values[0][0])
            min_required = [int(x) for x in table_values[1][0].split(",")]
            work_days = int(table_values[2][0])
            rest_days = int(table_values[3][0])

        self.getvals = customtkinter.CTkButton(
            self, text="update table values", command=lambda: get_values(self)
        )
        self.getvals.grid(row=15, column=10, padx=20, pady=10)

        # button to call the solver function and display the results
        def diplay_results():
            results = pl3_planification(days, min_required, work_days, rest_days)

            # Create a string representation of the dictionary
            results_text = tkinter.StringVar(value=results)
            # Create a new CTkLabel with the string representation as the text
            dict_str = "\n".join([f"{key}: {value}" for key, value in results.items()])
            results_text = tkinter.StringVar(value=dict_str)
            # Create a new CTkLabel with the string representation as the text
            results_label = customtkinter.CTkLabel(self,textvariable=results_text,width=120,height=25,fg_color=("white", "gray20"),corner_radius=8)
            results_label.grid(row=2, column=20, padx=20, pady=10)
            results_label = customtkinter.CTkLabel(self,textvariable=results_text,width=120,height=25,fg_color=("white", "gray20"),corner_radius=8)
        self.solvebutton = customtkinter.CTkButton(self, text="solve", command=diplay_results)
        self.solvebutton.grid(row=15, column=20, padx=20, pady=10)



class MyFrame4(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        
        # table inputs
        column_headers = ["Parameter", "Value"]
        row_headers = [
           "months",
           "demand",
           "initial_stock",
           "initial_workers",
           "worker_monthly_wage",
           "regular_hours_per_worker",
           "max_overtime_hours",
           "overtime_hourly_wage",
           "production_time_per_pair",
           "raw_material_cost",
           "raw_material_cost",
           "recruitment_cost",
           "recruitment_cost",
           "layoff_cost",
           "raw_material_cost",
           "stock_cost_per_pair"
       ]
       
        default_values = [["5"], ["3000, 5000, 2000, 1000, 1000"], ["500"], ["100"], ["1500"], ["160"], ["20"] , ["13"], ["4"], ["15"], ["1600"], ["2000"],["15"], ["3"]]
       
        rows, columns = matrix_dimensions(default_values)
        self.table = CustomTable(
            self,
            rows,
            columns,
            default_values,
            row_headers=row_headers,
            column_headers=column_headers,
        )
        self.table.grid(row=0, column=2, padx=20, pady=10)

        # get values from the table
        def get_values(self):
            global months, demand, initial_stock, initial_workers, worker_monthly_wage, regular_hours_per_worker, max_overtime_hours, overtime_hourly_wage, production_time_per_pair, raw_material_cost, recruitment_cost, layoff_cost, stock_cost_per_pair
            
            table_values = self.table.get_table_values()
            months = int(table_values[0][0])
            demand = [int(x) for x in table_values[1][0].split(",")]
            initial_stock = int(table_values[2][0])
            initial_workers = int(table_values[3][0])
            worker_monthly_wage = int(table_values[4][0])
            regular_hours_per_worker = int(table_values[5][0])
            max_overtime_hours = int(table_values[6][0])
            overtime_hourly_wage = int(table_values[7][0])
            production_time_per_pair = int(table_values[8][0])
            raw_material_cost = int(table_values[9][0])
            recruitment_cost = int(table_values[10][0])
            layoff_cost = int(table_values[11][0])
            raw_material_cost = int(table_values[12][0])
            stock_cost_per_pair = int(table_values[13][0])
        self.getvals = customtkinter.CTkButton(self, text="update table values", command=lambda: get_values(self))
        self.getvals.grid(row=2, column=2, padx=20, pady=10)


        # button to call the solver function and display the results
        def diplay_results():
            results = pl4_gestion_de_la_production(months, demand, initial_stock, initial_workers, worker_monthly_wage, regular_hours_per_worker, max_overtime_hours, overtime_hourly_wage, production_time_per_pair, raw_material_cost, recruitment_cost, layoff_cost, stock_cost_per_pair)
            
            dict_str = ""
            for k1, v1 in results.items():
                dict_str += f"Month {k1}:\n"
                for k2, v2 in v1.items():
                    dict_str += f" {k2}: {v2}\n"
            results_text = tkinter.StringVar(value=dict_str)
            # Create a string representation of the dictionary
            ###
            # Create a new CTkLabel with the string representation as the text
            results_label = customtkinter.CTkLabel(self,textvariable=results_text,width=120,height=100,fg_color=("white", "gray20"),corner_radius=8)
            results_label.grid(row=0, column=10, padx=20, pady=10)
            results_label = customtkinter.CTkLabel(self,textvariable=results_text,width=120,height=100,fg_color=("white", "gray20"),corner_radius=8)
        self.solvebutton = customtkinter.CTkButton(self, text="solve", command=diplay_results)
        self.solvebutton.grid(row=2, column=10, padx=20, pady=10)


class MyFrame5a(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        # inputs
        param_text_var = tkinter.StringVar(value="params")
        param_label = customtkinter.CTkLabel(self,textvariable=param_text_var,width=120,height=25,fg_color=("white", "gray20"),corner_radius=8)
        param_label.grid(row=0, column=0, padx=20, pady=10)
        entries = [    ("offres de centrale 1,2,3", "", "35,50,40"),
                       ("demandes maximal de ville 1,2,3,4", "", "45,20,30,30")]
                
        for i, (text, placeholder, default) in enumerate(entries):
            text_var = tkinter.StringVar(value=text)
            label = customtkinter.CTkLabel(self,textvariable=text_var,width=120,height=25,fg_color=("white", "gray20"),corner_radius=8)
            label.grid(row=i+1, column=0, padx=20, pady=10)
            entry = customtkinter.CTkEntry(self,placeholder_text=placeholder,width=120,height=25,border_width=2,corner_radius=10)
            entry.grid(row=i+1, column=1, padx=20, pady=10)
            entry.insert(0, default)
            setattr(self, f"entry{i+1}", entry)

        transport_costs = [
            [8, 6, 10, 9],
            [9, 12, 13, 7],
            [14, 9, 16, 5],
        ]
        # Create a function to be called when the button is clicked
        def update_x():
            global offres , demandes
            offres = [int(x) for x in self.entry1.get().split(",")]
            demandes = [int(x) for x in self.entry2.get().split(",")]
            
        # button to update values
        self.getbutton = customtkinter.CTkButton(self, text="update values", command=update_x)
        self.getbutton.grid(row=15, column=1, padx=20, pady=10)

        # button to call the solver function and display the results
        def diplay_results():
            solution, obj_val = optimal_electricity_supply(offres, demandes, transport_costs)
            # Create a string representation of the dictionary
            if solution is not None:
                optimal_solution = (
                    "Optimal solution found:\n"
                    + "\n".join(
                        [f"Supply {x_val} million KWh from Centrale {i + 1} to Ville {j + 1}"
                        for i, j, x_val in solution]
                    )
                    + f"\nObjective value: {obj_val}"
                )
            else:
                optimal_solution = "No optimal solution found."
            results_text = tkinter.StringVar(value=optimal_solution)
            # Create a new CTkLabel with the string representation as the text
            results_label = customtkinter.CTkLabel(self,textvariable=results_text,width=120,height=25,fg_color=("white", "gray20"),corner_radius=8)
            results_label.grid(row=20, column=0, padx=20, pady=10)
        self.solvebutton = customtkinter.CTkButton(self, text="solve", command=diplay_results)
        self.solvebutton.grid(row=16, column=1, padx=20, pady=10)

"""
class MyFrame5b(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
"""
class MyFrame6(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        #set the table in the GUI
        ##set the headers
        column_headers=["A", "B", "C", "D1", "D2", "E", "F"]
        row_headers=["A", "B", "C", "D1", "D2", "E", "F"]
        ##set the default values
        global default_values 
        default_values = [
            [float('nan'), 5, 3, 5, 5, 20, 20],
            [9, float('nan'), 9, 1, 1, 8, 15],
            [0.4, 8, float('nan'), 1, 0.5, 10, 12],
            [float('nan'), float('nan'), float('nan'), float('nan'), 1.2, 2, 12],
            [float('nan'), float('nan'), float('nan'), 8, float('nan'), 2, 12],
            [float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), 1],
            [float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), 7, float('nan')]
        ]
        ##create the table and set it in the GUI
        rows, columns = matrix_dimensions(default_values)
        self.table = CustomTable(self, rows, columns, default_values, row_headers=row_headers, column_headers=column_headers)
        self.table.grid(row=0, column=2, padx=20, pady=10)


        #get values from the table
        def get_values(self):
            global table_values
            table_values = self.table.get_table_values()
            print(table_values)
        self.getvals = customtkinter.CTkButton(self, text="update table values", command=lambda: get_values(self))
        self.getvals.grid(row=2, column=2, padx=20, pady=10)
        
        
        
        # button to call the solver function and display the results
        def diplay_results(table_values):
            for i in range(len(table_values)):
               for j in range(len(table_values[i])):
                    table_values[i][j] = float(table_values[i][j])
            capacities = [200, 300, 100]
            client_demands = [400, 180]
            transport_costs_matrix = pd.DataFrame(
                table_values,
                columns=["A", "B", "C", "D1", "D2", "E", "F"],
                index=["A", "B", "C", "D1", "D2", "E", "F"],
            )

            solution, obj_val = optimize_distribution(capacities, client_demands, transport_costs_matrix)
        

            results_text = ""
            if solution is not None:
                results_text += "Optimal solution found:\n"
                for i, j, x_val in solution:
                    results_text += f"Transport {x_val} tonnes from {i} to {j}\n"
                results_text += f"Objective value: {obj_val}\n"
            else:
                results_text += "No optimal solution found.\n"

            # Create a new CTkLabel with the string representation as the text
            results_label1 = customtkinter.CTkLabel(self,text=results_text,width=120,height=25,fg_color=("white", "gray20"),corner_radius=8)
            results_label1.grid(row=0, column=10, padx=20, pady=10)
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
        self.button = customtkinter.CTkButton(self, text="graphe", command=lambda: display_logistic_graph(transport_costs_matrix))
        self.button.grid(row=2, column=20,padx=20, pady=10)
            
        self.solvebutton = customtkinter.CTkButton(self, text="solve", command=lambda: diplay_results(table_values))
        self.solvebutton.grid(row=2, column=10, padx=20, pady=10)







class MyFrame7(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)


        #set the table in the GUI
        ##set the headers
        row_headers= ["Entreprise 1", "Entreprise 2", "Entreprise 3", "Entreprise 4", "Entreprise 5", "Entreprise 6"]
        column_headers  = ["projet 1  ", "projet 2  ", "projet 3  ", "projet 4  ", "projet 5  ", "projet 6  ", "projet 7  ", "projet 8  "]
        ##set the default values
        global default_values 
        default_values = [
                [float('nan'), 8200, 7800, 5400, float('nan'), 3900, float('nan'), float('nan')],
                [7800, 8200, float('nan'), 6300, float('nan'), 3300, 4900, float('nan')],
                [float('nan'), 4800, float('nan'), float('nan'), float('nan'), 4400, 5600, 3600],
                [float('nan'), float('nan'), 8000, 5000, 6800, float('nan'), 6700, 4200],
                [7200, 6400, float('nan'), 3900, 6400, 2800, float('nan'), 3000],
                [7000, 5800, 7500, 4500, 5600, float('nan'), 6000, 4200]
            ]
        #create the table and set it in the GUI
        rows, columns = matrix_dimensions(default_values)
        self.table = CustomTable(self, rows, columns, default_values, row_headers=row_headers, column_headers=column_headers)
        self.table.grid(row=0, column=2, padx=20, pady=10)

        #get values from the table
        def get_values(self):
            global table_values
            table_values = self.table.get_table_values()
            print(table_values)
        self.getvals = customtkinter.CTkButton(self, text="update table values", command=lambda: get_values(self))
        self.getvals.grid(row=2, column=2, padx=20, pady=10)


        # button to call the solver function and display the results
        def diplay_results(table_values):
            for i in range(len(table_values)):
               for j in range(len(table_values[i])):
                    table_values[i][j] = float(table_values[i][j])

            assignment, obj_val = optimize_assignment(table_values)
            # Create a string representation of the dictionary
            if assignment:
                optimal_solution = (
                    "Optimal solution found:\n"
                    + "\n".join(
                        [f"Assign project {j} to company {i}" for i, j in assignment]
                    )
                    + f"\nObjective value: {obj_val}"
                )
            else:
                optimal_solution = "No optimal solution found."

            results_text = tkinter.StringVar(value=optimal_solution)
            # Create a new CTkLabel with the string representation as the text
            results_label = customtkinter.CTkLabel(self,textvariable=results_text,width=120,height=25,fg_color=("white", "gray20"),corner_radius=8)
            results_label.grid(row=0, column=10, padx=20, pady=10)
        self.solvebutton = customtkinter.CTkButton(self, text="solve", command=lambda: diplay_results(table_values))
        self.solvebutton.grid(row=2, column=10, padx=20, pady=10)


class MyFrame8(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # set the default values for the matrix and show it in the GUI
        global default_values 
        default_values = [
                    [float('nan'), 70, 63, 56, float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), float('nan')],
                    [float('nan'), float('nan'), 25, 19, 73, 50, 79, float('nan'), float('nan'), float('nan')],
                    [float('nan'), 25, float('nan'), 29, 69, 61, float('nan'), float('nan'), float('nan'), float('nan')],
                    [float('nan'), 19, 29, float('nan'), 67, 45, float('nan'), float('nan'), 85, float('nan')],
                    [float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), 18, 67, 69, 54, 87],
                    [float('nan'), float('nan'), float('nan'), float('nan'), 18, float('nan'), 72, 52, 51, 97],
                    [float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), 17, 31, 72],
                    [float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), 17, float('nan'), 15, float('nan')],
                    [float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), 31, 15, float('nan'), 69],
                    [float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), float('nan')]
                ]
        
        row_headers = ["ville 1 ", "ville 2  ", "ville 3  ", "ville 4  ", "ville 5  ", "ville 6  ", "ville 7  ", "ville 8  ", "ville 9  ", "ville 10  "]
        column_headers = ["ville 1 ", "ville 2  ", "ville 3  ", "ville 4  ", "ville 5  ", "ville 6  ", "ville 7  ", "ville 8  ", "ville 9  ", "ville 10  "]

        rows, columns = matrix_dimensions(default_values)
        self.table = CustomTable(self, rows, columns, default_values, row_headers=row_headers, column_headers=column_headers)
        self.table.grid(row=0, column=2, padx=20, pady=10)

        # button to get values from the table
        def get_values(self):
            global table_values
            table_values = self.table.get_table_values()
            print(table_values)
        self.getvals = customtkinter.CTkButton(self, text="update table values", command=lambda: get_values(self))
        self.getvals.grid(row=2, column=2, padx=20, pady=10)


        # button to call the solver function and display the results
        def diplay_results(table_values):
            for i in range(len(table_values)):
               for j in range(len(table_values[i])):
                    table_values[i][j] = float(table_values[i][j])

            graph = {i: {} for i in range(1, 11)}
            for i, row in enumerate(table_values, start=1):
                for j, distance in enumerate(row, start=1):
                    if not (distance != distance):  # Check if it's not nan
                        graph[i][j] = distance

            shortest_path_distance = dijkstra(graph, 1, 10)
            # Create a string representation of the dictionary
            optimal_solution=(f"The shortest path distance between city 1 and city 10 is:\n {shortest_path_distance}")

            results_text = tkinter.StringVar(value=optimal_solution)
            # Create a new CTkLabel with the string representation as the text
            results_label = customtkinter.CTkLabel(self,textvariable=results_text,width=120,height=25,fg_color=("white", "gray20"),corner_radius=8)
            results_label.grid(row=0, column=10, padx=20, pady=10)
        self.solvebutton = customtkinter.CTkButton(self, text="solve", command=lambda : diplay_results(table_values))
        self.solvebutton.grid(row=2, column=10, padx=20, pady=10)


class MyFrame9(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        # button to call the solver function and display the results
        def diplay_results():
            # Define data
            plants = ['Usine1', 'Usine2', 'Usine3', 'Usine4', 'Usine5']
            depots = ['Depot1', 'Depot2', 'Depot3']
            clients = ['Client1', 'Client2', 'Client3', 'Client4']

            production_capacity = [300, 200, 300, 200, 400]
            prod_to_depot_cost = [
                [800, 1000, 1200],
                [700, 500, 700],
                [800, 600, 500],
                [500, 600, 700],
                [700, 600, 500]
            ]
            depot_to_client_cost = [
                [40, 80, 90, 50],
                [70, 40, 60, 80],
                [80, 30, 50, 60]
            ]
            client_demand = [200, 300, 150, 250]
            fixed_costs = [35000, 45000, 40000, 42000, 40000, 40000, 20000, 60000]

            results = tomo_optimization(plants, depots, clients, production_capacity, prod_to_depot_cost, depot_to_client_cost, client_demand, fixed_costs)
            # Create a string representation of the dictionary

            results_text = tkinter.StringVar(value=results)
            # Create a new CTkLabel with the string representation as the text
            results_label = customtkinter.CTkLabel(self,textvariable=results_text,width=120,height=25,fg_color=("white", "gray20"),corner_radius=8)
            results_label.grid(row=20, column=0, padx=20, pady=10)
        self.solvebutton = customtkinter.CTkButton(self, text="solve", command=diplay_results)
        self.solvebutton.grid(row=16, column=1, padx=20, pady=10)
    

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Projet RO")
        self.geometry("900x1000")


        # set grid layout 1x2
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

       
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(10, weight=1)
        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=20,width=30, border_spacing=10, text="Home",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   anchor="w", command=self.home_button_event)
        self.home_button.grid(row=0, column=0, sticky="ew") # positionnement dans la seconde colonne
        

########### navigation bar buttons 
        frames = ["PL 1",
                  "PL 2", 
                  "PL 3",
                  "PL 4", 
                  "PL 5", 
                  "PL 6 ",
                  "PL 7 ",
                  "PL 8 ",
                  "PL 9"]

        for i, frame in enumerate(frames, start=1):
            if True : 
                button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=20,width=30, border_spacing=10, text=frame,
                                                fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                               anchor="w", command=getattr(self, f"frame_{i}_button_event"))
                button.grid(row=0, column=i+1, sticky="ew")
                setattr(self, f"frame_{i}_button", button)


        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Light", "Dark", "System"],
                                                                  command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=0, column=11, padx=20, pady=20, sticky="s")

       

        # create the frames (frame for each PL)
        self.home_frame = home(master=self)

        self.first_frame = MyFrame1(master=self)
        self.second_frame = MyFrame2(master=self)
        self.third_frame = MyFrame3(master=self)
        self.fourth_frame = MyFrame4(master=self)
        self.fifth_framea = MyFrame5a(master=self)
        self.sixth_frame = MyFrame6(master=self)
        self.seventh_frame = MyFrame7(master=self)
        self.eighth_frame = MyFrame8(master=self)
        self.ninth_frame = MyFrame9(master=self)

        # select default frame
        self.select_frame_by_name("home")

       
    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_1_button.configure(fg_color=("gray75", "gray25") if name == "frame_1" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
        self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")
        self.frame_4_button.configure(fg_color=("gray75", "gray25") if name == "frame_4" else "transparent")
        self.frame_5_button.configure(fg_color=("gray75", "gray25") if name == "frame_5" else "transparent")
        self.frame_6_button.configure(fg_color=("gray75", "gray25") if name == "frame_6" else "transparent")
        self.frame_7_button.configure(fg_color=("gray75", "gray25") if name == "frame_7" else "transparent")
        self.frame_8_button.configure(fg_color=("gray75", "gray25") if name == "frame_8" else "transparent")
        self.frame_9_button.configure(fg_color=("gray75", "gray25") if name == "frame_9" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=1, column=0, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "frame_1":
            self.first_frame.grid(row=1, column=0, sticky="nsew")
        else:
            self.first_frame.grid_forget()
        if name == "frame_2":
            self.second_frame.grid(row=1, column=0, sticky="nsew")
        else:
            self.second_frame.grid_forget()
        if name == "frame_3":
            self.third_frame.grid(row=1, column=0, sticky="nsew")
        else:
            self.third_frame.grid_forget()
        if name == "frame_4":
            self.fourth_frame.grid(row=1, column=0, sticky="nsew")
        else:
            self.fourth_frame.grid_forget()
        if name == "frame_5":
            self.fifth_framea.grid(row=1, column=0, sticky="nsew")
        else:
            self.fifth_framea.grid_forget()
        if name == "frame_6":
            self.sixth_frame.grid(row=1, column=0, sticky="nsew")
        else:
            self.sixth_frame.grid_forget()
        if name == "frame_7":
            self.seventh_frame.grid(row=1, column=0, sticky="nsew")
        else:
            self.seventh_frame.grid_forget()
        if name == "frame_8":
            self.eighth_frame.grid(row=1, column=0, sticky="nsew")
        else:
            self.eighth_frame.grid_forget()
        if name == "frame_9":
            self.ninth_frame.grid(row=1, column=0, sticky="nsew")
        else:
            self.ninth_frame.grid_forget()


    def home_button_event(self):
        self.select_frame_by_name("home")

    def frame_1_button_event(self):
        self.select_frame_by_name("frame_1")

    def frame_2_button_event(self):
        self.select_frame_by_name("frame_2")

    def frame_3_button_event(self):
        self.select_frame_by_name("frame_3")

    def frame_4_button_event(self):
        self.select_frame_by_name("frame_4")

    def frame_5_button_event(self):
        self.select_frame_by_name("frame_5a")

    def frame_6_button_event(self):
        self.select_frame_by_name("frame_6")
    
    def frame_7_button_event(self):
        self.select_frame_by_name("frame_7")

    def frame_8_button_event(self):
        self.select_frame_by_name("frame_8")

    def frame_9_button_event(self): 
        self.select_frame_by_name("frame_9")


    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)


if __name__ == "__main__":
    app = App()
    app.mainloop()

