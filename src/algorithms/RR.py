from collections import deque
import matplotlib.pyplot as plt
from algorithms.graph import Graph

class RoundRobin(Graph):
    def __init__(self, processes, quantum):
        self.processes = sorted(processes, key=lambda p: p['tiempo de llegada'])  # Orden inicial por llegada
        self.quantum = quantum
        self.wait_time = 0
        self.sistem_time = 0
        self.process_executed = self.calculateProcesses()

    def calculateProcesses(self):
        queue = deque(self.processes)  # Cola de procesos
        current_time = 0
        executed_processes = []
        remaining_time = {p['nombre']: p['rafaga'] for p in self.processes}  # Tiempo restante por proceso
        arrival_time = {p['nombre']: p['tiempo de llegada'] for p in self.processes}  # Tiempo de llegada por proceso
        last_execution = {}  # Última ejecución para calcular tiempos de espera

        while queue:
            process = queue.popleft()  # Sacar el primer proceso en la cola
            nombre = process['nombre']
            start_time = max(current_time, arrival_time[nombre])  # Inicio después de la llegada del proceso
            burst = min(remaining_time[nombre], self.quantum)  # Ejecutar hasta el quantum o menos si es el último ciclo
            
            end_time = start_time + burst
            executed_processes.append((nombre, start_time, end_time))

            # Calcular tiempos de espera y en sistema
            if nombre in last_execution:
                self.wait_time += start_time - last_execution[nombre]  # Tiempo de espera entre ejecuciones
            else:
                self.wait_time += start_time - arrival_time[nombre]  # Primera espera desde llegada
            
            self.sistem_time += end_time - arrival_time[nombre]  # Tiempo total en el sistema
            last_execution[nombre] = end_time  # Registrar última ejecución

            # Actualizar tiempo restante
            remaining_time[nombre] -= burst
            if remaining_time[nombre] > 0:
                queue.append(process)  # Volver a poner en la cola si aún tiene tiempo de CPU

            current_time = end_time  # Avanzar el tiempo actual

        return executed_processes

    def getProccessExecuted(self):
        return self.process_executed

    def getWaitTime(self):
        return self.wait_time / len(self.processes) if self.processes else 0

    def getSistemTime(self):
        return self.sistem_time / len(self.processes) if self.processes else 0