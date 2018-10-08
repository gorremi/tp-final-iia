# -*- coding: utf-8 -*-

#import json
import decodejson
import reglas
from functools import partial

from Tkinter import *
from pprint import pprint


class Jugador:
	def __init__(self,nombre,id_jug,promClarin,pj, pj_u5):
			self.nombre=nombre
			self.id_jug=id_jug
			self.prom_clarin=promClarin
			self.partidos_jugados=pj
			self.pj_ultimos5 = pj_u5
	#def __str__(self) :
	#	return "Jugador: ",self.nombre ," id: ",self.id_jug," promedio: " +str(self.promedio)

fecha=["","fecha1","fecha2","fecha3","fecha4","fecha5","fecha6","fecha7","fecha8","fecha9","fecha10","fecha11","fecha12","fecha13","fecha14","fecha15","fecha16","fecha17","fecha18","fecha19"]

global parafecha

jugadores = []
jug = decodejson.jugadores
goles = decodejson.goles
partidos = decodejson.partidos
equipos = decodejson.equipos
amarillas = decodejson.amonestados
rojas = decodejson.expulsados
figuras = decodejson.figuras

#Funciones para el análisis

def fueEnfecha(id_part):
	for p in partidos:
		if p["id_partido"] == id_part:
			return p["fecha"]


def contargoles(id_):  #cuenta los goles de un jugador, toma como argumento el id del jugador
	global parafecha
	gols = 0
	for g in goles:
		if (id_ == g["id_jug"]) and not(g["tipo"] == "en contra") and (fueEnfecha(g["id_partido"])<parafecha) :
			gols+=1
	return gols

def contaramarillas(id_):  #cuenta las amarillas de un jugador, toma como argumento el id del jugador
	global parafecha
	ama = 0
	for a in amarillas:
		if ((id_ == a["id_jug"]) and (fueEnfecha(a["id_partido"])<parafecha))  :
			ama+=1
	return ama

def contarrojas(id_):  #cuenta las rojas de un jugador, toma como argumento el id del jugador
	global parafecha
	roj = 0
	for r in rojas:
		if ((id_ == r["id_jug"]) and (fueEnfecha(r["id_partido"])<parafecha))  :
			roj+=1
	return roj

def contarfigura(id_):  #cuenta las veces que fue figura un jugador, toma como argumento el id del jugador
	global parafecha
	fig = 0
	for f in figuras:
		if ((id_ == f["id_jug"]) and (fueEnfecha(f["id_partido"])<parafecha))  :
			fig+=1
	return fig


def buscar_proximorival(equip): #busca le proximo rival de un equipo
	global parafecha
	for p in partidos:
		if (p["fecha"] == parafecha) and (equip == p["eq_local"]):
			return p["eq_visita"]
		if (p["fecha"] == parafecha) and (equip == p["eq_visita"]):
			return p["eq_local"]

def golesequipoF(equip):	#obtiene los goles a favor de un equipo
	global parafecha
	goles = 0
	for p in partidos:
		if p["fecha"] < parafecha :
			if p["eq_local"] == equip:
				goles = goles + p["g_local"]
			if p["eq_visita"] == equip:
				goles = goles + p["g_visita"]
			
	return goles

def golesequipoC(equip):	#obtiene los goles en contra de un equipo
	global parafecha
	goles = 0
	for p in partidos:
		if p["fecha"] < parafecha :
			if p["eq_local"] == equip:
				goles = goles + p["g_visita"]
			if p["eq_visita"] == equip:
				goles = goles + p["g_local"]
			
	return goles
	
def vallaInvicta(equip):	#obtiene la cantidad de partidos en la que un equipo no recibio goles
	global parafecha
	vallaInv = 0
	for p in partidos:
		if p["fecha"] < parafecha :
			if p["eq_local"] == equip:
				if p["g_visita"] == 0:
					vallaInv += 1
			if p["eq_visita"] == equip:
				if p["g_local"] == 0:
					vallaInv += 1
			
	return vallaInv

#Función para ordenar la lista de jugadores segun el valor obtenido en la defuzificación
def comparaIndices(x,y):
	if x.indiceReco < y.indiceReco:
		return -1
	elif x.indiceReco > y.indiceReco:
		return 1
	elif x.indiceReco == y.indiceReco:
		if x.prom_clarin < y.prom_clarin:
			return -1
		elif x.prom_clarin > y.prom_clarin:
			return 1
		elif x.prom_clarin == y.prom_clarin:
			if	x.promedio_gol < y.promedio_gol:
				return -1
			elif x.promedio_gol > y.promedio_gol:
				return 1
			elif x.promedio_gol == y.promedio_gol:
				if x.amarillas > y.amarillas:
					return -1
				elif x.amarillas < y.amarillas:
					return 1
				else:
					return 0
			else:
				return 0
		else:
			return 0
	else:
		return 0

