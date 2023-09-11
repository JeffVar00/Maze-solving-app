- Disclaimer: Pymaze was prohibited to use

### Maze Generation Rules

    0 – Espacios por los cuales puede moverse el agente
    1 – Paredes o obstáculos donde no se permite al agente caminar por ahí
    2 – El punto de inicio
    3 – El punto final o meta
    4 – El recorrido que hace cada camino, si lo quieren mostrar
    5 – La ruta mínima obtenida por el algoritmo

### Algorithms

    • Dijkstra
    • Bellman – Ford
    • Depth First Search (DFS)
    • Breadth-First Search (BFS)
    • A* Search

### Questions for memory and time estimates

    Basado en los resultados obtenidos a partir del laberinto 200x200 podemos obtener los siguientes resultados:

    • ¿Qué algoritmo es más veloz en obtener la mejor ruta?
    • ¿Qué algoritmo consume más memoria?

    Podemos concluir que el algoritmo que consumio menos memoria fue el bellman Ford pero fue el que mas duro en encontrar una ruta
        Algoritmo: Bellman Ford
            Tiempo: 2.887443 segundos
            Memoria usada: 27.73 KB

    A diferencia del depth first search que fue el que mas memoria uso
        Algoritmo: Depth First Search (DFS)
            Tiempo: 1.941080 segundos
            Memoria usada: 887.73 KB

    Y el Breadth First Search (BFS) fue el que menos tiempo tardo en encontrar una ruta
        Algoritmo: Breadth First Search (BFS)
            Tiempo: 0.591832 segundos
            Memoria usada: 142.35 KB

    Tambien notar que la solucion otorgada por el Breadth First Search fue diferente a las demas y que el algoritmo DFS fue el menos eficiente al encontrar una ruta.


### Maze sizes:

laberinto1 5x5
laberinto2 50x50
laberinto3 200x200

### How to use

Just type in the terminal Python3 .\main.py

### How to change the maze

Select the desired maze in the data folder, it wil solve the maze and show it on screen the solved solution and save it into the results folder in data (can access via Results button)

### How to clean the maze

To clean the maze just press the Clean Laberinth button

### How to change the algorithm

Select your desired algorithm from the list at the top :)

### How to create a maze

Select the Generate new Maze button and it will create a new maze with the desired size, you can change the size in the window to create a new maze, please note that the size cant be empty and each difficulty represents how many walls will be in the maze, the higher the difficulty the more walls will be in the maze

The maze generation button is used for make it easier to create a maze but its not included in what is asked in the project, so it cant be perfect and sometimes generate a unsolvable Maze