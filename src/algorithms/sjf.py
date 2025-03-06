from algorithms.graph import Graph

class Sjf(Graph):

    def eliminateProcess(self, processes, executed_processes):
        return [p for p in processes if p['nombre'] not in executed_processes]

    def getProcessAvailable(self, processes, current_time, executed_processes):
        return [p for p in processes if p['tiempo de llegada'] <= current_time and p['nombre'] not in executed_processes]
        
    def calculateProcesses(self, processes):  
        processes = sorted(processes, key=lambda p: p['tiempo de llegada']) 
        process_list = []
        executed_processes = []
        current_time = 0

        while processes:
            processes = self.eliminateProcess(processes, executed_processes)
            available_processes = self.getProcessAvailable(processes, current_time, executed_processes)

            if not available_processes:
                if not processes:
                    break 
                current_time = processes[0]['tiempo de llegada']
                available_processes = self.get_available_processes(processes, current_time, executed_processes)

            available_processes.sort(key=lambda p: p['rafaga'])

            for process in available_processes:
                start_time = current_time
                end_time = start_time + process['rafaga']
                current_time = end_time

                self.wait_time += start_time - process['tiempo de llegada']
                self.sistem_time += end_time - process['tiempo de llegada']

                process_list.append((process['nombre'], start_time, end_time))
                executed_processes.append(process['nombre'])

        return sorted(process_list, key=lambda p: p[0]) 
