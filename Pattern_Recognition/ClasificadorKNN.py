import math

class ClasificadorKNN:
    listaEntrenamiento = []
    listaClasificados = []
    metrica = 0
    clases = 0
    desempate = 0
    k = 0

    def __init__(self,listaEntrenamiento,k,desempate):
        self.listaEntrenamiento = listaEntrenamiento
        self.k = k
        self.desempate = desempate

    def calcularDistancias(self,patronEvaluacion,lEntrenamiento):
        diferencia = 0
        suma = 0
        distanciaPatrones = []
        for patron in lEntrenamiento:
            for rasgo in range(0,3):
                print("patron " + str(patron) + "  PATRON ECA " + str(patronEvaluacion))
                diferencia = abs((patron[rasgo] - patronEvaluacion[rasgo])**2)
                suma += diferencia
            distancia = round(math.sqrt(suma),1)
            suma = 0
            # Clase, distancia
            datosPatron = (patron[4],distancia)
            distanciaPatrones.append(datosPatron)
        distanciaPatrones.sort(key=lambda tup:tup[1])
        return distanciaPatrones

    def asignarClase(self,distanciaPatrones):
        clase1, clase2 = 0 , 0
        for i in range(0,self.k):
            if distanciaPatrones[i][0] == 1:
                clase1 += 1
            elif distanciaPatrones[i][0] == 2 :
                clase2 += 1
        return (clase1,clase2)

    def desempatar(self,distanciaPatrones,clases):
        clase = 0
        distanciaTotal1, distanciaTotal2 = 0,0
        # Si el desempate es por distancia media
        if self.desempate == 1:
            for i in range(0,self.k):
                if distanciaPatrones[i][0] == 1:
                    distanciaTotal1 += distanciaPatrones[i][1]
                elif distanciaPatrones[i][0] == 2:
                    distanciaTotal2 += distanciaPatrones[i][1]
            try:
                d1 = distanciaTotal1 / clases[0]
            except ZeroDivisionError:
                d1 = 0
            try:
                d2 = distanciaTotal2 / clases[1]
            except ZeroDivisionError:
                d2 = 0
            clase = 1 if d1 > d2 else 2
        # Si el desempate es por pesado de casos
        elif self.desempate == 2:
            for i in range(0,self.k):
                if distanciaPatrones[i][0] == 1:
                    try:
                        distanciaTotal1 += 1 / distanciaPatrones[i][1]
                    except ZeroDivisionError:
                        pass
                elif distanciaPatrones[i][0] == 2:
                    try:
                        distanciaTotal2 += distanciaPatrones[i][1]
                    except ZeroDivisionError: pass
                clase = 1 if distanciaTotal1 > distanciaTotal2 else 2
        return clase

    def clasificar(self,listaRecuperacion):
        claseAsignada = 0
        lEntrenamiento = []
        for clase in self.listaEntrenamiento:
            lEntrenamiento += clase
        for patron in listaRecuperacion:
            distanciaPatrones = self.calcularDistancias(patron,lEntrenamiento)
            clases = self.asignarClase(distanciaPatrones)
            if self.desempate == 3:
                if clases[0] > clases[1]:
                    claseAsignada = 1
                elif clases[0] < clases[1]:
                    claseAsignada = 2
            else:
                claseAsignada = self.desempatar(distanciaPatrones,clases)
            patron.append(claseAsignada)
            lEntrenamiento.append(patron.copy())
            self.listaClasificados.append(patron.copy())
        return self.listaClasificados
