class Estadisticas:
    archivoSalida = ""
    listaClasificados = []
    cantidadPatrones = 0
    listaComparacion = []
    archivoComparacion = ""
    precision = 0
    accuracy = 0
    recall = 0
    tp,fp,tn,fn = 0,0,0,0

    def __init__(self,archivoSalida,listaClasificados,archivoComparacion):
        self.archivoSalida = archivoSalida
        self.listaClasificados = listaClasificados
        self.archivoComparacion = archivoComparacion

    def leerArchivoComparacion(self):
        archivo = open(self.archivoComparacion,"r")
        for linea in archivo:
            patron = linea.split(",")
            patron = [round(float(rasgo),1) for rasgo in patron]
            self.listaComparacion.append(patron)
        archivo.close()
        self.cantidadPatrones = len(self.listaComparacion)

    def generarMatrizConfusion(self, clasificador):
        if clasificador == 3:
            index = 2
        else: index = 4
        for patron in range(0,len(self.listaClasificados)):
            print(str(self.listaClasificados[patron]) + "   " + str(self.listaComparacion[patron]))
            if self.listaClasificados[patron][index] == 1 and self.listaComparacion[patron][4] == 1:
                self.tp += 1
            elif self.listaClasificados[patron][index] == 1 and self.listaComparacion[patron][4] == 2:
                self.fp += 1
            elif self.listaClasificados[patron][index] == 2 and self.listaComparacion[patron][4] == 1:
                self.fn += 1
            else:
                self.tn += 1
        print("TP " + str(self.tp) + "\tFP " + str(self.fp) + "\nFN " + str(self.fn) + "\tTN " + str(self.tn))
        self.precision = self.tp / (self.tp + self.fp)
        self.recall = self.tp / (self.tp + self.fn)
        self.accuracy = (self.tp + self.tn) / (self.tp + self.tn + self.fp + self.fn)
        print("Precision " + str(self.precision) + "  recall  " + str(self.recall) + "  accuracy  " + str(self.accuracy))
