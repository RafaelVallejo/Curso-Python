#!/usr/bin/python
# -*- coding: utf-8 -*-
#UNAM-CERT
# Vallejo Fernández Rafael Alejandro
# El script recibe como argumentos: archivo_palabras y archivo_salida
import sys
from itertools import permutations
from random import choice, randint

numeros = '0123456789'
simbolos = '@!$#&/()=_-*[].'
dicc_simbolos = {'a':'@','c':'(','s':'$','i':'&','l':'/'}
dicc_numeros = {'o':'0','l':'1','z':'2','e':'3','a':'4','s':'5','g':'6','t':'7','b':'8','q':'9'}

lista_palabras = []
nueva = []
nueva_simbolos = []
nueva_numeros = []
lista_completa = []
lista_posibles_contrasenias = []  # lista que contendrás las contraseñas generadas
def printError(msg, exit = False):
    """Función que imprime mensaje de error y sale del programa
    Recibe: mensaje a mostrar y booleano que indica si se debe terminar la ejecución del programa"""
    sys.stderr.write('Error:\t%s\n' % msg)
    if exit:
        sys.exit(1)

def lee_palabras(archivo):
    """Función que lee el archivo que contiene las palabras para generar las contraseñas. Cada palabra está en una línea.
    Recibe archivo y devuelve lista con las palabras leídas"""
    with open(archivo,'r') as palabras:
        for palabra in palabras:
            lista_palabras.append(palabra[:-1])
    return lista_palabras

def separa_por_caracteres(lista):
    """Función que separa cada palabra de la lista en sublistas de caracteres para poder realizar las permutaciones y manipularlas
    más fácilmente. Recibe lista con las palabras leídas y devuelve la nueva lista con sublistas de las palabras seaparadas por
    caracteres"""
    lista_resultado = [ [ letras for letras in palabra ] for palabra in lista ]
    return lista_resultado

def cambia_letra_por_simbolo(lista):
    """Función que cambia las letras (keys) de la palabra por algún símbolo (values), serán modificadas en la lista que recibe como parámetro """
    for palabra in lista:
        i = 0
        while i < len(palabra):
            if palabra[i] in dicc_simbolos.keys():
                pal = palabra[i]
                palabra[i] = dicc_simbolos[palabra[i]]
            i += 1

def cambia_letra_por_numero(lista):
    """Función que cambia las letras (keys) de la palabra por algún número (values), serán modificadas en la lista que recibe como parámetro """
    for palabra in lista:
        i = 0
        while i < len(palabra):
            if palabra[i] in dicc_numeros.keys():
                pal = palabra[i]
                palabra[i] = dicc_numeros[palabra[i]]
            i += 1

def mayus_letra_por_palabra(lista):
    """Función que cambia a mayúscula o minúscula una letra de la palabra, recorre las palabras de la lista y va haciendo el cambio
    De letra a letra de la palabra para regresar una lista con las palabras originales con n veces una letra mayúscula/minúscula
    Devuelve lista con las nuevas palabras donde cada una tiene una letra mayúscula"""
    alterada = []
    for palabra in lista:
        cadena = ''
        i = 0
        while i < len(palabra):
            palabra[i] = palabra[i].swapcase()
            alterada.append(cadena.join(palabra))
            palabra[i] = palabra[i].swapcase()
            i += 1
    return alterada
