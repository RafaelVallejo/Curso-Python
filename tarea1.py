#!/usr/bin/python
# -*- coding: utf-8 -*-
#UNAM-CERT

###  Tarea 1
primos = []
def valida_palindromo(cadena):
	"""Funcion que valida si una cadena sin espacios es un palinddromo y devuelve True o False.
	A partir del tamaÃ±o de la cadena se va comparando los caracteres de la primera y la ultima posicion, respectivamente  """
	tam = 0
	while tam < len(cadena):
		if cadena[tam] != cadena[-(tam+1)]:
			return False
		tam+=1
	return True

def palindromo_mas_grande(cadena):
	"""Funcion que recibe cadenas separadas por un espacio y devuelve la cadena palindromo mas grande.
	Se separan las cadenas y se valida que sea un palindromo para comparar sus tamaÃ±os y obtener la mas grande
	"""
	cadenas = cadena.split()
	mas_grande = ''
	for cad in cadenas:
		if valida_palindromo(cad):
			if len(cad) > len(mas_grande):
				mas_grande = cad
	return mas_grande

def es_primo(numero):
	"""Funcion que valida si un numero ingresado (parametro) es primo o no y devuelve True o False.
	Se va obteniendo el modulo del numero ingresado desde el 2 (es el primer numero primo) hasta numero-1, si en algun caso es 0, el
	numero no es primo"""
	for i in range(2,numero):
		if numero%i == 0:
			return False
	return True

def n_primos(n,valor=2):
	"""Funcion que obtiene los n numeros primos que se indiquen como parametro y los devuelve en una lista (primos).
	El segundo parametro indica el valor del primer numero primo para poder obtener los demas valores y se colcoa por defecto = 2.
	La lista se obtiene de forma recursiva y haciendo uso de la funcion que valida si un valor es primo o no.
	El caso base es cuando n=1 y se inserta el primer numero primo ademas de ordenar la lista (menor a mayor) y devolverla
	"""
	if n == 1:
		primos.append(2)
		primos.sort()
		return primos
	else:
		if  es_primo(valor):
			primos.append(valor)
		else:
			return n_primos(n,valor+1)
		return n_primos(n-1,valor+1)

##Valida palindromo
if valida_palindromo("luzazul"):
	print "Es palindromo: True"
else:
	print "Es palindromo: False"
### Imprime palindromo mas grande
print "El palindromo mas grande es: " + palindromo_mas_grande("larutanatural anitalavalatina bob luzazul")

### Indica si un numero es primo
if es_primo(149):
	print "Es primo: True"
else:
	print "Es primo: False"
### Imprime la lista de los n numeros primos que se indiquen
print n_primos(15)
