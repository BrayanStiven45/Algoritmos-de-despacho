from algorithms.fifo import Fifo
from algorithms.sjf import Sjf
from algorithms.priority import Prioridad
from algorithms.RR import RoundRobin
import tkinter as tk
from tkinter import ttk

# procesos = [
#     {"nombre": "A", "rafaga": 6, 'tiempo de llegada': 0,  "prioridad": 2},
#     {"nombre": "B", "rafaga": 4, 'tiempo de llegada': 1,  "prioridad": 1},
#     {"nombre": "C", "rafaga": 2, 'tiempo de llegada': 2,  "prioridad": 3},
#     {"nombre": "D", "rafaga": 3, 'tiempo de llegada': 3, "prioridad": 2},
# ]

class SchedulerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Algoritmos")

        self.procesos = [
            {"nombre": "A", "rafaga": 6, "tiempo de llegada": 0, "prioridad": 2},
            {"nombre": "B", "rafaga": 4, "tiempo de llegada": 1, "prioridad": 1},
            {"nombre": "C", "rafaga": 2, "tiempo de llegada": 2, "prioridad": 0},
            {"nombre": "D", "rafaga": 3, "tiempo de llegada": 3, "prioridad": 1},
        ]

        self.algoritmos = ["FIFO", "SJF", "Prioridad", "Round Robin"]
        self.selected_algorithm = tk.StringVar(value=self.algoritmos[0])
        
        self.create_widgets()
        self.update_table()

    def create_widgets(self):
        # Frame para la tabla (izquierda)
        self.table_frame = tk.Frame(self.root)
        self.table_frame.pack(side=tk.LEFT, padx=10, pady=10)

        # Tabla
        self.tree = ttk.Treeview(self.table_frame, columns=("nombre", "rafaga", "tiempo de llegada"), show="headings")
        self.tree.heading("nombre", text="Proceso")
        self.tree.heading("rafaga", text="Ráfaga")
        self.tree.heading("tiempo de llegada", text="Tiempo de llegada")
        self.tree.pack()
        
        # Hacer la tabla editable
        self.tree.bind("<Double-1>", self.on_double_click)

        # Frame para controles (derecha)
        self.controls_frame = tk.Frame(self.root)
        self.controls_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        # Selección de algoritmo
        tk.Label(self.controls_frame, text="Selecciona un algoritmo").pack()
        self.algorithm_menu = ttk.Combobox(self.controls_frame, values=self.algoritmos, textvariable=self.selected_algorithm, state="readonly")
        self.algorithm_menu.pack()
        self.algorithm_menu.bind("<<ComboboxSelected>>", self.update_table)

        # Campo Quantum (solo para Round Robin)
        self.quantum_label = tk.Label(self.controls_frame, text="Quantum:")
        self.quantum_entry = tk.Entry(self.controls_frame)

        # Botón para ejecutar
        self.run_button = tk.Button(self.controls_frame, text="Ejecutar", command=self.run_algorithm)
        self.run_button.pack(pady=5)

    def update_table(self, event=None):
        # Limpiar tabla
        for col in self.tree['columns']:
            self.tree.heading(col, text="")
        self.tree.delete(*self.tree.get_children())

        # Obtener algoritmo seleccionado
        algo = self.selected_algorithm.get()
        columns = ["nombre", "rafaga", "tiempo de llegada"]
        if algo == "Prioridad":
            columns.append("prioridad")
        
        self.tree.configure(columns=columns)
        for col in columns:
            self.tree.heading(col, text=col.capitalize())

        # Insertar datos
        for p in self.procesos:
            values = [p[col] for col in columns]
            self.tree.insert("", tk.END, values=values)

        # Mostrar u ocultar quantum
        if algo == "Round Robin":
            self.quantum_label.pack()
            self.quantum_entry.pack()
        else:
            self.quantum_label.pack_forget()
            self.quantum_entry.pack_forget()

    def on_double_click(self, event):
        item = self.tree.identify_row(event.y)
        column = self.tree.identify_column(event.x)
        if item and column:
            col_index = int(column[1:]) - 1
            entry = tk.Entry(self.root)
            entry.place(x=event.x_root, y=event.y_root, width=50)
            entry.focus()
            
            def on_enter(event):
                new_value = entry.get()
                current_values = list(self.tree.item(item, 'values'))
                current_values[col_index] = new_value
                self.tree.item(item, values=current_values)
                entry.destroy()
            
            entry.bind("<Return>", on_enter)
            entry.bind("<FocusOut>", lambda e: entry.destroy())

    def run_algorithm(self):
        algo = self.selected_algorithm.get()
        quantum = int(self.quantum_entry.get()) if algo == "Round Robin" else None
        
        procesos = [
            {"nombre": self.tree.item(item)['values'][0], "rafaga": int(self.tree.item(item)['values'][1]),
             "tiempo de llegada": int(self.tree.item(item)['values'][2]), "prioridad": int(self.tree.item(item)['values'][3]) if algo == "Prioridad" else None}
            for item in self.tree.get_children()
        ]

        if algo == "FIFO":
            sim = Fifo(procesos)
        elif algo == "SJF":
            sim = Sjf(procesos)
        elif algo == "Prioridad":
            sim = Prioridad(procesos)
        elif algo == "Round Robin":
            sim = RoundRobin(procesos, quantum)
        
        sim.graph(algo)

if __name__ == "__main__":
    root = tk.Tk()
    app = SchedulerApp(root)
    root.mainloop()