def comparaIndicesArq(x,y):
	if x.indiceReco < y.indiceReco:
		return -1
	elif x.indiceReco > y.indiceReco:
		return 1
	elif x.indiceReco == y.indiceReco:
		if x.prom_goles_recib < y.prom_goles_recib:
			return 1
		elif x.prom_clarin > y.prom_clarin:
			return -1
		elif x.prom_goles_recib == y.prom_goles_recib:
			if x.prom_goles_rival_F > y.prom_goles_rival_F:
				return -1
			elif x.prom_goles_rival_F < y.prom_goles_rival_F:
				return 1
			else:
				return 0
		else:
			return 0
	else:
		return 0


#Funciones para mostrar los resultados
color = "#9CC4FA"

#Captura el frame que crea la funcion, para despues destruirlo en la siguiente llamada
global frameGlobalListaJug
global analisis
global v_res
def mostrarInfo(jug):
	global analisis
	analisis.destroy()
	global v_res
	an=Frame(v_res,width=400, height=500,bg=color)
	
	Label(an,text="Nombre: ",width=20,anchor=W,bg=color).grid(row=1,column=1)
	Label(an,text=jug.nombre,width=30,anchor=W,bg=color).grid(row=1,column=2)
	Label(an,text="Equipo: ",width=20,anchor=W,bg=color).grid(row=2,column=1)
	Label(an,text=jug.equipo,width=30,anchor=W,bg=color).grid(row=2,column=2)
	Label(an,text="Partidos jugados: ",width=20,anchor=W,bg=color).grid(row=3,column=1)
	Label(an,text=int(jug.partidos_jugados),width=30,anchor=W,bg=color).grid(row=3,column=2)
	Label(an,text="Promedio Clarin: ",width=20,anchor=W,bg=color).grid(row=4,column=1)
	Label(an,text='%.3f'%jug.prom_clarin,width=30,anchor=W,bg=color).grid(row=4,column=2)
	Label(an,text="Posición: ",width=20,anchor=W,bg=color).grid(row=5,column=1)
	Label(an,text=jug.posicion,width=30,anchor=W,bg=color).grid(row=5,column=2)
	Label(an,text="Promedio de gol: ",width=20,anchor=W,bg=color).grid(row=6,column=1)
	Label(an,text='%.3f'%jug.promedio_gol,width=30,anchor=W,bg=color).grid(row=6,column=2)		
	Label(an,text="Próximo rival: ",width=20,anchor=W,bg=color).grid(row=7,column=1)
	Label(an,text=jug.proximo_rival,width=30,anchor=W,bg=color).grid(row=7,column=2)
	if (jug.posicion == "DEF") or (jug.posicion == "ARQ"):
		Label(an,text="Promedio goles en contra de %s: "%jug.equipo,width=20,anchor=W,wraplength=140,bg=color).grid(row=8,column=1)
		Label(an,text='%.3f'%jug.prom_goles_recib,width=30,anchor=W,bg=color).grid(row=8,column=2)	
		Label(an,text="Vallas invictas: ",width=20,anchor=W,bg=color).grid(row=9,column=1)
		Label(an,text=jug.veces_vi,width=30,anchor=W,bg=color).grid(row=9,column=2)	
		Label(an,text="Promedio goles a favor del próximo rival: ",width=20,anchor=W,wraplength=140,bg=color).grid(row=10,column=1)
		Label(an,text='%.3f'%jug.prom_goles_rival_F,width=30,anchor=W,bg=color).grid(row=10,column=2)
		
	else:
		Label(an,text="Promedio goles en contra de %s: "%jug.proximo_rival,width=20,anchor=W,wraplength=140,bg=color).grid(row=8,column=1)
		Label(an,text='%.3f'%jug.prom_goles_rival_C,width=30,anchor=W,bg=color).grid(row=8,column=2)	
			
			
	an.pack(anchor=NW,padx=10,pady=45)
	analisis = an
	
