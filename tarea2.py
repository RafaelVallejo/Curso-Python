#!/usr/bin/python
# -*- coding: utf-8 -*-
#UNAM-CERT
#
### Tarea 2
from random import randrange  # modulo para generar numeros pseudoaleatorios

letras_M = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
letras_m = 'abcdefghijklmnopqrstuvwxyz'
numeros = '123456789'
simbolos = '@!#$%&/\()=?[]{}*+-.,;:_'

def genera_password(n=12,password=''):
	""" Funcion que genera contrasenias de forma recursiva, devuelve un string. El parametro n indica la longitud de la contrasenia y por
	 defecto sera de 12 caracteres mientras que el segundo parametro es la contrasenia que se generara y por ello esta vacia por defecto.
	De acuerdo a las cadenas definidas de letras, numeros y simbolos, se obtiene de forma aleatoria que caracter sera elegido de estos y
	dentro de cada una se vuelve a obtener algun caracter aleatorio que sera concatenado a la contrasenia que se genera. Para obtenerlas
	de forma aleatorias se uso randrange
	"""
	if n==0:
		return password
	else:
		aleatorio = randrange(4)

		if aleatorio == 0:
			caracter = letras_M[randrange(len(letras_M))]
		elif aleatorio == 1:
			caracter = letras_m[randrange(len(letras_m))]
		elif aleatorio == 2:
			caracter = numeros[randrange(len(numeros))]
		else:
			caracter = simbolos[randrange(len(numeros))]

		password += caracter
		return genera_password(n-1,password)

# Se imprime la contrasenia generada con genera_password con el tamanio por defecto, si se pone el valor de n sera el tamanio que se generara
print 'El password generado es: ' + genera_password()
