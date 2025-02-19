# VERSION CASO BASE 2

import simpy
import random


def nodo(ambiente, arreglo, nodoid):
    print(f"Nodo {nodoid}: {arreglo}")
    # CASO BASE
    if len(arreglo) == 2:
        if arreglo[0] <= arreglo[1]:
            return arreglo
        else:
            return arreglo[::-1]
    # EN OTRO CASO, MEZCLAR
    else:
        mitad = len(arreglo) // 2
        mitad_izq = arreglo[:mitad]
        print(mitad_izq)
        mitad_der = arreglo[mitad:]
        print(mitad_der)
        hijo_izq = ambiente.process(nodo(ambiente, mitad_izq, nodoid * 2 + 1))
        hijo_der = ambiente.process(nodo(ambiente, mitad_der, nodoid * 2 + 2))
        mitad_ordenada_izq, mitad_ordenada_der = (yield hijo_izq & hijo_der).values()
        print(f"valores recibidos {nodoid}: {mitad_ordenada_izq}, {mitad_ordenada_der}")

        # COMPARAR CUAL MITAD VA PRIMERO
        resultado = mitad_ordenada_izq + mitad_ordenada_der
        print(resultado)
        return resultado


arreglo_sin_ordernar = [random.randint(0, 1000) for p in range(0, 16)]
print(arreglo_sin_ordernar)

ambiente = simpy.Environment()

ambiente.process(nodo(ambiente, arreglo_sin_ordernar, 0))
ambiente.run()
