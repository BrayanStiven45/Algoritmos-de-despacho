from algorithms.graph import Graph

class Prioridad(Graph):

  def ordenarPrioridad(self, processes, current_time):
        # Filtrar los procesos que han llegado hasta el tiempo actual
        process_ejecute = [process for process in processes if process['tiempo de llegada'] <= current_time]

        # Eliminar de la lista principal los procesos que han llegado hasta el tiempo actual
        processes = [process for process in processes if process['tiempo de llegada'] > current_time]

        # Ordenar los procesos por prioridad
        return processes, sorted(process_ejecute, key=lambda p: p['prioridad'])

  def calculateProcesses(self, processes):
      process_list = []  # Lista donde almacenaremos el nombre y los tiempos de los procesos
      current_time = 0  # Inicializamos el tiempo actual en 0
      processes = sorted(processes, key=lambda p: p['tiempo de llegada'])
      processes_copy = processes.copy()

      while processes_copy:
          # Ordenar y obtener los procesos que han llegado hasta el tiempo actual
          processes_copy, process_ejecute = self.ordenarPrioridad(processes_copy, current_time)
          if not process_ejecute:
            current_time += 1

          for process in process_ejecute:

              # Si el proceso llega después del tiempo actual, actualizamos current_time
              if process['tiempo de llegada'] > current_time:
                  current_time = process['tiempo de llegada']

              # El tiempo de inicio es el tiempo actual
              start_time = current_time
              # Incrementamos el tiempo actual con la ráfaga del proceso
              current_time += process['rafaga']
              # El tiempo de finalización es el nuevo tiempo actual
              end_time = current_time

              # Calculamos el tiempo de espera: tiempo total desde que llegó hasta que comenzó a ejecutarse
              wait_time = start_time - process['tiempo de llegada']
              self.wait_time += wait_time

              # El tiempo de sistema es el tiempo total desde que llegó hasta que terminó de ejecutarse
              system_time = end_time - process['tiempo de llegada']
              self.sistem_time += system_time

              # Guardamos el nombre del proceso y los tiempos de inicio y fin
              process_list.append((process['nombre'], start_time, end_time))

    #   self.sistem_time /= len(processes)
    #   self.wait_time /= len(processes)
      # Devolver la lista con los procesos y los tiempos, junto con los tiempos acumulados de espera y sistema
      return sorted(process_list, key=lambda p: p[0])