import reglasDelanteros
import reglasMedios
import reglasDefensores
import reglasArqueros

# Conjuntos de etiquetas:
#  nombre_del_conjunto = [(etiqueta,1er,2do,3ro,4to),...... ]
#                  indice      0     1   2   3   4
# 1ro,2do,3ro,4to representan un trapecio
# para representar un triangulo, 2do=3ro

#VC ---> Variable de Control
# NR = No recomendado, PR = Poco Recomendado, AR = Algo recomendado, R = Recomendado, BR = Bastante Recomendado, MR = Muy Recomendado
VC = [("NR",0,0,4,6),("PR",4,6,6,8),("AR",6,8,10,12),("R",10,12,14,16),("BR",14,16,16,18),("MR",16,18,20,20)]


#PC ---> Promedio Puntaje Clarin
# DM = Demasiado Bajo; MB = Muy bajo; B = Bajo; M = Medio; A = Alto; MA = Muy alto
#original PC= [("DM",0,0,3,4),("MB",3.4,3.6,4.4,4.6),("B",4.4,4.6,5.4,5.6),("M",5.4,5.6,6,6.2),("A",6,6.2,6.8,7.2),("MA",6.8,7.2,10,10)]

PC= [("DM",0,0,3,4),("MB",3.2,3.6,4.4,4.8),("B",4.2,4.6,5.4,5.8),("M",5.4,5.8,6,6.4),("A",6,6.4,6.6,7.2),("MA",6.6,7.2,10,10)]

inf = 100 #Infinito
# ----- Delanteros y Medios -------------- 

#Jug_PG ---> Promedio de Gol de Delantero y Medio
# MP = Muy poco; P = Poco; M = Medio; B = Bueno; A = Alto, MA = Muy Alto

Jug_PG = [("MP",0,0,0,0.1),("P",0,0.1,0.2,0.3),("M",0.2,0.3,0.4,0.5),("B",0.4,0.5,0.6,0.7),("A",0.6,0.7,0.9,1),("MA",0.9,1,inf,inf)]

#PGCR ---> Promedio de Goles en Contra del Rival
# MP = Muy poco; P = Poco; M = Medio; A = Alto; MA = Muy alto
PGCR = [("MP",0,0,0.2,0.4),("P",0.2,0.4,0.6,0.8),("M",0.6,0.8,1,1.2),("A",1,1.2,1.6,1.8),("MA",1.6,1.8,inf,inf)]

# ----- Defensores -------

#Def_PG ---> Promedio de Gol de Defensor
# P = Poco; M= Medio; A = Alto
Def_PG = [("P",0,0,0.1,0.2),("M",0.1,0.2,0.4,0.5),("A",0.4,0.5,inf,inf)]

#PGC ---> Promedio de Gol en Contra del equipo
# P = Poco; M = Medio; A = Alto; MA = Muy alto
PGC = [("P",0,0,0.4,0.7),("M",0.4,0.7,1,1.3),("A",1,1.3,1.6,1.9),("MA",1.6,1.9,inf,inf)]

#PVI ---> Promedio de Valla Invicta
# P = Poco; M = Medio; A = Alto; MA = Muy alto
PVI = [("P",0,0,0.1,0.2),("M",0.1,0.2,0.3,0.4),("A",0.3,0.4,0.6,0.7),("MA",0.6,0.7,1,1)]

#PGER ---> Promedio Gol Equipo Rival
# P = Poco; M= Medio; A = Alto
PGER = [("P",0,0,0.3,0.5),("M",0.3,0.5,0.8,1),("A",0.8,1,inf,inf)]

#PTA ---> Promedio Tarjetas Amarillas
# P = Poco; M= Medio; A = Alto
PTA = [("P",0,0,0.1,0.2),("M",0.1,0.2,0.3,0.4),("A",0.3,0.4,inf,inf)]


# ------ Arqueros -------
#Promedio Valla Invicta Arquero
# P = Poco; M= Medio; A = Alto; MA = Muy Alto
PVIA = [("P",0,0,0.2,0.3),("M",0.2,0.3,0.4,0.5),("A",0.4,0.5,0.6,0.8),("MA",0.6,0.8,1,1)]




