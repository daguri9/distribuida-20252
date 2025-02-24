import simpy
import random


class Nodo:
    def mezclar(self, mitad_ordenada_izq: list, mitad_ordenada_der: list):
        pass

    def ordenar(self, arreglo: list):
        pass

    def __init__(self, padre: Nodo):
        self.padre = padre


arreglo_sin_ordernar = [random.randint(0, 1000) for p in range(0, 16)]
print(arreglo_sin_ordernar)

ambiente = simpy.Environment()

ambiente.process(nodo(ambiente, arreglo_sin_ordernar, 0))
ambiente.run(until=1)
