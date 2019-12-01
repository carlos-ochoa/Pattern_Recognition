import numpy as np

class ClasificadorBayesianoNormal:

    listaClasificados = []
    listaEntrenamiento = []
    patronesRepresentativos = []
    discriminanteCoordenada = []
    puntosPase = []
    parametrosEcuacion = [] # 0 - x, 1 - x, 2 - bias

    def __init__(self,listaEntrenamiento):
        self.listaEntrenamiento = listaEntrenamiento

    def getDiscriminanteCoordenada(self):
        return self.discriminanteCoordenada

    def getPuntosPase(self):
        return self.puntosPase

    def getParametrosEcuacion(self):
        return self.parametrosEcuacion

    def calcularPatronRepresentativo(self):
        r = 0
        x = 0
        patronRepresentativo = []
        for clase in self.listaEntrenamiento:
            for rasgo in range(0,2):
                for patron in clase:
                    r += patron[rasgo]
                    if rasgo == 0:
                        x += patron[0]
                r = round(r / len(clase),1)
                #print("r " + str(r))
                patronRepresentativo.append(r)
                r = 0
            x = round(x / len(clase),1)
            self.parametrosEcuacion.append(x)
            x = 0
            self.patronesRepresentativos.append(patronRepresentativo.copy())
            patronRepresentativo.clear()

    def calcularDiscriminante(self):
        # Generamos un solo discriminante por ser biclase el clasificador, luego lo hago más general
        # Convertimos los vectores a matrices de numpy
        print("dif0   " + str(np.array(self.patronesRepresentativos[0])) + "   dif1   " + str(np.array(self.patronesRepresentativos[1])))
        diferencia = np.array(self.patronesRepresentativos[0]) - np.array(self.patronesRepresentativos[1])
        b = (self.parametrosEcuacion[0] - self.parametrosEcuacion[1]) * (self.parametrosEcuacion[0] + self.parametrosEcuacion[1])
        b /= 2
        suma = np.array(self.patronesRepresentativos[0]) + np.array(self.patronesRepresentativos[1])
        bias = diferencia.transpose().dot(suma) / 2
        print("diferencia " + str(diferencia) + " suma " + str(suma) + " bias " + str(bias))
        self.discriminanteCoordenada = [diferencia,bias]
        self.parametrosEcuacion.append(b)

    def clasificarPatrones(self,listaRecuperacion):
        for patron in listaRecuperacion:
            patronA = patron[0:2]
            d = self.discriminanteCoordenada[0].transpose().dot(patronA) - self.discriminanteCoordenada[1]
            if len(self.puntosPase) <= 2:
                print("pA d " + str(patronA[0]) + "  " + str(d))
                coordenada = [patronA[0],d]
                self.puntosPase.append(coordenada.copy())
            if d >= 0:
                patronA.append(1)
            else:
                patronA.append(2)
            self.listaClasificados.append(patronA)
        self.discriminanteCoordenada[0] = self.discriminanteCoordenada[0].sum()
        return self.listaClasificados
