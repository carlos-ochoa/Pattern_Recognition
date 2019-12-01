import numpy as np
import random

class Lernmatrix:
    clases = [] # Lista de arrays de numpy
    patronesFundamentales = [] # Lista de arrays de numpy

    def __init__(self,clases,patronesFundamentales):
        self.clases = clases
        self.patronesFundamentales = patronesFundamentales

    def crearMatriz(self):
        clase = 0
        patron = 0
        j = 0
        # Primero creamos nuestra matriz de ceros
        M = np.zeros([len(self.clases),len(self.patronesFundamentales[0])])
        # Para cada patrón representativo iteramos y actualizamos la matriz
        for p in self.patronesFundamentales:
            for indice in p:
                if self.clases[clase][clase] != indice:
                    M[clase][j] -= 1
                else:
                    M[clase][j] += 1
                j += 1
            clase += 1
            j = 0
        # Retornamos la matriz final lista para recuperación
        return M

    def verificarClase(self,patron):
        mayores = 0
        clase = 0
        patronClase = [0,0,0]
        valorMayor = np.amax(patron)
        # AHora vemos si se repite varias veces este valor maximo en el patron
        indices = np.where(patron == valorMayor)[0]
        for j in indices:
            patronClase[j] = 1
        # Si el tamaño de indices es superior a 1 no se puede clasificar
        if len(indices) > 1:
            clase = -1
        else: clase = indices[0]
        return (clase,patronClase)

    def recuperarPatrones(self,M,patrones):
        i = 0
        clasesAsignadas = []
        print("Fase de recuperación:\n")
        for i in range(len(self.clases)):
            # Hacemos la multiplicación M . patron
            resultado = M.dot(patrones[i])
            # Ahora verificamos en la clase a la que pertenece
            clase = self.verificarClase(resultado)
            if clase[0] != -1:
                print(str(M) + "." + str(patrones[i]) + " = " + str(resultado) + " = " + str(self.clases[clase[0]]) + " Asociado a clase " + str(clase[0]) + "\n")
            else:
                print(str(M) + "." + str(patrones[i]) + " = " + str(resultado) + " = " + str(clase[1]) + " No se puede asociar a una clase" + "\n")
            # Colocamos la clase en una lista
            clasesAsignadas.append(clase)
        return clasesAsignadas

    # patron -> Patrón al que se le va a introducir ruido
    # porcentaje -> a cuántos bits se les introduce ruido
    # tipo -> tipo de ruido
    def introducirRuido(self,patron,porcentaje,tipo):
        i = 0
        porcentajeRuido = porcentaje / len(patron)
        while i < porcentaje:
            posicion = random.randint(0,len(patron)-1)
            # Si el tipo de ruido es aditivo
            if tipo == 1:
                if patron[posicion] == 0:
                    patron[posicion] = 1
                    i += 1
            # Si es ruido sustractivo
            elif tipo == 2:
                if patron[posicion] == 1:
                    patron[posicion] = 0
                    i += 1
            # Si es ruido mixto
            elif tipo == 3:
                if patron[posicion] == 0:
                    patron[posicion] = 1
                    i += 1
                elif patron[posicion] == 1:
                    patron[posicion] = 0
                    i += 1
        return (patron,porcentajeRuido)
