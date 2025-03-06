from algorithms.graph import Graph

class Fifo(Graph):

  def calculateProcesses(self, process):
    process = sorted(process, key=lambda p: p['tiempo de llegada'])
    process_list = []
    current_time = 0

    for process in process:
      if process['tiempo de llegada'] > current_time:
        current_time = process['tiempo de llegada']

      start_time = current_time
      current_time += process['rafaga']
      end_time = current_time

      self.wait_time += start_time - process['tiempo de llegada']
      self.sistem_time += end_time - process['tiempo de llegada']

      process_list.append((process['nombre'], start_time, end_time))

    return process_list


