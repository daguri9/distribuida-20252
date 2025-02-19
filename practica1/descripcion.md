# Computación Distribuida 2025-2 Práctica 1: Árboles

Profesor: Mauricio Riva Palacio Orozco
Ayudante: Adrián Felipe Fernández Romero
Laboratorio: Daniel Michel Tavera
Fecha de entrega: miércoles 5 de marzo de 2025

## Descripción de la Práctica
El equipo deberá implementar una versión distribuida del algoritmo Merge Sort, como sigue:
- El proceso raíz deberá generar un arreglo de 16 números de forma aleatoria e imprimirlo en la consola.
- Si un proceso tiene que ordenar más de 2 números, deberá dividir su arreglo de números en dos subarreglos de la mitad de tamaño y enviar cada mitad a uno de sus procesos hijos.
- Si un proceso solo tiene 2 números por ordenar, deberá colocar el más pequeño primero y el más grande después y enviarlos de regreso a su padre. 
- Si lo prefieren, pueden subdividir el arreglo de 2 números en dos arreglos de un solo elemento (trivialmente ordenados) y usar el proceso de mezcla para unirlos.
- Cuando un proceso recibe los subarreglos ordenados de ambos hijos, deberá mezclarlos para obtener su arreglo ordenado y, si no es la raíz, enviar el arreglo ordenado a su padre.
- Al final, la raíz tendrá el arreglo completo ordenado y deberá imprimirlo en la consola. Los procesos también deberán imprimir en la consola cada vez que envíen o reciban un mensaje, indicando el identificador del proceso, la ronda que se está procesando (‘tiempo’ de la simulación) y el tipo de mensaje (GO o BACK). No es necesario que impriman los subarreglos cada vez, basta con que la raíz imprima el arreglo completo antes y después de ordenarlo.
- Recuerden agregar comentarios que expliquen el funcionamiento del código.

## Requisitos de entrega
Guardar el código fuente del programa en un archivo con el nombre “Practica1”, seguido
de los nombres de los integrantes del equipo; por ejemplo:

```
Practica1_MauricioRivaPalacio_AdrianFernandez_DanielMichel.py
```

Realizar también un reporte en pdf con el mismo nombre, en el cual se indique lo
siguiente:
- Los nombres de todos los integrantes del equipo.
- Una descripción de cómo se desarrolló la práctica y cómo funciona la solución implementada.
- La forma de operar el programa, incluyendo si se esperan entradas del usuario (y cuáles), así como qué salida(s) arroja.
- Cualquier otro comentario o aclaración que consideren pertinente.
Subir los archivos al Classroom antes de las 23:59 horas de la fecha de entrega cumpliendo los siguientes lineamientos:
- Solamente un miembro del equipo debe enviar los archivos.
- Los demás integrantes deben marcar la práctica como entregada y agregar un comentario en el que indiquen quiénes son los integrantes de su equipo y quién entregó el código.