def imprimirDelanteros(padre,delanteros):
	global frameGlobalListaJug
	global analisis
	analisis.destroy()
	frameGlobalListaJug.destroy()
	lista=Frame(padre,width=400, height=500,bg=color)
	
	
	Label(lista,text= "Delanteros Recomendados:",font= 25,bg=color).pack(anchor=NW,padx=0)
	lista2=Frame(lista,bd=3,relief=RIDGE,bg="#7E7E7E")
	
	fila=1
	Label(lista2,text="Jugador",bg="#C6CDC6",width=30,anchor=W,bd=2,relief=RAISED,highlightthickness=1.5).grid(row=fila,column=1)
	Label(lista2,text="POS",bg="#C6CDC6",width=5,anchor=W,bd=2,relief=RAISED,highlightthickness=1.5).grid(row=fila,column=2)
	Label(lista2,text="Equipo",bg="#C6CDC6",width=15,anchor=W,bd=2,relief=RAISED,highlightthickness=1.5).grid(row=fila,column=3)
	Label(lista2,text="Indice",bg="#C6CDC6",width=15,anchor=W,bd=2,relief=RAISED,highlightthickness=1.5).grid(row=fila,column=4)
	Label(lista2,text="Info",bg="#C6CDC6",width=5,anchor=W,bd=2,relief=RAISED,highlightthickness=1.5).grid(row=fila,column=5)
	fila=2
	for j in delanteros:			
			Label(lista2,text=j.nombre,bg="#F33C3C",width=30,anchor=W,bd=2,relief=RAISED,highlightthickness=1.5).grid(row=fila,column=1)
			Label(lista2,text=j.posicion,bg="#F33C3C",width=5,anchor=W,bd=2,relief=RAISED,highlightthickness=1.5).grid(row=fila,column=2)
			Label(lista2,text=j.equipo,bg="#F33C3C",width=15,anchor=W,bd=2,relief=RAISED,highlightthickness=1.5).grid(row=fila,column=3)
			Label(lista2,text=str(j.indiceReco),bg="#F33C3C",width=15,anchor=W,bd=2,relief=RAISED,highlightthickness=1.5).grid(row=fila,column=4)
			fun = partial(mostrarInfo,j)
			Button(lista2,text="ver",bg="#F33C3C",command=fun,width=5,borderwidth=0.5,pady=1).grid(row=fila,column=5)
			fila +=1
	
	
	lista2.pack(anchor=NW,padx=0,pady=10)
	lista.pack(anchor=NW,padx=10,pady=10,side=LEFT)
	
	mostrarInfo(delanteros[0])
	
	
	frameGlobalListaJug = lista
	
def imprimirMedios(padre,meds):
	
	global frameGlobalListaJug
	global analisis
	analisis.destroy()
	frameGlobalListaJug.destroy()
	lista=Frame(padre,width=400, height=500,bg=color)
	
	
	Label(lista,text= "Medios Recomendados:",font= 25,bg=color).pack(anchor=NW,padx=0)
	lista2=Frame(lista,bd=3,relief=RIDGE,bg="#7E7E7E")
	
	fila=1
	Label(lista2,text="Jugador",bg="#C6CDC6",width=30,anchor=W,bd=2,relief=RAISED,highlightthickness=1.5).grid(row=fila,column=1)
	Label(lista2,text="POS",bg="#C6CDC6",width=5,anchor=W,bd=2,relief=RAISED,highlightthickness=1.5).grid(row=fila,column=2)
	Label(lista2,text="Equipo",bg="#C6CDC6",width=15,anchor=W,bd=2,relief=RAISED,highlightthickness=1.5).grid(row=fila,column=3)
	Label(lista2,text="Indice",bg="#C6CDC6",width=15,anchor=W,bd=2,relief=RAISED,highlightthickness=1.5).grid(row=fila,column=4)
	Label(lista2,text="Info",bg="#C6CDC6",width=5,anchor=W,bd=2,relief=RAISED,highlightthickness=1.5).grid(row=fila,column=5)
	fila=2
	for j in meds:			
			Label(lista2,text=j.nombre,bg="#18CFF0",width=30,anchor=W,bd=2,relief=RAISED,highlightthickness=1.5).grid(row=fila,column=1)
			Label(lista2,text=j.posicion,bg="#18CFF0",width=5,anchor=W,bd=2,relief=RAISED,highlightthickness=1.5).grid(row=fila,column=2)
			Label(lista2,text=j.equipo,bg="#18CFF0",width=15,anchor=W,bd=2,relief=RAISED,highlightthickness=1.5).grid(row=fila,column=3)
			Label(lista2,text=str(j.indiceReco),bg="#18CFF0",width=15,anchor=W,bd=2,relief=RAISED,highlightthickness=1.5).grid(row=fila,column=4)
			fun = partial(mostrarInfo,j)
			Button(lista2,text="ver",bg="#18CFF0",command=fun,width=5,borderwidth=0.5,pady=1).grid(row=fila,column=5)
			fila +=1
	
	
	lista2.pack(anchor=NW,padx=0,pady=10)
	lista.pack(anchor=NW,padx=10,pady=10,side=LEFT)
	
	mostrarInfo(meds[0])
	
	
	frameGlobalListaJug = lista