def pertenencia_etiqueta (x,etiqueta):
		if not(x>=etiqueta[1] and x<=etiqueta[4]):
			return (etiqueta[0],False,0)
		
		elif x >= etiqueta[2] and x<= etiqueta[3]:
			return (etiqueta[0], True, 1 )
		
		elif x>= etiqueta[1] and x<etiqueta[2]:
			nivel_pertenencia = (1/(etiqueta[2]-etiqueta[1]))*(x-etiqueta[1])
			if nivel_pertenencia == 0:
				return (etiqueta[0], False,nivel_pertenencia)
			else: return (etiqueta[0], True,nivel_pertenencia)
		else: 
			nivel_pertenencia = (1/(etiqueta[4]-etiqueta[3]))*(etiqueta[4]-x)
			if nivel_pertenencia == 0:
				return (etiqueta[0], False,nivel_pertenencia)
			else: return (etiqueta[0], True,nivel_pertenencia)
			
def unif(ls):
	ls_ = []
	for s in VC:
		aux = filter(lambda x: s[0] == x[0], ls)
		if len(aux) <= 1:
			ls_=ls_ + aux
		else:
			max_ = max(map(lambda x: x[1],aux))
			ls_ = ls_ + [(s[0],max_)]
	return ls_

def buscarEti(s):
	for a in VC:
		if a[0] == s:
			return a



def centroProm(x):
	t = buscarEti(x[0])

	if not(x[0] == "NR") and not(x[0] == "MR") :
		
		if x[1] == 1:
			M = ((t[4]-t[1]) + (t[3]-t[2]) )/2.0
			return (M,t[1]+(t[4]-t[1])/2.0)
		else:
			x_ = (x[1] * (t[2]-t[1]))+t[1]
			M = ((t[4]-t[1]) + (t[3]-t[2]) + (2.0 * (t[2]-x_)) ) * (x[1]/2.0)
			
			return (M,t[1]+(t[4]-t[1])/2.0)
	elif x[0] == "NR":
		if x[1] == 1:
			M = ((t[4]-t[1]) + (t[3]-t[2]) )/2.0
			        #cm rectangulo eje x    # M rectangulo      # cm triangulo            #M tirangulo
			cx_= ( ((t[3]-t[1]) / 2.0 )    *  (t[3]-t[1]) )  +  ( (((t[4]-t[3]) / 3)+t[3]) *((t[4]-t[3]) / 2.0)     ) 
			cx = cx_ / ((t[3]-t[1]) + ((t[4]-t[3]) / 2.0))
			return (M,t[1]+cx)
		else:
			x_ = t[4]-(x[1] * (t[4]-t[3]) ) 
			M = (((t[4]-t[1]) + (t[3]-t[2]) + (x_ - t[3])) ) * (x[1]/2.0)
				#cm eje x rectang       #M rectangulo              #cm triangulo               #M triangulo
			cx_=  (((x_ - t[1])/2)     *   (x_ - t[1])*x[1] ) + ( (((t[4]- x_) / 3) + x_) *     (t[4]- x_) *x[1] /2         )
			cx = cx_ / ( ((x_ - t[1])*x[1]) +   ((t[4]- x_) *x[1] /2 ))
			return (M,t[1]+cx)
	else:
		if x[1] ==1:
			M = ((t[4]-t[1]) + (t[3]-t[2]) )/2.0
			        #cm rectangulo eje x                # M rectangulo            # cm triangulo            #M tirangulo
			cx_= ( ((t[2]-t[1])+((t[4]-t[2]) / 2.0 ) )   *  (t[4]-t[2]) )  +  ( (2.0*((t[2]-t[1]) / 3.00)) *((t[2]-t[1]) / 2.0)     )
			cx = cx_ / ((t[4]-t[2]) + ((t[2]-t[1]) / 2.0))
			return (M,t[1]+cx)
		else:
			x_ = (x[1] * (t[2]-t[1]))+t[1]
			M = ((t[4]-t[1]) + (t[3]-t[2]) + (2.0 * (t[2]-x_)) ) * (x[1]/2.0)
				#cm eje x rectang       #M rectangulo              #cm triangulo               #M triangulo
			cx_=  (((x_-t[1])+((t[4]-x_)/2) )    *   (t[4]-x_)*x[1] ) + ( (2* ((x_-t[1]) / 3) ) *     (x_ - t[1]) *x[1] /2         )
			cx = cx_ / ( ((t[4]-x_)*x[1]) +   ((x_ - t[1]) *x[1] /2 ))
			return (M,t[1]+cx)
			
			
			
def tnorm(ls):
	return (min (ls))



