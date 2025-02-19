# VERSION CASO BASE 2

import simpy
import random


def mezclar(mitad_ordenada_izq, mitad_ordenada_der):
    resultado = []
    i, j = 0, 0

    while i < len(mitad_ordenada_izq) and j < len(mitad_ordenada_der):
        if mitad_ordenada_izq[i] < mitad_ordenada_der[j]:
            resultado.append(mitad_ordenada_izq[i])
            i += 1
        else:
            resultado.append(mitad_ordenada_der[j])
            j += 1

    while i < len(mitad_ordenada_izq):
        resultado.append(mitad_ordenada_izq[i])
        i += 1

    while j < len(mitad_ordenada_der):
        resultado.append(mitad_ordenada_der[j])
        j += 1

    return resultado


def nodo(ambiente, arreglo, nodoid):
    print(f"Nodo {nodoid} GOT IN: {arreglo}")
    if len(arreglo) == 2:
        if arreglo[0] <= arreglo[1]:
            return arreglo
        else:
            return arreglo[::-1]
    else:
        mitad = len(arreglo) // 2
        mitad_izq = arreglo[:mitad]
        print(mitad_izq)
        mitad_der = arreglo[mitad:]
        print(mitad_der)
        hijo_izq = ambiente.process(nodo(ambiente, mitad_izq, nodoid * 2 + 1))
        hijo_der = ambiente.process(nodo(ambiente, mitad_der, nodoid * 2 + 2))
        mitad_ordenada_izq, mitad_ordenada_der = (yield hijo_izq & hijo_der).values()
        yield ambiente.timeout(1)
        print(f"Nodo {nodoid} GOT BACK: {mitad_ordenada_izq}, {mitad_ordenada_der}")
        resultado = mezclar(mitad_ordenada_izq, mitad_ordenada_der)
        print(resultado)
        return resultado


arreglo_sin_ordernar = [random.randint(0, 1000) for p in range(0, 16)]
print(arreglo_sin_ordernar)

ambiente = simpy.Environment()

ambiente.process(nodo(ambiente, arreglo_sin_ordernar, 0))
ambiente.run(until=1)
