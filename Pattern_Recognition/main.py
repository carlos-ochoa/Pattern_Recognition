import ManejadorArchivos as ma
import ClasificadorBayesiano as cb
import ClasificadorMetricas as cm
import ClasificadorBayesianoNormal as cbn
import ClasificadorKNN as ckn
import Lernmatrix as lm
import Estadisticas as e
import matplotlib.pyplot as plt
import numpy as np

'''
    Autor: Carlos Armando Ochoa Ginera
    Descripción: Software que hace uso de clasificadores probabilísticos-estadísticos y basados
                 en métricas con el objetivo de clasificar si un tumor encontrado en una mamografía es
                 benigno o maligno.
    Atributos:
        BI-RADS, edad, forma, contorno, densidad
'''

def graficarClasificados(listaClasificados):
    coordenadasXClase0, coordenadasYClase0 = [],[]
    coordenadasXClase1, coordenadasYClase1 = [],[]
    paresCoordenadas = []
    for patron in listaClasificados:
        #print(str(patron) + '\n')
        if patron[4] == 0.0:
            coordenadasXClase0.append(patron[0])
            coordenadasYClase0.append(patron[1])
        else:
            coordenadasXClase1.append(patron[0])
            coordenadasYClase1.append(patron[1])
    plt.scatter(coordenadasXClase0, coordenadasYClase0, alpha=0.3, c="orange")
    plt.scatter(coordenadasXClase1, coordenadasYClase1, alpha=0.3, c="blue")
    plt.show()


def graficar(listaEntrenamiento,listaClasificados,clas,discriminante = [],puntosPase = []):
    if clas == 3:
        index = 2
    else : index = 4
    coordenadasXClase0, coordenadasYClase0 = [],[]
    coordenadasXClase1, coordenadasYClase1 = [],[]
    paresCoordenadas = []
    for clase in listaEntrenamiento:
        for patron in clase:
            #print(str(patron) + '\n')
            if patron[4] == 1:
                coordenadasXClase0.append(patron[0])
                coordenadasYClase0.append(patron[1])
            elif patron[4] == 2:
                coordenadasXClase1.append(patron[0])
                coordenadasYClase1.append(patron[1])
    coordenadasXCClase0, coordenadasYCClase0 = [],[]
    coordenadasXCClase1, coordenadasYCClase1 = [],[]
    paresCoordenadas = []
    for patron in listaClasificados:
            #print(str(patron) + '\n')
        if patron[index] == 1.0:
            coordenadasXCClase0.append(patron[0])
            coordenadasYCClase0.append(patron[1])
        elif patron[index] == 2.0:
            coordenadasXCClase1.append(patron[0])
            coordenadasYCClase1.append(patron[1])
    if clas == 3:
        # Graficamos la recta discriminante
        print("D0 " + str(discriminante[0]) + "  D1  " + str(discriminante[1]))
        #recta = [discriminante[0]*i - discriminante[1] for i in x]
        #plt.plot(x,recta)
        #plt.plot([0,discriminante[1]],[10,discriminante[1]-6])
        x = np.linspace(4.5,7.5,100)
        y = abs(puntosPase[0] - puntosPase[1])*x - puntosPase[2]
        print("PUNTOS " + str(puntosPase[0]) + "," + str(puntosPase[1]) + "  " + str(puntosPase[2]))
        plt.plot([4.5,6.5],[2,4.5],color="purple",label="Discriminante")
        #plt.plot(puntosPase[0],puntosPase[1])
    plt.scatter(coordenadasXClase0, coordenadasYClase0, alpha=0.3, c="orange", label="Entrenamiento")
    plt.scatter(coordenadasXClase1, coordenadasYClase1, alpha=0.3, c="blue",label="Entrenamiento")
    plt.scatter(coordenadasXCClase0, coordenadasYCClase0, alpha=0.3, c="red",label="Iris Cetosa")
    plt.scatter(coordenadasXCClase1, coordenadasYCClase1, alpha=0.3, c="green",label="Iris versicolor")
    plt.legend(loc = 1)
    plt.xlim(4,7.5)
    plt.ylim(1.5,4.5)
    plt.show()



