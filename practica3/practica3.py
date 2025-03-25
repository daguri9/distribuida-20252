import random
import simpy

def construye_grafica(n: int):
    # La grafica se representa como una matriz de adyacencias.
    # Inicialmente construye la grafica de forma que este conectada linealmente.
    grafica = [
        [1 if col == row - 1 or row == col - 1 else 0 for col in range(n)]
        for row in range(n)
    ]

    # Decide el resto de los vertices con probabilidad 0.5
    for i in range(n - 2):
        for j in range(i + 2, n):
            grafica[i][j] = random.randint(0, 1)
            grafica[j][i] = grafica[i][j]

    # Imprime la matriz de adyacencias.
    print("Grafica generada: ")
    print("\n".join(["  ".join([str(cell) for cell in row]) for row in grafica]))
    return grafica


def obten_diametro(grafica):
    env = simpy.Environment()
    n = len(grafica)
    vecinos = [[i for i in range(n) if row[i] != 0] for row in grafica]
    stores = [simpy.Store(env) for _ in range(n)]

    for i in range(n):
        env.process(proceso(env, i, vecinos[i], stores[i]))
    
    


def proceso(env, id, vecinos, store):
    # TODO
    pass

n = 8
grafica = construye_grafica(n)