def imprimirDefensores(padre,defe):
	
	global frameGlobalListaJug
	global analisis
	analisis.destroy()
	frameGlobalListaJug.destroy()
	lista=Frame(padre,width=400, height=500,bg=color)
	
	
	Label(lista,text= "Defensores Recomendados:",font= 25,bg=color).pack(anchor=NW,padx=0)
	lista2=Frame(lista,bd=3,relief=RIDGE,bg="#7E7E7E")
	
	fila=1
	Label(lista2,text="Jugador",bg="#C6CDC6",width=30,anchor=W,bd=2,relief=RAISED,highlightthickness=1.5).grid(row=fila,column=1)
	Label(lista2,text="POS",bg="#C6CDC6",width=5,anchor=W,bd=2,relief=RAISED,highlightthickness=1.5).grid(row=fila,column=2)
	Label(lista2,text="Equipo",bg="#C6CDC6",width=15,anchor=W,bd=2,relief=RAISED,highlightthickness=1.5).grid(row=fila,column=3)
	Label(lista2,text="Indice",bg="#C6CDC6",width=15,anchor=W,bd=2,relief=RAISED,highlightthickness=1.5).grid(row=fila,column=4)
	Label(lista2,text="Info",bg="#C6CDC6",width=5,anchor=W,bd=2,relief=RAISED,highlightthickness=1.5).grid(row=fila,column=5)
	fila=2
	for j in defe:			
			Label(lista2,text=j.nombre,bg="#47FD47",width=30,anchor=W,bd=2,relief=RAISED,highlightthickness=1.5).grid(row=fila,column=1)
			Label(lista2,text=j.posicion,bg="#47FD47",width=5,anchor=W,bd=2,relief=RAISED,highlightthickness=1.5).grid(row=fila,column=2)
			Label(lista2,text=j.equipo,bg="#47FD47",width=15,anchor=W,bd=2,relief=RAISED,highlightthickness=1.5).grid(row=fila,column=3)
			Label(lista2,text=str(j.indiceReco),bg="#47FD47",width=15,anchor=W,bd=2,relief=RAISED,highlightthickness=1.5).grid(row=fila,column=4)
			fun = partial(mostrarInfo,j)
			Button(lista2,text="ver",bg="#47FD47",command=fun,width=5,borderwidth=0.5,pady=1).grid(row=fila,column=5)
			fila +=1
	
	
	lista2.pack(anchor=NW,padx=0,pady=10)
	lista.pack(anchor=NW,padx=10,pady=10,side=LEFT)
	
	mostrarInfo(defe[0])
	
	
	frameGlobalListaJug = lista

def imprimirArqueros(padre,arq):
	
	global frameGlobalListaJug
	global analisis
	analisis.destroy()
	frameGlobalListaJug.destroy()
	lista=Frame(padre,width=400, height=500,bg=color)
	
	
	Label(lista,text= "Defensores Recomendados:",font= 25,bg=color).pack(anchor=NW,padx=0)
	lista2=Frame(lista,bd=3,relief=RIDGE,bg="#7E7E7E")
	
	fila=1
	Label(lista2,text="Jugador",bg="#C6CDC6",width=30,anchor=W,bd=2,relief=RAISED,highlightthickness=1.5).grid(row=fila,column=1)
	Label(lista2,text="POS",bg="#C6CDC6",width=5,anchor=W,bd=2,relief=RAISED,highlightthickness=1.5).grid(row=fila,column=2)
	Label(lista2,text="Equipo",bg="#C6CDC6",width=15,anchor=W,bd=2,relief=RAISED,highlightthickness=1.5).grid(row=fila,column=3)
	Label(lista2,text="Indice",bg="#C6CDC6",width=15,anchor=W,bd=2,relief=RAISED,highlightthickness=1.5).grid(row=fila,column=4)
	Label(lista2,text="Info",bg="#C6CDC6",width=5,anchor=W,bd=2,relief=RAISED,highlightthickness=1.5).grid(row=fila,column=5)
	fila=2
	for j in arq:			
			Label(lista2,text=j.nombre,bg="#D6C641",width=30,anchor=W,bd=2,relief=RAISED,highlightthickness=1.5).grid(row=fila,column=1)
			Label(lista2,text=j.posicion,bg="#D6C641",width=5,anchor=W,bd=2,relief=RAISED,highlightthickness=1.5).grid(row=fila,column=2)
			Label(lista2,text=j.equipo,bg="#D6C641",width=15,anchor=W,bd=2,relief=RAISED,highlightthickness=1.5).grid(row=fila,column=3)
			Label(lista2,text=str(j.indiceReco),bg="#D6C641",width=15,anchor=W,bd=2,relief=RAISED,highlightthickness=1.5).grid(row=fila,column=4)
			fun = partial(mostrarInfo,j)
			Button(lista2,text="ver",bg="#D6C641",command=fun,width=5,borderwidth=0.5,pady=1).grid(row=fila,column=5)
			fila +=1
	
	
	lista2.pack(anchor=NW,padx=0,pady=10)
	lista.pack(anchor=NW,padx=10,pady=10,side=LEFT)
	
	mostrarInfo(arq[0])
	
	
	frameGlobalListaJug = lista