def main():
    print("Bienvenido a la versión beta de los clasificadores\n")
    print("Los patrones de entrenamiento del clasificador se leen desde mammographic_masses.data\n")
    print("Los patrones de recuperación del clasificador se leen desde data-rec.data\n")
    print("El caso de estudio es determinar si un tumor encontrado en la mama es benigno o maligno\n")
    print("Dataset proporcionado por M. Elter, R. Schulz-Wendtland and T. Wittenberg (2007)\nThe prediction of breast cancer biopsy outcomes using two CAD approaches that both emphasize an intelligible decision process.\nMedical Physics 34(11), pp. 4164-4172\n")
    print("El dataset original cuenta con 961 patrones, de los cuales se tomaron 66% (634) para entrenamiento y el resto para recuperacion\n ")
    print("Selecciona qué clasificador deseas utilizar\n")
    print("1.- Clasificador Bayesiano\n2.-Clasificador basado en métricas\n3.-Clasificador para distribuciones normales\n4.-Clasificador Knn\n")
    print("5.- Memoria asociativa (No usa el dataset habitual)\n")
    clas = int(input())
    if clas == 1:
        # Primero cargamos los archivos
        manejador = ma.ManejadorArchivos("iris1.csv","iris-rec1.csv","resultadosBayes.txt",2)
        manejador.leerArchivo()
        manejador.leerArchivoRec()
        listaEntrenamiento = manejador.getListaEntrenamiento()
        clasificador = cb.ClasificadorBayesiano(listaEntrenamiento,manejador.getCardinalidades(),[0],2)
        clasificador.calcularProbabilidadesClases()
        clasificador.calcularDistribucionesCondicionales()
        listaRecuperacion = manejador.getListaRecuperacion()
        listaClasificados = clasificador.clasificarPatrones(listaRecuperacion)
        manejador.escribirArchivo(listaClasificados)
        # Generamos una gráfica con los datos de entrenamiento
        estadisticas = e.Estadisticas("matrizBay.txt",listaClasificados,"iris-comp1.csv")
        estadisticas.leerArchivoComparacion()
        estadisticas.generarMatrizConfusion(1)
        graficar(listaEntrenamiento,listaClasificados,clas,[])
        #graficarClasificados(listaClasificados)
    if clas == 2:
        # Primero cargamos los archivos
        manejador = ma.ManejadorArchivos("iris1.csv","iris-rec1.csv","resultadosMetricas.txt",2)
        manejador.leerArchivo()
        manejador.leerArchivoRec()
        listaEntrenamiento = manejador.getListaEntrenamiento()
        print("\nIndica la métrica con la que quieres evaluar:")
        print("\n1.-CityBlock")
        print("\n2.-Euclidia")
        print("\n3.-Infinito\n")
        metrica = int(input())
        clasificador = cm.ClasificadorMetricas(listaEntrenamiento,metrica,2)
        clasificador.calcularPatronRepresentativo()
        listaRecuperacion = manejador.getListaRecuperacion()
        listaClasificados = clasificador.clasificarPatrones(listaRecuperacion)
        #print("listaClasificados " + str(listaClasificados))
        manejador.escribirArchivo(listaClasificados)
        # Generamos una gráfica con los datos de entrenamiento
        estadisticas = e.Estadisticas("matrizMet.txt",listaClasificados,"iris-comp1.csv")
        estadisticas.leerArchivoComparacion()
        estadisticas.generarMatrizConfusion(2)
        graficar(listaEntrenamiento,listaClasificados,clas,[])
        #graficarClasificados(listaClasificados)
    if clas == 3:
        # Primero cargamos los archivos
        manejador = ma.ManejadorArchivos("iris1.csv","iris-rec1.csv","resultadosNormal.txt",2)
        manejador.leerArchivo()
        manejador.leerArchivoRec()
        listaEntrenamiento = manejador.getListaEntrenamiento()
        clasificador = cbn.ClasificadorBayesianoNormal(listaEntrenamiento)
        clasificador.calcularPatronRepresentativo()
        clasificador.calcularDiscriminante()
        listaRecuperacion = manejador.getListaRecuperacion()
        listaClasificados = clasificador.clasificarPatrones(listaRecuperacion)
        manejador.escribirArchivo(listaClasificados)
        discriminante = clasificador.getDiscriminanteCoordenada()
        puntos = clasificador.getParametrosEcuacion()
        estadisticas = e.Estadisticas("matrizNormal.txt",listaClasificados,"iris-comp1.csv")
        estadisticas.leerArchivoComparacion()
        estadisticas.generarMatrizConfusion(3)
        graficar(listaEntrenamiento,listaClasificados,clas,discriminante,puntos)
    if clas == 4:
        manejador = ma.ManejadorArchivos("iris1.csv","iris-rec1.csv","resultadosNormal.txt",2)
        manejador.leerArchivo()
        manejador.leerArchivoRec()
        listaEntrenamiento = manejador.getListaEntrenamiento()
        print("Digite el valor de K\n")
        k = int(input())
        print("Indique el metodo de desempate a utilizar\n")
        print("1.-Por distancia media\n2.-Por pesado de casos\n3.-Normal\n")
        desempate = int(input())
        clasificador = ckn.ClasificadorKNN(listaEntrenamiento,k,desempate)
        listaRecuperacion = manejador.getListaRecuperacion()
        listaClasificados = clasificador.clasificar(listaRecuperacion)
        manejador.escribirArchivo(listaClasificados)
        estadisticas = e.Estadisticas("matrizKNN.txt",listaClasificados,"iris-comp1.csv")
        estadisticas.leerArchivoComparacion()
        estadisticas.generarMatrizConfusion(4)
        graficar(listaEntrenamiento,listaClasificados,clas)
    if clas == 5:
        patrones = []
        a = np.array([0,1,0,0,1])
        b = np.array([1,1,0,1,1])
        c = np.array([1,1,1,1,0])
        patrones.append(a)
        patrones.append(b)
        patrones.append(c)
        clases = []
        a = np.array([1,0,0])
        b = np.array([0,1,0])
        c = np.array([0,0,1])
        clases.append(a)
        clases.append(b)
        clases.append(c)
        lernmatrix = lm.Lernmatrix(clases,patrones)
        print("Asociaciones: x0: " + str(patrones[0]) + ",y0: " + str(clases[0]) + "; x1: " + str(patrones[1]) + ",y1: " + str(clases[1]) + "; x2: " + str(patrones[2]) + ",y2: " + str(clases[2]))
        M = lernmatrix.crearMatriz()
        print("\n Matriz de la memoria asociativa:\n " + str(M))
        clasesAsignadas = lernmatrix.recuperarPatrones(M,patrones)
        print(clasesAsignadas)
        while True:
            patronesRuido = patrones.copy()
            print("\n A continuación puede probar el nivel de ruido que soporta la memoria asociativa")
            print("1.- Ruido aditivo\n2.-Ruido sustractivo\n3.- Ruido mixto")
            ruido = int(input())
            print("Selecciona el patrón al que quieres introducir ruido\n")
            patron = int(input())
            print("Digita cuántos bits quieres cambiar")
            bits = int(input())
            patronRuido = lernmatrix.introducirRuido(patrones[patron],bits,ruido)
            patronesRuido[patron] = patronRuido[0]
            print("Enviando..." + str(patronesRuido))
            clasesAsignadas = lernmatrix.recuperarPatrones(M,patronesRuido)
            print("Ruido al " + str(patronRuido[1]*100) + "%\n")
            print(clasesAsignadas)
            print("¿salir? s = si , n = no")
            if input() == "s": break





main()
