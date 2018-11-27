#!/usr/bin/python
# -*- coding: utf-8 -*-
#UNAM-CERT
##### Valide a los becarios sin importar si estan en minúsculas o mayúsculas
### inserte a los becarios aprobados en mayúsculas
#### Ordene la lista de aprobados despuÃ©s de hacer una insercion

## Función que permite borrar a un becario aprobado a partir de su nombre completo
#      Recibe nombre del bec a eliminar; regresa True si se pudo eliminar y False si no se encontraba en la lista
aprobados = []
bec = []
lista = ['Manuel','Valeria','Alejandro','Luis','Enrique','Omar','Abraham','Oscar']

def aprueba_becario(nombre_completo):
    nombre_separado = nombre_completo.split()
    for nombre in lista:
	if len(bec) == len(lista):
		break;
	bec.append(nombre.lower())
    for n in nombre_separado:
        if n in bec:
            return False
    aprobados.append(nombre_completo.upper())
    aprobados.sort()
    return True

def borrar_completo(nombre_becario):
    if nombre_becario.upper() in aprobados:
	aprobados.remove(nombre_becario.upper())
	return True
    else:
	return False


becarios = ['Cervantes Varela JUAN MaNuEl',
            'Leal González IgnaciO',
            'Ortiz Velarde valeria',
            'Martínez Salazar LUIS ANTONIO',
            'Rodrí­guez Gallardo pedro alejandro',
            'Tadeo Guillén DiAnA GuAdAlUpE',
            'Ferrusca Ortiz jorge luis',
            'Juárez Méndez JeSiKa',
            'Pacheco Franco jesus ENRIQUE',
            'Vallejo Fernández RAFAEL alejanDrO',
            'López Fernández serVANDO MIGuel',
            'Hernández González ricaRDO OMAr',
            'Acevedo Gómez LAura patrICIA',
            'Manzano Cruz isaías AbrahaM',
            'Espinosa Curiel OscaR']
for b in becarios:
    if aprueba_becario(b.lower()):
        print 'APROBADOO: ' + b
    else:
        print 'REPROBADO: ' + b

if borrar_completo('Rafael Alejandro VAllejo Fernández'):
	print 'Se  eliminó de la lista'
else:
	print 'No se encontró en la lista'

#print aprobados
#print bec
#print becarios
