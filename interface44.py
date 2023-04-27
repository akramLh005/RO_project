import tkinter
import tkinter.messagebox
import customtkinter

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Tp Recherche Operationnelle")
        self.geometry(f"{1100}x{580}")


        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="TP Recherche Operationnelle", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=80, pady=(20, 10))
       
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 60))

        # create textbox
        self.textbox = customtkinter.CTkTextbox(self, width=400)
        self.textbox.grid(row=0, column=0, padx=(20, 20), pady=(100, 300), sticky="nsew")
        
        # create tabview
        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.grid(row=0, column=1, padx=(100, 100), pady=(100, 100), sticky="nsew")
        self.tabview.add("TP Recherche Opérationnelle")
   
        self.tabview.tab("TP Recherche Opérationnelle").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs

        self.combobox_1 = customtkinter.CTkComboBox(self.tabview.tab("TP Recherche Opérationnelle"),values=["PL1", "PL2","PL3","PL4", "PL5", "PL6","PL7", "PL8","PL9"])
        self.combobox_1.grid(row=1, column=0, padx=20, pady=(10, 70))
        self.string_input_button = customtkinter.CTkButton(self.tabview.tab("TP Recherche Opérationnelle"), text="Ouvrir le PL",command=self.open_input_dialog_event)
        self.string_input_button.grid(row=2, column=0, padx=20, pady=(10, 40))



        # set default values
    
    
       
        self.appearance_mode_optionemenu.set("Mode")

       
        self.combobox_1.set("Choisir la PL")
        self.textbox.insert("0.0", "\n\n" + "L'interface que nous avons développée pour notre projet de recherche opérationnelle permettra de présenter de manière claire et concise les neuf problèmes linéaires (PL) que nous avons travaillés sur les deux séries de PL fournies.   En somme, cette interface permettra de présenter efficacement notre travail sur les PL et de faciliter la saisie des variables nécessaires pour la résolution des problèmes.\n\n" * 1)
        
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


if __name__ == "__main__":
    app = App()
    app.mainloop()