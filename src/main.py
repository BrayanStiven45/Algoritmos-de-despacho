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
        # Frame para la tabla
        self.table_frame = tk.Frame(self.root)
        self.table_frame.pack(side=tk.LEFT, padx=10, pady=10)

        # Tabla de procesos
        self.tree = ttk.Treeview(self.table_frame, columns=("nombre", "rafaga", "tiempo de llegada", "prioridad"), show="headings")
        for col in ["nombre", "rafaga", "tiempo de llegada", "prioridad"]:
            self.tree.heading(col, text=col.capitalize())
        self.tree.pack()
        
        # Hacer la tabla editable
        self.tree.bind("<Double-1>", self.on_double_click)

        # Frame de controles
        self.controls_frame = tk.Frame(self.root)
        self.controls_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        # Selección de algoritmo
        tk.Label(self.controls_frame, text="Selecciona un algoritmo").pack()
        self.algorithm_menu = ttk.Combobox(self.controls_frame, values=self.algoritmos, textvariable=self.selected_algorithm, state="readonly")
        self.algorithm_menu.pack()
        self.algorithm_menu.bind("<<ComboboxSelected>>", self.update_table)

        # Campo Quantum
        self.quantum_label = tk.Label(self.controls_frame, text="Quantum:")
        self.quantum_entry = tk.Entry(self.controls_frame)

        # Botones de control
        self.add_button = tk.Button(self.controls_frame, text="Nuevo Proceso", command=self.add_process_window)
        self.add_button.pack(pady=5)

        self.delete_button = tk.Button(self.controls_frame, text="Eliminar Proceso", command=self.delete_process)
        self.delete_button.pack(pady=5)

        self.run_button = tk.Button(self.controls_frame, text="Ejecutar", command=self.run_algorithm)
        self.run_button.pack(pady=5)

    def update_table(self, event=None):
        self.tree.delete(*self.tree.get_children())  # Limpiar la tabla

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

    def add_process_window(self):
        """ Abre una nueva ventana para agregar un proceso """
        new_window = tk.Toplevel(self.root)
        new_window.title("Nuevo Proceso")
        new_window.geometry("250x200")

        tk.Label(new_window, text="Nombre:").pack()
        name_entry = tk.Entry(new_window)
        name_entry.pack()

        tk.Label(new_window, text="Ráfaga:").pack()
        burst_entry = tk.Entry(new_window)
        burst_entry.pack()

        tk.Label(new_window, text="Tiempo de llegada:").pack()
        arrival_entry = tk.Entry(new_window)
        arrival_entry.pack()

        tk.Label(new_window, text="Prioridad:").pack()
        priority_entry = tk.Entry(new_window)
        priority_entry.pack()

        def add_process():
            nombre = name_entry.get().strip()
            try:
                rafaga = int(burst_entry.get())
                tiempo_llegada = int(arrival_entry.get())
                prioridad = int(priority_entry.get())
                
                if not nombre:
                    raise ValueError("El nombre no puede estar vacío.")
                
                self.procesos.append({
                    "nombre": nombre,
                    "rafaga": rafaga,
                    "tiempo de llegada": tiempo_llegada,
                    "prioridad": prioridad
                })
                
                self.update_table()
                new_window.destroy()
            except ValueError:
                messagebox.showerror("Error", "Por favor, ingrese valores válidos.")

        tk.Button(new_window, text="Agregar", command=add_process).pack(pady=10)

    def delete_process(self):
        """ Elimina el proceso seleccionado de la tabla """
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Atención", "Seleccione un proceso para eliminar.")
            return
        
        for item in selected_item:
            proceso_nombre = self.tree.item(item, "values")[0]
            self.procesos = [p for p in self.procesos if p["nombre"] != proceso_nombre]
            self.tree.delete(item)

    def run_algorithm(self):
        """ Ejecuta el algoritmo seleccionado con los datos actuales """
        algo = self.selected_algorithm.get()
        quantum = int(self.quantum_entry.get()) if algo == "Round Robin" else None
        
        procesos = [
            {"nombre": self.tree.item(item)['values'][0], 
             "rafaga": int(self.tree.item(item)['values'][1]),
             "tiempo de llegada": int(self.tree.item(item)['values'][2]),
             "prioridad": int(self.tree.item(item)['values'][3]) if algo == "Prioridad" else None}
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
