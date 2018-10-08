# -*- coding: utf-8 -*-

import json
 



#d = open('gran_dt.json')
d = open('datos/fecha_18_completa.json')
lectura = d.read()
datosJSON = lectura



##############

#Amonestados
indiceA = datosJSON.find('gran_dt.amonestados')

indiceA1 = datosJSON.find('[',indiceA)    
indiceA2 = datosJSON.find(']',indiceA)

amonestadosJSON = datosJSON[indiceA1 : indiceA2 +1]

#Equipos
indiceEq = datosJSON.find('gran_dt.equipos')

indiceEq1 = datosJSON.find('[',indiceEq)    
indiceEq2 = datosJSON.find(']',indiceEq)

equiposJSON = datosJSON[indiceEq1 : indiceEq2 +1]

#Expulsados
indiceEx = datosJSON.find('gran_dt.expulsados')

indiceEx1 = datosJSON.find('[',indiceEx)    
indiceEx2 = datosJSON.find(']',indiceEx)

expulsadosJSON = datosJSON[indiceEx1 : indiceEx2 +1]

#Figura
indiceF = datosJSON.find('gran_dt.figura')

indiceF1 = datosJSON.find('[',indiceF)    
indiceF2 = datosJSON.find(']',indiceF)

figuraJSON = datosJSON[indiceF1 : indiceF2 +1]

#Goles
indiceG = datosJSON.find('gran_dt.goles')

indiceG1 = datosJSON.find('[',indiceG)    
indiceG2 = datosJSON.find(']',indiceG)

golesJSON = datosJSON[indiceG1 : indiceG2 +1]

#Incidencias
indiceI = datosJSON.find('gran_dt.incidencias')

indiceI1 = datosJSON.find('[',indiceI)    
indiceI2 = datosJSON.find(']',indiceI)

incidenciasJSON = datosJSON[indiceI1 : indiceI2 +1]


#Jugadores
indiceJ = datosJSON.find('gran_dt.jugadores')

indiceJ1 = datosJSON.find('[',indiceJ)    
indiceJ2 = datosJSON.find(']',indiceJ)

jugadoresJSON = datosJSON[indiceJ1 : indiceJ2 +1]

#Partidos
indiceP = datosJSON.find('gran_dt.partidos')

indiceP1 = datosJSON.find('[',indiceP)    
indiceP2 = datosJSON.find(']',indiceP)

partidosJSON = datosJSON[indiceP1 : indiceP2 +1]


###############



amonestados = json.loads(amonestadosJSON) 
equipos = json.loads(equiposJSON)
expulsados = json.loads(expulsadosJSON)
figuras = json.loads(figuraJSON)
goles = json.loads(golesJSON)
incidencias = json.loads(incidenciasJSON)
jugadores = json.loads(jugadoresJSON)
partidos = json.loads(partidosJSON)

