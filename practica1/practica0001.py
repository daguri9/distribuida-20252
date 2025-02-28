import simpy
import random


class Nodo:
    def __init__(self, env, nodo_id: int, padre: Nodo):
        self.env = env
        self.nodo_id = nodo_id
        self.padre = padre
        self.hijo_izq = None
        self.mitad_recibida_izq = None
        self.hijo_der = None
        self.mitad_recibida_der = None
        self.lista = []
        env.process(self.ejecutar())

    def recibir_mitad(self, mitad_recibida: list, id_remitente: int):
        if id_remitente == self.hijo_izq.nodo_id:
            mitad_recibida_izq = mitad_recibida
        elif id_remitente == self.hijo_der.nodo_id:
            mitad_recibida_der = mitad_recibida

    def mezclar(self, mitad_ordenada_izq: list, mitad_ordenada_der: list):
        """
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
        """
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
        """
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
        """
        if len(lista) == 1:
            print(
                f"BACK: Enviando {lista} a el padre de {self.nodo_id} ({self.padre.nodo_id})"
            )
            self.padre.mezclar(lista)
        elif len(lista) == 2:
            if lista[0] <= lista[1]:
                print(
                    f"BACK: Enviando {lista} a el padre de {self.nodo_id} ({self.padre.nodo_id})"
                )
                self.padre.mezclar(lista)
            else:
                print(
                    f"BACK: Enviando {lista[::-1]} a el padre de {self.nodo_id} ({self.padre.nodo_id})"
                )
                self.padre.mezclar(lista[::-1])
        else:
            mitad = len(lista) // 2
            self.mitad_izq = lista[:mitad]
            self.mitad_der = lista[mitad:]

            if self.hijo_izq is None:
                self.hijo_izq = Nodo(self.env, self.nodo_id * 2 + 1, self)

            if self.hijo_der is None:
                self.hijo_der = Nodo(self.env, self.nodo_id * 2 + 2, self)

            self.hijo_izq.ordenar(self.mitad_izq)
            print(f"GO: Enviando {self.mitad_izq} a {self.hijo_izq.nodo_id}")
            self.hijo_der.ordenar(self.mitad_der)
            print(f"GO: Enviando {self.mitad_der} a {self.hijo_der.nodo_id}")

        yield self.env.timeout(1)

    def ejecutar(self):
        while True:
            if self.padre is None and self.lista == []:
                self.lista = [random.randint(0, 1000) for p in range(0, 16)]
                print(f"{self.nodo_id} ha generado {self.lista}")
                self.ordenar(self.lista)


if __name__ == "__main__":
    env = simpy.Environment()
    raiz = Nodo(env, 0, None)
    env.process(raiz.ejecutar())
    env.run()
