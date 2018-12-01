#!/usr/bin/python
# -*- coding: utf-8 -*-
#UNAM-CERT
#  Vallejo Fernández Rafael Alejandro

from re import match
import sys
# 1. Expresión reg que coincida con dir IPv4
def dirIP(archivo):
    """ Función que valida si las direcciones IPv4 leídas del archivo son válidas
    Recibe: archivo y devuelve: Direcciones IPv4 válidas en la salida estándar"""
    # patron = r'[0-2]?[0-9]{1,2}\.[0-2]?[0-9]{1,2}\.[0-2]?[0-9]{1,2}\.[0-2]?[0-9]{1,2}'  # Expresión regular que valida formato de direcciones 0-999.0-999.0-999.0-999
    patron = r'^[^0](((1?[0-9]{,2})|(2[0-5]{1,2}))\.){3}((1?[0-9]{1,2})|(2[0-5][0-4]))$'  # Expresión regular que valida direcciones IPv4 dentro del rango permitido y con el formato correcto:
                                                                                        # 1-199.0-199.0-199.0-199 ó 200-255.200-255.200-255.200-254
    with open(archivo, 'r') as archivo_direcciones:
        for direccion in archivo_direcciones:
            if match(patron,direccion[:-1]):
                print direccion

# 2. Expresión reg que coincida con una dirección de correo electrónico
def correo(archivo):
    """ Función que valida si las direcciones de correo leídas del archivo son válidas
    Recibe: archivo y devuelve: Direcciones de correo válidas en la salida estándar"""
    patron = r'^[^.0-9_][a-zA-z._0-9]+[^_.]@[a-zA-Z]+\.[a-zA-Z]+(\.[a-zA-Z]+)*[^.]$'  # Expresión regular que valida formato de correos: inician con letras
                            #  y despues pueden tener números, puntos, guiones bajos @ palabra/letra punto palabra/letra
    with open(archivo, 'r') as archivo_correos:
        for correo in archivo_correos:
            if match(patron,correo[:-1]):
                print correo

print 'direcciones IPv4 válidas:'
dirIP(sys.argv[1])  # el argumento uno es el archivo de donde se leerán las direcciones IP a validar
print 'direcciones de correo válidas:'
correo(sys.argv[2])  # el argumento dos es el archivo de donde se leerán las direcciones de correo a validar