def imprimirEquipo(padre,arq,defe,med,delanteros):
	global frameGlobalListaJug
	global analisis
	analisis.destroy()
	frameGlobalListaJug.destroy()
	lista=Frame(padre,width=400, height=500,bg=color)
	
	Label(lista,text= "Equipo Recomendado:",font= 25,bg=color).pack(anchor=NW,padx=0)
	lista2=Frame(lista,bd=3,relief=RIDGE,bg="#7E7E7E")
	
	fila=1
	Label(lista2,text="Jugador",bg="#C6CDC6",width=30,anchor=W,bd=2,relief=RAISED,highlightthickness=1.5).grid(row=fila,column=1)
	Label(lista2,text="POS",bg="#C6CDC6",width=5,anchor=W,bd=2,relief=RAISED,highlightthickness=1.5).grid(row=fila,column=2)
	Label(lista2,text="Equipo",bg="#C6CDC6",width=15,anchor=W,bd=2,relief=RAISED,highlightthickness=1.5).grid(row=fila,column=3)
	Label(lista2,text="Indice",bg="#C6CDC6",width=15,anchor=W,bd=2,relief=RAISED,highlightthickness=1.5).grid(row=fila,column=4)
	Label(lista2,text="Info",bg="#C6CDC6",width=5,anchor=W,bd=2,relief=RAISED,highlightthickness=1.5).grid(row=fila,column=5)
	
	
	fila = 2
	for j in arq[0:1]:			
			Label(lista2,text=j.nombre,bg="#D6C641",width=30,anchor=W,bd=2,relief=RAISED,highlightthickness=1.5).grid(row=fila,column=1)
			Label(lista2,text=j.posicion,bg="#D6C641",width=5,anchor=W,bd=2,relief=RAISED,highlightthickness=1.5).grid(row=fila,column=2)
			Label(lista2,text=j.equipo,bg="#D6C641",width=15,anchor=W,bd=2,relief=RAISED,highlightthickness=1.5).grid(row=fila,column=3)
			Label(lista2,text=str(j.indiceReco),bg="#D6C641",width=15,anchor=W,bd=2,relief=RAISED,highlightthickness=1.5).grid(row=fila,column=4)
			fun = partial(mostrarInfo,j)
			Button(lista2,text="ver",bg="#D6C641",command=fun,width=5,borderwidth=0.5,pady=1).grid(row=fila,column=5)
			
			fila +=1
	for j in defe[0:3]:			
			Label(lista2,text=j.nombre,bg="#47FD47",width=30,anchor=W,bd=2,relief=RAISED,highlightthickness=1.5).grid(row=fila,column=1)
			Label(lista2,text=j.posicion,bg="#47FD47",width=5,anchor=W,bd=2,relief=RAISED,highlightthickness=1.5).grid(row=fila,column=2)
			Label(lista2,text=j.equipo,bg="#47FD47",width=15,anchor=W,bd=2,relief=RAISED,highlightthickness=1.5).grid(row=fila,column=3)
			Label(lista2,text=str(j.indiceReco),bg="#47FD47",width=15,anchor=W,bd=2,relief=RAISED,highlightthickness=1.5).grid(row=fila,column=4)
			fun = partial(mostrarInfo,j)
			Button(lista2,text="ver",bg="#47FD47",command=fun,width=5,borderwidth=0.5,pady=1).grid(row=fila,column=5)
			
			fila +=1
	for j in med[0:4]:			
			Label(lista2,text=j.nombre,bg="#18CFF0",width=30,anchor=W,bd=2,relief=RAISED,highlightthickness=1.5).grid(row=fila,column=1)
			Label(lista2,text=j.posicion,bg="#18CFF0",width=5,anchor=W,bd=2,relief=RAISED,highlightthickness=1.5).grid(row=fila,column=2)
			Label(lista2,text=j.equipo,bg="#18CFF0",width=15,anchor=W,bd=2,relief=RAISED,highlightthickness=1.5).grid(row=fila,column=3)
			Label(lista2,text=str(j.indiceReco),bg="#18CFF0",width=15,anchor=W,bd=2,relief=RAISED,highlightthickness=1.5).grid(row=fila,column=4)
			fun = partial(mostrarInfo,j)
			Button(lista2,text="ver",bg="#18CFF0",command=fun,width=5,borderwidth=0.5,pady=1).grid(row=fila,column=5)
			fila +=1
	for j in delanteros[0:3]:			
			Label(lista2,text=j.nombre,bg="#F33C3C",width=30,anchor=W,bd=2,relief=RAISED,highlightthickness=1.5).grid(row=fila,column=1)
			Label(lista2,text=j.posicion,bg="#F33C3C",width=5,anchor=W,bd=2,relief=RAISED,highlightthickness=1.5).grid(row=fila,column=2)
			Label(lista2,text=j.equipo,bg="#F33C3C",width=15,anchor=W,bd=2,relief=RAISED,highlightthickness=1.5).grid(row=fila,column=3)
			Label(lista2,text=str(j.indiceReco),bg="#F33C3C",width=15,anchor=W,bd=2,relief=RAISED,highlightthickness=1.5).grid(row=fila,column=4)
			fun = partial(mostrarInfo,j)
			Button(lista2,text="ver",bg="#F33C3C",command=fun,width=5,borderwidth=0.5,pady=1).grid(row=fila,column=5)
			fila +=1
	
	
	lista2.pack(anchor=NW,padx=0,pady=10)
	
	Label(lista,text= "Suplentes:",font= 25,bg=color).pack(anchor=NW,padx=0,pady=5)
	
	
	lista3=Frame(lista,bd=3,relief=RIDGE,bg="#7E7E7E")
	
	fila=1
	Label(lista3,text="Jugador",bg="#C6CDC6",width=30,anchor=W,bd=2,relief=RAISED,highlightthickness=1.5).grid(row=fila,column=1)
	Label(lista3,text="POS",bg="#C6CDC6",width=5,anchor=W,bd=2,relief=RAISED,highlightthickness=1.5).grid(row=fila,column=2)
	Label(lista3,text="Equipo",bg="#C6CDC6",width=15,anchor=W,bd=2,relief=RAISED,highlightthickness=1.5).grid(row=fila,column=3)
	Label(lista3,text="Indice",bg="#C6CDC6",width=15,anchor=W,bd=2,relief=RAISED,highlightthickness=1.5).grid(row=fila,column=4)
	Label(lista3,text="Info",bg="#C6CDC6",width=5,anchor=W,bd=2,relief=RAISED,highlightthickness=1.5).grid(row=fila,column=5)
	
	
	
	fila=2
	for j in arq[1:2]:			
			Label(lista3,text=j.nombre,bg="#D6C641",width=30,anchor=W,bd=2,relief=RAISED,highlightthickness=1.5).grid(row=fila,column=1)
			Label(lista3,text=j.posicion,bg="#D6C641",width=5,anchor=W,bd=2,relief=RAISED,highlightthickness=1.5).grid(row=fila,column=2)
			Label(lista3,text=j.equipo,bg="#D6C641",width=15,anchor=W,bd=2,relief=RAISED,highlightthickness=1.5).grid(row=fila,column=3)
			Label(lista3,text=str(j.indiceReco),bg="#D6C641",width=15,anchor=W,bd=2,relief=RAISED,highlightthickness=1.5).grid(row=fila,column=4)
			fun = partial(mostrarInfo,j)
			Button(lista3,text="ver",bg="#D6C641",command=fun,width=5,borderwidth=0.5,pady=1).grid(row=fila,column=5)
			fila +=1
	for j in defe[3:4]:			
			Label(lista3,text=j.nombre,bg="#47FD47",width=30,anchor=W,bd=2,relief=RAISED,highlightthickness=1.5).grid(row=fila,column=1)
			Label(lista3,text=j.posicion,bg="#47FD47",width=5,anchor=W,bd=2,relief=RAISED,highlightthickness=1.5).grid(row=fila,column=2)
			Label(lista3,text=j.equipo,bg="#47FD47",width=15,anchor=W,bd=2,relief=RAISED,highlightthickness=1.5).grid(row=fila,column=3)
			Label(lista3,text=str(j.indiceReco),bg="#47FD47",width=15,anchor=W,bd=2,relief=RAISED,highlightthickness=1.5).grid(row=fila,column=4)
			fun = partial(mostrarInfo,j)
			Button(lista3,text="ver",bg="#47FD47",command=fun,width=5,borderwidth=0.5,pady=1).grid(row=fila,column=5)
			fila +=1
	for j in med[4:5]:			
			Label(lista3,text=j.nombre,bg="#18CFF0",width=30,anchor=W,bd=2,relief=RAISED,highlightthickness=1.5).grid(row=fila,column=1)
			Label(lista3,text=j.posicion,bg="#18CFF0",width=5,anchor=W,bd=2,relief=RAISED,highlightthickness=1.5).grid(row=fila,column=2)
			Label(lista3,text=j.equipo,bg="#18CFF0",width=15,anchor=W,bd=2,relief=RAISED,highlightthickness=1.5).grid(row=fila,column=3)
			Label(lista3,text=str(j.indiceReco),bg="#18CFF0",width=15,anchor=W,bd=2,relief=RAISED,highlightthickness=1.5).grid(row=fila,column=4)
			fun = partial(mostrarInfo,j)
			Button(lista3,text="ver",bg="#18CFF0",command=fun,width=5,borderwidth=0.5,pady=1).grid(row=fila,column=5)
			fila +=1
	for j in delanteros[3:4]:			
			Label(lista3,text=j.nombre,bg="#F33C3C",width=30,anchor=W,bd=2,relief=RAISED,highlightthickness=1.5).grid(row=fila,column=1)
			Label(lista3,text=j.posicion,bg="#F33C3C",width=5,anchor=W,bd=2,relief=RAISED,highlightthickness=1.5).grid(row=fila,column=2)
			Label(lista3,text=j.equipo,bg="#F33C3C",width=15,anchor=W,bd=2,relief=RAISED,highlightthickness=1.5).grid(row=fila,column=3)
			Label(lista3,text=str(j.indiceReco),bg="#F33C3C",width=15,anchor=W,bd=2,relief=RAISED,highlightthickness=1.5).grid(row=fila,column=4)
			fun = partial(mostrarInfo,j)
			Button(lista3,text="ver",bg="#F33C3C",command=fun,width=5,borderwidth=0.5,pady=1).grid(row=fila,column=5)
			fila +=1
	
	lista3.pack(anchor=NW,padx=0,pady=5)
	
	Label(lista,text= "Nota: La comparación de índices es entre jugadores de la misma posición, no usar el índice para comparar jugadores de distinta posición",font= 15,wraplength=500,bg=color).pack(anchor=NW,padx=0,pady=5)
	
	
	lista.pack(anchor=NW,padx=10,pady=10,side=LEFT)
	
	mostrarInfo(arq[0])
	
	
	frameGlobalListaJug = lista
			
	






