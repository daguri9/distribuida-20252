import simpy
import random

#definimos el proceso hijo: un contador que regresa un dato aleatorio
def ordenar(ambiente, lista, id):
    print(f"ID: {id}, ronda: {ambiente.now}")
    if len(lista) == 2:
        return lista if lista[0] < lista[1] else lista[::-1]
    
    mitad = len(lista) // 2
    yield ambiente.timeout(1)
    print("GO: hijo izquierda")
    hi = ambiente.process(ordenar(ambiente, lista[mitad:], id*2 + 1))
    print("GO: hijo derecho")
    hd = ambiente.process(ordenar(ambiente, lista[:mitad], id*2 + 2))
    lista_izq, lista_der = (yield hi & hd).values()
    
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
    print(f"BACK, ronda: {ambiente.now}")
    return lista_ordenada

    

def main():
    lista = [random.randint(0, 1000) for _ in range(0, 16)]
    ambiente = simpy.Environment()
    lista_ordenada = ambiente.process(ordenar(ambiente, lista, 1))
    ambiente.run()
    print(lista_ordenada.value)


if __name__ == "__main__":
    main()
