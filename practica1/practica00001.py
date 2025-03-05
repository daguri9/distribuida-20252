import simpy
import random


def ordenar(ambiente: simpy.core.Environment, lista: list, id: int):
    """
    Este método abstrae un proceso/nodo en un sistema distribuido
    síncrono diseñado para resolver MergeSort sobre una lista arbitraria.

    Se asume y garantiza que este sistema distribuido siempre
    mantiene una topología de arbol binario.

    Un nodo recibe una lista de elementos, si tiene mas de dos
    elementos, se parte por la mitad y cada una es mandada a ordenar
    a los dos procesos hijos del nodo por un mensaje GO.

    Si la lista tiene uno o dos elementos, se ordena trivialmente
    y se manda de regreso al proceso padre por medio de un mensaje
    BACK.

    Parameters
    ----------
    ambiente:
        Un ambiente de ejecución de procesos simulados de SimPy.

    lista: list
        Lista para ordenar.

    id: int
        Lista ordenada entregada por el nodo hijo derecho.

    Returns
    -------
    list:
        Lista ordenada al mezclar las anteriores.
    """
    print(f"[Ronda {ambiente.now}] Nuevo nodo, ID: {id}")

    # Se verifica si la lista recibida es trivial de ordenar.
    # De ser el caso, se ordena, se regresa y el proceso concluye.
    if len(lista) == 2:
        return lista if lista[0] < lista[1] else lista[::-1]
    elif len(lista) == 1:
        return lista

    # Si la lista no es trivial, se parte en dos y se invocan
    # a dos procesos para resolverlas.
    mitad = len(lista) // 2
    yield ambiente.timeout(1)

    id_hijo_izq = id * 2
    print(f"[Ronda {ambiente.now}] GO: {id}->{id_hijo_izq} (hijo izquierdo)")
    hi = ambiente.process(ordenar(ambiente, lista[mitad:], id_hijo_izq))

    id_hijo_der = id * 2 + 1
    print(f"[Ronda {ambiente.now}] GO: {id}->{id_hijo_der} (hijo derecho)")
    hd = ambiente.process(ordenar(ambiente, lista[:mitad], id_hijo_der))

    # Se espera por los resultados de los procesos hijos.
    lista_izq, lista_der = (yield hi & hd).values()

    # Una vez recibidas las listas ordenadas de los procesos hijos,
    # podemos fusionarlas en una sola iterando sobre de ellas a la vez
    # y poniendo los elementos mayores o menores segun corresponda.
    lista_ordenada = []
    i, j = 0, 0

    while i < len(lista_izq) and j < len(lista_der):
        if lista_izq[i] <= lista_der[j]:
            lista_ordenada.append(lista_izq[i])
            i += 1
        else:
            lista_ordenada.append(lista_der[j])
            j += 1

    lista_ordenada.extend(lista_izq[i:])
    lista_ordenada.extend(lista_der[j:])

    yield ambiente.timeout(1)

    # Finalmente, podemos devolver la lista ordenada final.
    print(f"[Ronda {ambiente.now}] BACK: Desde {id}")
    return lista_ordenada


def main():
    """
    Un método simple para inicializar la simulación.
    Se genera una lista aleatoria y se invoca un proceso raíz para
    completar la tarea de ordenarlo.
    """
    lista = [random.randint(0, 1000) for _ in range(0, 16)]
    print(f"Lista desordenada: {lista}")
    ambiente = simpy.Environment()
    lista_ordenada = ambiente.process(ordenar(ambiente, lista, 1))
    ambiente.run()
    print(f"Lista ordenada: {lista_ordenada.value}")
    print(f"Completado en {ambiente.now} rondas.")


if __name__ == "__main__":
    main()