#Analisis
def calculo(pf,ventanapadre):
	global parafecha
	parafecha = pf

	jugadores = []
	

	
	#print "\n ------ \n"
	#print "Para fecha ", parafecha,"   : \n"

	for i in range(len(jug)) :
		puntosClarin=0.000
		partidosjugados=0.000
		pj_ultimos5 = 0
		jugoUltimo = 0
		promClarin =0
		promgol =0.00
		for j in range(parafecha-1) :
			if jug[i][fecha[j+1]] is not None :
				partidosjugados +=1
				puntosClarin +=jug[i][fecha[j+1]]
				if (j+1) >= (parafecha-5):
					pj_ultimos5 +=1
				if (j+1) == (parafecha-1):
					jugoUltimo = 1
		if partidosjugados > 0 :
			promClarin = puntosClarin / partidosjugados
			promgol = (contargoles(jug[i]["id_jug"]) / partidosjugados)
			
		jugadores.append(Jugador(jug[i]["nombre"],jug[i]["id_jug"],promClarin,partidosjugados,pj_ultimos5))
		
		jugadores[i].equipo=jug[i]["equipo"]
		jugadores[i].numero=jug[i]["numero"]
		jugadores[i].posicion=jug[i]["pos"]
		jugadores[i].promedio_gol= promgol
		jugadores[i].proximo_rival = buscar_proximorival(jug[i]["equipo"])
		jugadores[i].prom_goles_rival_F = (golesequipoF(jugadores[i].proximo_rival)*1.000) / (parafecha-1)  
		jugadores[i].prom_goles_rival_C = (golesequipoC(jugadores[i].proximo_rival)*1.000) / (parafecha-1)
		jugadores[i].prom_goles_recib = (golesequipoC(jugadores[i].equipo)*1.000) / (parafecha-1)
		jugadores[i].valla_invicta = (vallaInvicta( jugadores[i].equipo ) *1.000) / (parafecha-1)
		jugadores[i].veces_vi = vallaInvicta( jugadores[i].equipo )
		jugadores[i].amarillas = (contaramarillas(jug[i]["id_jug"]) *1.000) / (parafecha-1)
		jugadores[i].rojas = (contarrojas(jug[i]["id_jug"])*1.000) / (parafecha-1)
		jugadores[i].veces_figura = contarfigura(jug[i]["id_jug"])
		jugadores[i].ultimo = jugoUltimo		
	
	
	
	
	
	
	for j in jugadores:
		if j.posicion == "DEL":
			j.indiceReco = reglas.calculoDelantero(j.prom_clarin,j.promedio_gol,j.prom_goles_rival_C)
		if j.posicion == "MED":
			j.indiceReco = reglas.calculoMedio(j.prom_clarin,j.promedio_gol,j.prom_goles_rival_C)
		if j.posicion == "DEF":
			j.indiceReco = reglas.calculoDefensor(j.prom_clarin,j.promedio_gol,j.prom_goles_recib,j.valla_invicta,j.prom_goles_rival_F,j.amarillas)
		if j.posicion == "ARQ":
			j.indiceReco = reglas.calculoArquero(j.prom_clarin,j.prom_goles_recib,j.prom_goles_rival_F)
	
	
	
	delanteros = filter(lambda x: (x.posicion == "DEL") and ((x.partidos_jugados >= ((parafecha-1)/2)) or (x.pj_ultimos5 > 2)) , jugadores)
	
	medios = filter(lambda x: (x.posicion == "MED") and ((x.partidos_jugados >= ((parafecha-1)/2)) or (x.pj_ultimos5 > 2)) , jugadores)
	
	defensores = filter(lambda x: (x.posicion == "DEF") and ((x.partidos_jugados >= ((parafecha-1)/2)) or (x.pj_ultimos5 > 2) or (x.ultimo == 1)) , jugadores)
	
	arqueros = filter(lambda x: (x.posicion == "ARQ") and ((x.partidos_jugados >= ((parafecha-1)/2)) or (x.pj_ultimos5 > 3) or (x.ultimo == 1)) , jugadores)
	
	
	delanteros.sort(comparaIndices)
	delanteros.reverse()
	
	medios.sort(comparaIndices)
	medios.reverse()
	
	defensores.sort(comparaIndices)
	defensores.reverse()
	
	arqueros.sort(comparaIndicesArq)
	arqueros.reverse()
	
	v_resultados = Toplevel(ventanapadre,bg=color)
	v_resultados.geometry("1000x650")

	botonera = Frame(v_resultados)	
	Button(botonera,text="Equipo recomendado",command=lambda:imprimirEquipo(v_resultados,arqueros[0:2],defensores[0:4],medios[0:5],delanteros[0:4]),bg="#C6CDC6").pack(side=LEFT)
	Button(botonera,text="Delanteros recomendados",command=lambda:imprimirDelanteros(v_resultados,delanteros[0:15]),bg="#C6CDC6").pack(side=LEFT)
	Button(botonera,text="Medios recomendados",command=lambda:imprimirMedios(v_resultados,medios[0:15]),bg="#C6CDC6").pack(side=LEFT)
	Button(botonera,text="Defensores recomendados",command=lambda:imprimirDefensores(v_resultados,defensores[0:15]),bg="#C6CDC6").pack(side=LEFT)
	Button(botonera,text="Arqueros recomendados",command=lambda:imprimirArqueros(v_resultados,arqueros[0:5]),bg="#C6CDC6").pack(side=LEFT)
	botonera.pack(anchor=NW,padx=10,pady=5)
	#lista_jug=Frame(v_resultados,width=400, height=500).pack(side=LEFT,anchor=NW,padx=10,pady=10)
	fram=Frame(v_resultados)
	global frameGlobalListaJug
	frameGlobalListaJug=fram
	global analisis
	analisis=Frame(v_resultados)
	global v_res
	v_res = v_resultados
	imprimirEquipo(v_resultados,arqueros[0:2],defensores[0:4],medios[0:5],delanteros[0:4])

	
ventana_ppal = Tk()
ventana_ppal.geometry("400x230")

#cabecera=Frame(ventana_ppal,width=400, height=150).pack()
cabecera = Frame(ventana_ppal).pack()
img_cabe=PhotoImage(file="imag/cabecera.gif")

label1 = Label(cabecera, image=img_cabe).pack()
base=Frame(ventana_ppal)
ingresa_fecha=Label(base,text="Realizar cálculo para la fecha: ",font=34).grid(row=1,column=1)
casilla=IntVar()
Entry(base,textvar=casilla,width=10).grid(row=1,column=2)

Button(base,text="Calcular",command=lambda: calculo(casilla.get(),ventana_ppal)).grid(row=2,column=1)
base.pack()

ventana_ppal.mainloop()