def permuta_palabras(lista):
    """Función que realiza las permutaciones de las palabras contenidas en la lista, las permutaciones se realizan con la función permutations() del módulo
    itertools. Cuando la palabra es mayor a 7 caracteres se particionan las permutaciones porque solamente llega a 7!.
    Se agregan a las conraseñas generadas desde las palabras originales con una simple modificación (una letra mayúscula en cada posición, cambiar letras por números),
    las contraseñas generadas de forma aleatoria de acuerdo a la función mezclar_todas_palabras y después se agregan las contraseñas generadas por las permutaciones.
    Recibe: la lista que contiene las sublistas de las palabras a permutar
    Devuevle: una lista con las contraseñas que se generaron"""
    cad = ''
    final,mezclas, resultado = [], [], []
    for palabra in lista:
        if len(palabra) <= 7:
            mezclas += permutations(palabra)
        if len(palabra) > 7 and len(palabra) < 15:
            mezclas+= permutations(palabra[:7])
            mezclas+= permutations(palabra[7:])
    for pal in mezclas:
        final += [ (list(pal)) ]
    temporal = []  # lista para verificar que las palabras originales no se repitan en la lista final sin permutaciones
    for original in lista:
        if original not in temporal:  # si la palabra que se va a agregar no se encuentra en la lista original, se escribe en el archivo
            temporal += [original]
            resultado.append(cad.join(original))
    for cadaUna in final:
        numero = randint(0,5)
        for i in range(0,numero):
            numOsimboloOmayus = randint(0,2)  # variable para decidir aleatoriamente si se agrega un simbolo, mayúscula/minúscula o número en las contraseñas de las permutaciones
            aleat = randint(0,len(cadaUna)-1)
            if numOsimboloOmayus == 0:
                cadaUna.insert(aleat, choice(simbolos))  # se elige algún caracter de la cadena símbolos y se inserta en una posición aleatoria
            elif numOsimboloOmayus == 1:
                cadaUna.insert(aleat, choice(numeros))  # se elige algún caracter de la números símbolos y se inserta en una posición aleatoria
            else:
                cadaUna[aleat] = cadaUna[aleat].swapcase()  # se elige algún caracter y se cambia a minúscula o mayúscula con swapcase()
        resultado.append(cad.join(cadaUna))
    return (list(set(resultado)))  # Devuelve las contraseañas en una lista donde antes se obtiene el conjunto (set) para tener únicamente las contraseñas únicas

def escribe_contrasenias(lista, archivo_salida):
    """Función que escribe las contraseñas generadas en el archivo de salida.
    Recibe: lista con las contraseñas únicas y el archivo donde se escribirán las conraseñas. """
    cad = ''
    with open(archivo_salida,'w') as passwords:
        for cadaPassword in lista:
            passwords.write(cad.join(cadaPassword)+'\n')

def mezclar_todas_palabras(lista):
    """Función para realizar la combinación aleatoria de las palabras contenidas en lista. Se establece límite de < 100 para lal nueva lista
    generada. Es una forma manual de realizar la mezcla de las palabras que después serán permutadas.
    Recibe lista con las palabras y devuelve la lista con sublistas de las palabras mezcladas"""
    cadenas = []
    otra = []
    while len(otra) < 100:
        for palabra in lista:
            for palabra in lista:
                posInicial = randint(0,len(palabra)-1)
                posFinal = randint(0,len(palabra)-1)
                agrega = palabra[posInicial:posFinal+1]
                if agrega not in cadenas and len(agrega) >= 2:
                    cadenas += agrega
            if cadenas != []:
                otra += [cadenas]
            cadenas = []
    return otra

def crea_listas():
    """Función para crear las listas de palabras que se utilizarán para generar las contraseñas. Se separan por caracteres para poder manipularlas más fácilmente
    Se crea una lista original, una lista de las palabrqas sustiutidas por símbolos, otra por números y devuelve la lista resultante de la concatenación de las
    tres listas"""
    nueva = separa_por_caracteres(lista_palabras)
    nueva_simbolos = separa_por_caracteres(lista_palabras)
    nueva_numeros = separa_por_caracteres(lista_palabras)
    cambia_letra_por_simbolo(nueva_simbolos)
    cambia_letra_por_numero(nueva_numeros)
    return nueva + nueva_numeros + nueva_simbolos


if len(sys.argv) != 3:  # Se verifica que se reciban 3 argumentos, <script> <archivo_palabras> <archivo_salida>
    printError('Indicar archivo a leer y archivo de salida.', True)
lee_palabras(sys.argv[1])
print 'Las palabras leídas de \'%s\' son:\n%s' % (sys.argv[1], lista_palabras)
lista_completa = crea_listas()
lista_completa = lista_completa + mezclar_todas_palabras(lista_completa)
lista_a_permutar = mayus_letra_por_palabra(lista_completa)
lista_final = separa_por_caracteres(lista_a_permutar)
lista_posibles_contrasenias = permuta_palabras(lista_final)  # lista que contiene las contraseñas únicas generadas
escribe_contrasenias(lista_posibles_contrasenias, sys.argv[2])
print 'Se generaron %s contraseñas y se escribieron en \'%s\'' % (len(lista_posibles_contrasenias), sys.argv[2])
