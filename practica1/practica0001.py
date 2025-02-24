import simpy
import random


class Nodo:
    def __init__(
        self,
        env,
        nodo_id: int,
        padre: Nodo,
        vecino_izq: Nodo,
        vecino_der: Nodo
    ):
        self.env = env
        self.nodo_id = nodo_id
        self.padre = padre
        self.vecino_izq = vecino_izq
        self.vecino_der = vecino_der
        self.inbox = simpy.Store(env)
        env.process(self.ejecutar())

    def mezclar(
        self,
        mitad_ordenada_izq: list,
        mitad_ordenada_der: list
    ) -> list:
        '''
        Recibe dos listas previamente ordenadas y se mezclan en una sola.
        Parameters
        ----------
        mitad_ordenada_izq: list
            Lista ordenada entregada por el nodo hijo izquierdo.

        mitad_ordenada_der: list
            Lista ordenada entregada por el nodo hijo derecho.
        Returns
        -------
        list:
            Lista ordenada al mezclar las anteriores.
        '''
        lista_mezclada = []
        i, j = 0, 0
        while i < len(mitad_ordenada_izq) and j < len(mitad_ordenada_der):
            if mitad_ordenada_izq[i] < mitad_ordenada_der[j]:
                lista_mezclada.append(mitad_ordenada_izq[i])
                i += 1
            else:
                lista_mezclada.append(mitad_ordenada_der[j])
                j += 1
        while i < len(mitad_ordenada_izq):
            lista_mezclada.append(mitad_ordenada_izq[i])
            i += 1
        while j < len(mitad_ordenada_der):
            lista_mezclada.append(mitad_ordenada_der[j])
            j += 1
        return lista_mezclada

    def ordenar(self, lista: list) -> list:
        '''
        Intenta ordenar una lista trivialmente: Si tiene dos elementos,
        se mueve el mayor al inicio y se regresa. Si tiene un solo
        elemento, se regresa tal cual.

        En cualquier otro caso, se parte a la mitad y se llama a otro proceso
        a intentar ordenar la lista trivialmente.
        ----------
        lista: list
            Lista a ordenar trivialmente.

        Returns
        -------
        list:
            Lista ordenada.
        '''
        if len(lista) == 1:
            return lista
        elif len(lista) == 2:
            if lista[0] <= lista[1]:
                return lista
            else:
                return lista[::-1]
        else:
            mitad = len(lista) // 2
            mitad_izq = lista[:mitad]
            mitad_der = lista[mitad:]

    def send(self, message):
        mitad_ordenada_izq.inbox.put((self.nodo_id, message))
        mitad_ordenada_der.inbox.put((self.nodo_id, message))

    def ejecutar(self):
        while True:
            sender, message = yield self.inbox.get()
            if not self.seen_message:
                self.seen_message = True
                print(f"Time {self.env.now}: Process {self.nodo_id} received message from {sender}")
                self.send(message)


# Simulation setup
def inicializar_simulacion(num_nodos, raiz):
    env = simpy.Environment()
    nodos = {}

    # Create processes
    for i in range(num_processes):
        processes[i] = Process(env, i, [])

    # Establish neighbors
    for a, b in edges:
        processes[a].neighbors.append(processes[b])
        processes[b].neighbors.append(processes[a])

    # Start broadcast from source
    env.process(initial_broadcast(env, processes[source]))
    env.run()


# Initial broadcast trigger
def initial_broadcast(env, source_process):
    yield env.timeout(0)
    source_process.seen_message = True
    print(f"Time {env.now}: Process {source_process.nodo_id} initiates broadcast")
    source_process.send("Message")


if __name__ == "__main__":
    arreglo_sin_ordernar = [random.randint(0, 1000) for p in range(0, 16)]
    inicializar_simulacion(len(arreglo_sin_ordernar), 0)