class ManejadorArchivos:
    listaEntrenamiento = []
    listaRecuperacion = []
    cardinalidades = []
    clases = 0
    def __init__(self,archivo,archivoR,archivoC,clases):
        self.archivoEntrenamiento = archivo
        self.archivoRecuperacion = archivoR
        self.archivoClasificados = archivoC
        self.clases = clases
        #self.rasgos = rasgos # Rasgos es una tupla que nos indica qué rasgos tomaremos en cuenta
        # Lo anterior solo es temporal, luego lo pongo mejor

    def getListaEntrenamiento(self):
        return self.listaEntrenamiento

    def getListaRecuperacion(self):
        return self.listaRecuperacion

    def getCardinalidades(self):
        return self.cardinalidades

    def getClasses(self):
        return self.clases

    def setListaRecuperacion(self,lista):
        self.listaRecuperacion = lista

    # Creamos el método que permite leer los datos del archivo de entrada
    def leerArchivo(self):
        clases = []
        claseActual = []
        for n in range(0,self.clases):
            clases.append(claseActual.copy())
        print(str(clases))
        # Sabemos desde un inicio que este clasificador es biclase
        totalClases = 0
        # Abrimos el archivo en modo lectura
        arcLectura = open(self.archivoEntrenamiento,"r")
        # Primero hacemos el tratamiento del dataset con Pandas
        # Ordenamos las filas según la clase a la que pertenecen
        # Iteramos y por cada fila construimos el vector de características de nuestros patrones
        for linea in arcLectura:
            # Separamos utilizando las comas para crear una lista preliminar de nuestro patron
            patron = linea.split(",")
            # Convertimos todos los rasgos del patrón a enteros
            patron = [round(float(rasgo),1) for rasgo in patron]
            patron = tuple(patron)
            # Como el sistema es biclase separamos directamente las clases en dos listas distintas
            # El rasgo 6 nos indica en qué clase se encuentra clasificado el patrón
            if patron[4] == 1.0:
                #print("Insertando a clase 0")
                clases[0].append(patron)
            elif patron[4] == 2.0:
                #print("Insertando a clase 1")
                clases[1].append(patron)
            else:
                clases[2].append(patron)
        # Colocamos cada clase dentro de la lista de entrenamiento
        for n in clases:
            self.listaEntrenamiento.append(n)
        #self.listaEntrenamiento.append(clases[0])
        #self.listaEntrenamiento.append(clase1)
        #self.listaEntrenamiento.append(clase2)
        tam = 0
        for n in clases:
            tam += len(n)
        self.cardinalidades.append(tam)
        #self.cardinalidades.append(len(clase0)+len(clase1))
        for n in clases:
            self.cardinalidades.append(len(n))
        #self.cardinalidades.append(len(clase0))
        #self.cardinalidades.append(len(clase1))

        #for clase in self.listaEntrenamiento:
        #    for patron in clase:
        #        print(str(patron) + '\n')
        #print("Cardinalidades: " + str(len(clase0)) + " ==== " + str(len(clase1)))
        arcLectura.close()

    # Creamos el método que permite leer los patrones para testeo
    def leerArchivoRec(self):
        # Abrimos el archivo en modo lectura
        arcLectura = open(self.archivoRecuperacion,"r")
        # Primero hacemos el tratamiento del dataset con Pandas
        # Ordenamos las filas según la clase a la que pertenecen
        # Iteramos y por cada fila construimos el vector de características de nuestros patrones
        for linea in arcLectura:
            # Separamos utilizando las comas para crear una lista preliminar de nuestro patron
            patron = linea.split(",")
            patron = [round(float(i),1) for i in patron]
            #print(str(patron) + '\n')
            # Colocamos cada patron ingresado dentro de la lista de entrenamiento
            self.listaRecuperacion.append(patron)
        arcLectura.close()

    # Creamos el archivo de salida con los clasificados
    # Recibe como parametros
    def escribirArchivo(self,listaClasificados):
        # Abrimos un archivo de modo escritura
        arcEscritura = open(self.archivoClasificados,"w")
        # Iteramos y por cada fila construimos el vector de características de nuestros patrones
        for patron in listaClasificados:
            cadena = ""
            i = 0
            for elemento in patron:
                if i == len(patron)-1:
                    cadena += str(elemento)
                else:
                    cadena += str(elemento) + ","
                i += 1
            arcEscritura.write(cadena + '\n')
        arcEscritura.close()
