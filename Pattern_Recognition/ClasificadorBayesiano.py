import numpy as np
import math

class ClasificadorBayesiano:

    clases = 0
    listaEntrenamiento = []
    rasgosEvaluacion = ()
    probabilidadesClases = []
    tablaProbabilidades = []
    listaClasificados = []
    valores = []

    '''
        Parámetros del constructor:
            listaEntrenamiento => Se trata de la lista con las clases clasificadas para entrenar al modelo
            cardinalidades => Lista que contiene las cardinalidades de las clases a clasificar
            rasgoEvaluacion => Es una lista que indica los rasgos que se tomarán en cuenta para el entrenamiento
    '''
    def __init__(self,listaEntrenamiento,cardinalidades,rasgosEvaluacion,clases):
        self.listaEntrenamiento = listaEntrenamiento
        self.cardinalidades = cardinalidades
        self.rasgosEvaluacion = rasgosEvaluacion
        self.clases = clases

    def calcularProbabilidadesClases(self):
        probabilidadClase0 = self.cardinalidades[1] / self.cardinalidades[0]
        probabilidadClase1 = self.cardinalidades[2] / self.cardinalidades[0]
        #probabilidadClase2 = self.cardinalidades[3] / self.cardinalidades[0]
        self.probabilidadesClases.append(probabilidadClase0)
        self.probabilidadesClases.append(probabilidadClase1)
        #self.probabilidadesClases.append(probabilidadClase2)

    def calcularDistribucionesCondicionales(self):
        cardinalidadValor = 0
        probabilidad = 0.0
        tablaProbabilidad = [[],[],[]]
        rasgos = []
        # Solo para propositos de analisis
        for rasgo in self.rasgosEvaluacion:
            for c in range(0,self.clases):
                for patron in self.listaEntrenamiento[c]:
                    rasgos.append(patron[rasgo])
        # Generamos el espectro de valores posibles del rasgo a evaluar
        self.valores = [round(v*0.1,1) for v in range(40,80)]
        # Para cada rasgo a tomar en cuenta crearemos su tabla de probabilidad condicional
        for rasgo in self.rasgosEvaluacion:
            # Iteramos unicamente sobre las tres clases que vamos a clasificar
            for c in range(0,self.clases):
                # Vamos a clasificar según el valor del estudio que se consiguió del billete
                # Sabemos entonces que hay solo 5 valores posibles (0-4)
                for i in self.valores:
                    for patron in self.listaEntrenamiento[c]:
                        #print("\nRasgo " + str(patron[rasgo]) +  " valor " + str(i))
                        if patron[rasgo] == i:
                            cardinalidadValor += 1
                            #print("\nValor de rasgo encontrado " + str(patron[rasgo]) + " van " + str(cardinalidadValor))
                    probabilidad = cardinalidadValor / len(self.listaEntrenamiento[c])
                    tablaProbabilidad[c].append(round(probabilidad,5))
                    cardinalidadValor = 0
        self.tablaProbabilidades = tablaProbabilidad

    def clasificarPatrones(self,listaRecuperacion):
        decisiones = []
        cont = 0
        rasgo = 0
        sum = 0
        print("Probabilidades: " + str(self.tablaProbabilidades))
        print("\nOtro gato " + str(self.probabilidadesClases))
        print("\nValores: " + str(self.valores))
        for patron in listaRecuperacion:
            r = patron[0]
            # Idea, esto puede ser busqueda binaria para más velocidad
            for v in self.valores:
                if v == r:
                    #print("\nValor encontrado " + str(v) + " con rasgo " + str(r))
                    rasgo = cont
                    break
                #else:
                    #print("\nValor no encontrado " + str(r))
                cont += 1
            cont = 0
            for clase in range(0,self.clases):
                if self.probabilidadesClases[clase] == 0 and self.tablaProbabilidades[clase][rasgo] == 0:
                    decision = 0
                elif self.probabilidadesClases[clase] != 0 and self.tablaProbabilidades[clase][rasgo] == 0:
                    decision = math.log(self.probabilidadesClases[clase])
                elif self.probabilidadesClases[clase] == 0 and self.tablaProbabilidades[clase][rasgo] != 0:
                    decision = math.log(self.tablaProbabilidades[clase][rasgo])
                else:
                    decision = math.log(self.probabilidadesClases[clase]) + math.log(self.tablaProbabilidades[clase][rasgo])
                decisiones.append(decision)
            print("\nPromedio Clase 0 " + str(decisiones[0]) + "  y promedio Clase1  " + str(decisiones[1]))
            if decisiones[0] >= decisiones[1] :
                patron.append(1)
            elif decisiones[1] >= decisiones[0] :
                patron.append(2)
            elif decisiones[2] >= decisiones[0]:
                patron.append(3)
            decisiones.clear()
            self.listaClasificados.append(patron)
        return self.listaClasificados
