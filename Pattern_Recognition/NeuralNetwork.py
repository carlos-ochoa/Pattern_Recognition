import numpy as np
#np.random.seed(0)

def sigmoide (x):
    return 1/(1 + np.exp(-x))

def derivadasigmoide(x):
    return x * (1 - x)

#Tabla xor
inputs = np.array([[0,0],[0,1],[1,0],[1,1]])
salidaEsperada = np.array([[0],[1],[1],[0]])

epochs = 10000
lr = 0.1
NeuronasCapaEntrada, NeuronasCapaOculta, NeuronasCapaSalida = 2,2,1

#Iniciamos los valores de manera aleatoria
pesosOcultos = np.random.uniform(size=(NeuronasCapaEntrada,NeuronasCapaOculta))
biasOcultos =np.random.uniform(size=(1,NeuronasCapaOculta))
pesosSalidas = np.random.uniform(size=(NeuronasCapaOculta,NeuronasCapaSalida))
biasSalidas = np.random.uniform(size=(1,NeuronasCapaSalida))

print("Pesos iniciales de la capa oculta: ",end='')
print(*pesosOcultos)
print("Bias iniciales de la capa oculta: ",end='')
print(*biasOcultos)
print("Pesos iniciales de la capa de salida: ",end='')
print(*pesosSalidas)
print("Bias iniciales de la capa de salida: ",end='')
print(*biasSalidas)


#Training algorithm
for _ in range(epochs):
	#Propagación hacia adelante
	activacionCapaOculta = np.dot(inputs,pesosOcultos)
	activacionCapaOculta += biasOcultos
	salidaCapaOculta = sigmoide(activacionCapaOculta)

	activacionCapaOculta = np.dot(salidaCapaOculta,pesosSalidas)
	activacionCapaOculta += biasSalidas
	salidaPredicha = sigmoide(activacionCapaOculta)

	#Backpropagation
	error = salidaEsperada - salidaPredicha
	d_salidaPredicha = error * derivadasigmoide(salidaPredicha)

	errorCapaOculta = d_salidaPredicha.dot(pesosSalidas.T)
	d_hidden_layer = errorCapaOculta * derivadasigmoide(salidaCapaOculta)

	#Actualizamos pesos y bias
	pesosSalidas += salidaCapaOculta.T.dot(d_salidaPredicha) * lr
	biasSalidas += np.sum(d_salidaPredicha,axis=0,keepdims=True) * lr
	pesosOcultos += inputs.T.dot(d_hidden_layer) * lr
	biasOcultos += np.sum(d_hidden_layer,axis=0,keepdims=True) * lr

print("Pesos finales capa oculta: ",end='')
print(*pesosOcultos)
print("Bias final capa oculta: ",end='')
print(*biasOcultos)
print("Pesos finales capa salida: ",end='')
print(*pesosSalidas)
print("Bias final de salida: ",end='')
print(*biasSalidas)

print("\nSalida de la red neuronal ",end='')
print(*salidaPredicha)
