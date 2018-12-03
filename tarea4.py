#!/usr/bin/python
# -*- coding: utf-8 -*-
#UNAM-CERT
# Vallejo Fernández Rafael Alejandro

from datetime import datetime
from hashlib import md5,sha1
import sys
import xml.etree.ElementTree as ET
hosts = []
reporte = []
class Host:
    """Clase para crear cada objeto host y generar el archivo CSV. Sus atributos son ip, status, ssh, honeypot, nombre_dominio"""
    def __init__(self, ip, status, ssh, honeypot, nombre_dominio):
        """Método "constructor" para inicializar los atributos del objeto"""
        self.ip = ip
        self.status = status
        self.ssh = ssh
        self.honeypot = honeypot
        self.nombre_dominio = nombre_dominio

    def __str__(self):
        """Método para convertir el objeto en una cadena con el formato que indiquemos"""
        return '%s,%s,%s,%s,%s\n' % (self.ip, self.status, self.ssh, self.honeypot, self.nombre_dominio)

def lee_xml(archivo_xml):
    """Función para leer el archivo xml. Se buscará la información solicitada para realizar el reporte, es decir, puertos abiertos, direcciones ips,
    estado del host (prendido o apagado), servidores HTTP utilizados, nombres de dominio, honeypots. Recibe el archivo xml que se analizará"""
    with open(archivo_xml,'r') as nmap:
        prendidos, apagados = 0, 0  #  variables para obtener las cantidads solicitadas
        host_port_22_open, host_port_53_open, host_port_80_open, host_port_443_open = 0, 0, 0 , 0
        serv_apache, serv_dionaea, serv_nginx, serv_otros = 0, 0, 0, 0
        nombre_dominio = 0
        completo = ET.fromstring(nmap.read())
        for cada_host in completo.findall('host'):
            paso = True  # Variable booleana para no contar dos veces los servidores HTTP en un mismo host y con diferente puerto
            host_nombre_dominio, puerto_22_abierto, host_honeypot, host_status = 'no tiene', 'puerto 22 cerrado', 'no es honeypot', ''  # Variables para el archivo CSV que se utlizan en la clase Host
            ip = cada_host.find('address').get('addr')
            status = cada_host.find('status').get('state')
            if status == 'up':
                host_status = 'host prendido'  # Variable para el objeto Host
                prendidos += 1
            elif status == 'down':
                host_status = 'host apagado'  # Variable para el objeto Host
                apagados += 1
            for puertos in cada_host.getiterator('ports'):
                for childPorts in puertos:
                    portid = childPorts.get('portid')
                    lista_status = childPorts.getiterator('state')
                    for status in lista_status:
                        state = status.get('state')
                        if portid == '22' and state == 'open':
                            host_port_22_open += 1
                            puerto_22_abierto = 'puerto 22 abierto'  # Variable para el objeto Host
                        elif portid == '53' and state == 'open':    host_port_53_open += 1
                        if portid == '80' and state == 'open':  host_port_80_open += 1
                        elif portid == '443' and state == 'open':   host_port_443_open += 1
            for servidores in cada_host.getiterator('service'):
                name =  servidores.get('product')
                if name == 'Apache httpd' and paso:
                    serv_apache += 1
                    paso = not paso
                elif name == 'Dionaea Honeypot httpd' and paso:
                    serv_dionaea += 1
                    host_honeypot = 'es honeypot'  # Variable para el objeto Host
                    paso = not paso
                elif name == 'nginx' and paso:
                    serv_nginx += 1
                    paso = not paso
                elif name != None:
                    serv_otros += 1
            for hostnames in cada_host.getiterator('hostname'):
                names = hostnames.getiterator('hostname')
                for name in names:
                    nombre_dominio += 1
                    host_nombre_dominio = name.get('name')  # Variable para el objeto Host
            hosts.append(Host(ip, host_status, puerto_22_abierto, host_honeypot, host_nombre_dominio))  # Se agrega un objeto Host a la lista (de objetos) de hosts

        cantidades = [ prendidos, apagados, host_port_22_open, host_port_53_open, host_port_80_open, host_port_443_open, nombre_dominio,
                    serv_apache, serv_dionaea, serv_nginx, serv_otros ]  # Se almacenan las cantidades obtenidas para el reporte
        for cantidad in cantidades: reporte.append(cantidad)  # Se agrega a la lista reporte las cantidades obtenidas con el análisis

def escribe_reporte_cantidades(archivo_xml, archivo_reporte):
    """ Función para escribir el reporte de salida con la hora de ejecución, md5 y sha1 del archivo xml además de las cantidades solicitadas
    Recibe archivo xml para obtener md5 y sha1, archivo de reporte donde se escribiran los resultados. También muestra en la salida estándar
    los resultados del reporte"""
    hora_ejecucion = datetime.now().time()
    md5_archivo = 'md5: %s' %(md5(archivo_xml).hexdigest())
    sha1_archivo = 'sha1: %s' %(sha1(archivo_xml).hexdigest())
    datos = '%s\n%s\n%s\n' %(hora_ejecucion, md5_archivo, sha1_archivo)
    (prendidos, apagados, ssh, dns, http, https, nombre_dominio, apache, honeypots, nginx, otros) = reporte
    salida = 'Hosts Prendidos: %s\nHosts Apagados: %s\nPuerto 22 abierto: %s\nPuerto 53 abierto: %s\nPuerto 80 abierto: %s\n\
Puerto 443 abierto: %s\nCon nombre de dominio: %s\nServidores HTTP:\n\tApache: %s\n\tHoneypots (Dionaea): %s\n\tNginx: %s\n\
\tOtros servicios: %s\n' %(prendidos, apagados, ssh, dns, http, https, nombre_dominio, apache, honeypots, nginx, otros)
    print datos + salida
    with open(archivo_reporte, 'w') as reporte_salida:
        reporte_salida.write(datos + salida)

def escribe_reporte_CSV(archivo_reporte):
    """Función para generar el archivo CSV utilizando el método str de la clase Host. Recibe el archivo donde se escribirá el reporte CSV"""
    with open(archivo_reporte + '.csv','w') as reporte_csv:
        map(lambda host: reporte_csv.write(str(host)),hosts)

if __name__ == "__main__":
    if len(sys.argv) != 4:  # Se verifica que se reciban 4 argumentos, <script> <archivo_xml> <reporte1.txt> <reporteCSV>
        printError('Indicar archivo a leer, archivo de reporte y archivo de reporte CSV', True)
    lee_xml(sys.argv[1])
    escribe_reporte_cantidades(sys.argv[1], sys.argv[2])
    escribe_reporte_CSV(sys.argv[3])
