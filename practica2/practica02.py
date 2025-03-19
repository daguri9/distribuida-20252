import simpy


class Proceso:
    def __init__(self, env, pid, vecinos):
        self.env = env
        self.pid = pid
        self.vecinos = vecinos
        self.hijos = []
        self.padre = None
        self.nivel = 0

    def go(self, distancia: int, remitente):
        if self.padre is None:
            self.padre = remitente
            self.hijos = []
            self.nivel = distancia + 1
            self.msg_esperados = len(self.vecinos) - 1
            if self.msg_esperados == 0:
                self.padre.back(True, distancia + 1, self)
            else:
                for vecino, peso in self.vecinos:
                    yield self.env.timeout(peso)
                    if vecino is not remitente:
                        vecino.go(distancia + 1, self)
        elif self.nivel > distancia + 1:
            self.padre = remitente
            self.hijos = []
            self.nivel = distancia + 1
            self.msg_esperados = len(self.vecinos) - 1
            if self.msg_esperados == 0:
                self.padre.back(True, self.nivel, self)
            else:
                for vecino, peso in self.vecinos:
                    yield self.env.timeout(peso)
                    if vecino is not remitente:
                        vecino.go(distancia + 1, self)
        else:
            remitente.back(False, distancia + 1, self)

    def back(self, resp: bool, distancia: int, remitente):
        if distancia == self.nivel + 1 and resp:
            self.hijos.append(remitente)
            self.msg_esperados -= 1
            if self.msg_esperados == 0 and self.padre is not self:
                yield self.env.timeout()
                if self.padre != None:
                    self.padre.back(True, distancia, self)
            else:
                self.bfs_completado = True

    def start(self):
        self.go(-1, self)


def construir_ejemplar(num_procesos, vertices, inicio):
    env = simpy.Environment()
    procesos = {}

    # Create processes
    for i in range(num_procesos):
        procesos[i] = Proceso(env, i, [])

    # Establish neighbors
    for a, b, c in vertices:
        procesos[a].vecinos.append((procesos[b], c))
        procesos[b].vecinos.append((procesos[a], c))

    # Start broadcast from source
    env.process(initial_bfs(env, procesos[inicio]))
    env.run()


# Initial broadcast trigger
def initial_bfs(env, inicio):
    yield env.timeout(0)


# Example usage
# Nomenclatura: (vertice, vertice, peso)
vertices = [(0, 1, 2), (0, 2, 1), (1, 2, 3), (2, 4, 1), (2, 3, 3), (3, 4, 1), (3, 5, 1)]
construir_ejemplar(6, vertices, source=0)