def defuzzificar(conj):
	centrosProm = map (lambda x: centroProm (x) ,conj)
	if len(centrosProm) == 1 :
		return centrosProm[0][1]
	else:
		 Mtotal = 0.0
		 sumatoria = 0.0
		 for x in centrosProm:
			Mtotal += x[0]
			sumatoria += (x[0]*x[1])
			
		 if Mtotal == 0:	
			return 0 
		 else:
			 return sumatoria / Mtotal
	
	

			
def calculoDelantero(promClarin, promGol,promGCR ):
		
		
		conjPC = filter(lambda x: x[1],map(lambda et: pertenencia_etiqueta (promClarin,et),PC))
		conjPG = filter(lambda x: x[1],map(lambda et: pertenencia_etiqueta (promGol,et),Jug_PG))
		conjPGCR = filter(lambda x: x[1],map(lambda et: pertenencia_etiqueta (promGCR,et),PGCR))
		
		conjVC=[]
		for a in conjPC:
			for b in conjPG:
				for c in conjPGCR:
					for dd in reglasDelanteros.reglDel:
						if (a[0] == dd[0]) and (b[0] == dd[1]) and (c[0] == dd[2]):
							 conjVC.append( (dd[3] , tnorm([a[2],b[2],c[2]])) )
		
		conjVC_ = unif(conjVC)
		
		return defuzzificar( conjVC_)
		
def calculoMedio(promClarin, promGol,promGCR ):
		
		
		conjPC = filter(lambda x: x[1],map(lambda et: pertenencia_etiqueta (promClarin,et),PC))
		conjPG = filter(lambda x: x[1],map(lambda et: pertenencia_etiqueta (promGol,et),Jug_PG))
		conjPGCR = filter(lambda x: x[1],map(lambda et: pertenencia_etiqueta (promGCR,et),PGCR))
		
		conjVC=[]
		for a in conjPC:
			for b in conjPG:
				for c in conjPGCR:
					for dd in reglasMedios.reglMed:
						if (a[0] == dd[0]) and (b[0] == dd[1]) and (c[0] == dd[2]):
							 conjVC.append( (dd[3] , tnorm([a[2],b[2],c[2]])) )
		
		conjVC_ = unif(conjVC)
		
		return defuzzificar( conjVC_)






		
def calculoDefensor(promClarin, promGol, promGC, promVI,promGER, promTA):
		
		conjPC = filter(lambda x: x[1],map(lambda et: pertenencia_etiqueta (promClarin,et),PC))
		conjPG = filter(lambda x: x[1],map(lambda et: pertenencia_etiqueta (promGol,et),Def_PG))
		conjPGC = filter(lambda x: x[1],map(lambda et: pertenencia_etiqueta (promGC,et),PGC))
		conjPVI = filter(lambda x: x[1],map(lambda et: pertenencia_etiqueta (promVI,et),PVI))
		conjPGER = filter(lambda x: x[1],map(lambda et: pertenencia_etiqueta (promGER,et),PGER))
		conjPTA = filter(lambda x: x[1],map(lambda et: pertenencia_etiqueta (promTA,et),PTA))
		
		conjVC=[]
		for a in conjPC:
			for b in conjPG:
				for c in conjPGC:
					for d in conjPVI:
						for e in conjPGER:
							for f in conjPTA:
								for gg in reglasDefensores.reglDef:
									if (a[0] == gg[0] and b[0] == gg[1] and c[0] == gg[2] and d[0] == gg[3] and e[0] == gg[4] and f[0] == gg[5] ):		
										conjVC.append((gg[6], tnorm ([a[2],b[2],c[2],d[2],e[2],f[2]])))
		
		conjVC_ = unif(conjVC)
		
		return defuzzificar(conjVC_)	
			
def calculoArquero(promClarin, promVI,promPGER ):
		
		
		conjPC = filter(lambda x: x[1],map(lambda et: pertenencia_etiqueta (promClarin,et),PC))
		conjPVI = filter(lambda x: x[1],map(lambda et: pertenencia_etiqueta (promVI,et),PVIA))
		conjPGER = filter(lambda x: x[1],map(lambda et: pertenencia_etiqueta (promPGER,et),PGER))
		
		conjVC=[]
		for a in conjPC:
			for b in conjPVI:
				for c in conjPGER:
					for dd in reglasArqueros.reglArq:
						if (a[0] == dd[0]) and (b[0] == dd[1]) and (c[0] == dd[2]):
							 conjVC.append( (dd[3] , tnorm([a[2],b[2],c[2]])) )
		
		conjVC_ = unif(conjVC)
		
		return defuzzificar( conjVC_)


















