# -*- coding: utf-8 -*-
"""M1_Actividad.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ca09Tq22OPALJ8XoqZ1omv0V1weWa29N

# Herramienta para la implementación de sistemas multiagentes
Carlos Moisés Chávez Jiménez A01637322
09/11/2021

## Descripción del código
Simulación de la limpieza de una habitación utilizando sistemas multiagentes

### Instalación de la librería agentpy
"""

!pip install agentpy

"""### Importamos las librerías a utilizar"""

# Model design
import agentpy as ap

# Visualization
import matplotlib.pyplot as plt
import seaborn as sns
import IPython

"""### Declaramos la clase contiene las funciones con las que trabajaremos
- La primer función declara los agentes, la cuadricula e inicializa la limpieza
- La segunda función se encarga de trabajar los espacios sucios
- La tercera documenta el final de la simulación
"""

class Limpieza(ap.Model):

    # Creación de los agentes y de la habitación.
    def setup(self):
        n_tiles = int(self.p['azulejos sucios'] * (self.p.size**2))
        tiles = self.agents = ap.AgentList(self, n_tiles)
        self.room = ap.Grid(self, [self.p.size]*2, track_empty=True)
        self.room.add_agents(tiles, random=True, empty=True)
        self.agents.condition = 0
        unfortunate_tiles = self.room.agents[0:self.p.size, 0:2]
        unfortunate_tiles.condition = 1

    def step(self):
        # Se selecciona el azulejo a limpiar
        cleaned_tiles = self.agents.select(self.agents.condition == 1)
        for tile in cleaned_tiles:
            for neighbor in self.room.neighbors(tile):
                if neighbor.condition == 0:
                    neighbor.condition = 1
            tile.condition = 2 # se marca como azulejo limpio
        # Se detiene si ya no hay azulejos por limpiar
        if len(cleaned_tiles) == 0:
            self.stop()
    # Se documenta la limpieza
    def end(self):
        cleaned_tiles = len(self.agents.select(self.agents.condition == 2))
        self.report('porcentaje de azulejos limpios',
                    cleaned_tiles / len(self.agents))

"""### Definimos los parametros de la cuadricula y la cantidad de pasos"""

parameters = {
    'azulejos sucios': 0.7,
    'size': 50, # Tamaño de la habitación
    'steps': 100,
}

"""### Declaramos la función de animación
Aqui es donde armamos la animación de la limpieza y la desplegamos.
"""

# Creamos la animación

def animation_plot(model, ax):
    attr_grid = model.room.attr_grid('condition')
    color_dict = {0:'#711D00', 1:'#00A5D8', 2:'#DCDCDC', None:'#D8C9BD'}
    ap.gridplot(attr_grid, ax=ax, color_dict=color_dict, convert=True)
    ax.set_title(f"Simulación de limpieza\n"
                 f"Pasos: {model.t}, Azulejos faltantes: "
                 f"{len(model.agents.select(model.agents.condition == 0))}")

fig, ax = plt.subplots()
model = Limpieza(parameters)
animation = ap.animate(model, fig, ax, animation_plot)
IPython.display.HTML(animation.to_jshtml(fps=15))

"""### Hacemos el experimento de tiempo con parametros definidos
Estos parametros son el tamaño de la cuadricula con el size y la densidad de arboles
Este experimento nos dirá el tiempo que tarda en limpiar toda la cuadricula.
"""

#  Definimos nuevamente los parametros para experimentar con el tiempo
parameters = {
    'azulejos sucios': ap.Range(0.2, 0.7),
    'size': 100
}
sample = ap.Sample(parameters, n=30)
# Iniciamos simulación
exp = ap.Experiment(Limpieza, sample, iterations=20)
results = exp.run()

"""### Graficamos la velocidad con la que se limpian todos los cuadros de la cuadricula"""

sns.set_theme()
sns.lineplot(
    data=results.arrange_reporters(),
    y='porcentaje de azulejos limpios',
    x='azulejos sucios'
);