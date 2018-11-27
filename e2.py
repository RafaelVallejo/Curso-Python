#!/usr/bin/python
# -*- coding: utf-8 -*-
#UNAM-CERT
#
### Funcion que valide si es un palindromo recibe cadena y devuelve true o false

def valida_palindromo(cadena):
	tam = 0
	while tam < len(cadena):
		if cadena[tam] != cadena[-(tam+1)]:
			return False
		tam+=1
	return True

if valida_palindromo("anitalavalatina"):
	print "Es palindromo: True"
else:
	print "Es palindromo: False"
