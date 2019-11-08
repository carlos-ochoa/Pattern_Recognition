import math

class ClasificadorMetricas:

    listaEntrenamiento = []
    listaClasificados = []
    patronesRepresentativos = []
    metrica = 0
    clases = 0

    def __init__(self,listaEntrenamiento,metrica,clases):
        self.listaEntrenamiento = listaEntrenamiento
        self.metrica = metrica
        self.clases = clases

    def calcularPatronRepresentativo(self):
        r = 0
        patronRepresentativo = []
        for clase in self.listaEntrenamiento:
            #print("Clase " + str(clase) + "\n")
            for rasgo in range(0,3):
                for patron in clase:
                    r += patron[rasgo]
                r = round(r / len(clase),1)
                patronRepresentativo.append(r)
                r = 0
            #patronRepresentativo.clear()
            print("Pat rep " + str(patronRepresentativo))
            self.patronesRepresentativos.append(patronRepresentativo.copy())
            patronRepresentativo.clear()

        #print("Patrones representativos " + str(self.patronesRepresentativos))

    def calcularDistancias(self,listaRecuperacion):
        diferencia = 0
        suma = 0
        distancia = 0
        diferencias = []
        distanciaPatron = []
        distanciaPatrones = []
        #print("patronesRepresentativos " + str(self.patronesRepresentativos))
        for patron in listaRecuperacion:
            for pr in self.patronesRepresentativos:
                for rasgo in range(0,3):
                    # Correspondiente a City Block y distancia a infinito
                    if self.metrica == 1:
                        diferencia = abs(patron[rasgo] - pr[rasgo])
                    # Distancia Euclidiana
                    elif self.metrica == 2:
                        diferencia = abs((patron[rasgo] - pr[rasgo])**2)
                    # Distancia a infinito
                    elif self.metrica == 3:
                        diferencia = abs(patron[rasgo] - pr[rasgo])
                        diferencias.append(diferencia)
                    #print("\nDiferencia " + str(diferencia))
                    suma += diferencia
                #distanciaPatron.append(suma)
                # Volvemos a hacer la adecuación de los valores de las distancias para obtener la distancia real
                if self.metrica == 1:
                    distancia = round(suma,1)
                elif self.metrica == 2:
                    distancia = round(math.sqrt(suma),1)
                elif self.metrica == 3:
                    distancia = round(max(diferencias),1)
                suma = 0
                diferencias.clear()
                distanciaPatron.append(distancia)

            #print(str(distanciaPatron))
            distanciaPatrones.append(distanciaPatron.copy())
            distanciaPatron.clear()
        return distanciaPatrones

    def clasificarPatrones(self,listaRecuperacion):
        patronClasificado = []
        patronAux = []
        patron = 0
        # Primero calculamos las distancias de cada punto a los patrones representativos
        distancias = self.calcularDistancias(listaRecuperacion)
        # Ahora colocamos los criterios de clasificación
        # x pertenece a Cj si dj < di
        for par in distancias:
            patronAux = listaRecuperacion[patron]
            if par[0] <= par[1]:
                print("Distancia 0 " + str(par[0]) + " distancia 1 " + str(par[1]) + " CLASE 0")
                patronAux.append(1)
            else:
                print("Distancia 0 " + str(par[0]) + " distancia 1 " + str(par[1]) + " CLASE 1")
                patronAux.append(2)
            patron += 1
            self.listaClasificados.append(patronAux)
        return self.listaClasificados
