from abc import ABC, abstractmethod
import matplotlib.pyplot as plt

class Graph(ABC):

  def __init__(self, process):
    self.process = process
    self.wait_time = 0
    self.sistem_time = 0
    self.process_executed = self.calculateProcesses(process)

  def getProcessExecuted(self):
    return self.process_executed

  def getWaitTime(self):
    return self.wait_time / len(self.process)

  def getSistemTime(self):
    return self.sistem_time / len(self.process)

  @abstractmethod
  def calculateProcesses(self):
    pass

  def graph(self, algoritmo):
    procesos_intervalos = {}
    for proceso, inicio, fin in self.process_executed:
        if proceso not in procesos_intervalos:
            procesos_intervalos[proceso] = []
        procesos_intervalos[proceso].append((inicio, fin))

    # Obtener un color único para cada proceso
    colores = plt.cm.get_cmap("tab10", len(procesos_intervalos))
    color_map = {proceso: colores(i) for i, proceso in enumerate(procesos_intervalos.keys())}

    # Crear el gráfico de Gantt
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_title(f"Diagrama de Gantt - {algoritmo}")
    ax.set_xlabel("Tiempo")
    ax.set_ylabel("Proceso")

    # Dibujar los intervalos de tiempo
    for i, (proceso, intervalos) in enumerate(procesos_intervalos.items()):
        for (inicio, fin) in intervalos:
            ax.barh(y=i, width=fin - inicio, left=inicio, color=color_map[proceso], align="center", height=0.3)
            ax.text(inicio + (fin - inicio) / 2, i, f"{inicio}-{fin}", ha="center", va="center", color="white", fontsize=9)

    # Configuración de ejes
    max_time = max(fin for _, _, fin in self.process_executed)
    ax.set_xlim(0, max_time)
    ax.set_yticks(range(len(procesos_intervalos)))
    ax.set_yticklabels(list(procesos_intervalos.keys()))

    # Ajustar los márgenes de la gráfica
    plt.subplots_adjust(bottom=0.198, top=0.936)

    # Mostrar métricas debajo del gráfico
    plt.text(0, -1, f"TE: {self.getWaitTime():.2f}s", fontsize=10)
    plt.text(3, -1, f"TS: {self.getSistemTime():.2f}s", fontsize=10)

    # Agregar la leyenda con los colores de los procesos
    legend_patches = [plt.Line2D([0], [0], color=color_map[proceso], lw=4, label=proceso) for proceso in procesos_intervalos.keys()]
    ax.legend(handles=legend_patches, title="Procesos", loc="center left", bbox_to_anchor=(1, 0.5))

    plt.show()

