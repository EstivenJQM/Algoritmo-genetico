import random as rand

# Caracteres disponibles, incluyendo espacio y mayúsculas
origen = " abcdefghijklmnñopqrstuvwxyzABCDEFGHIJKLMNÑOPQRSTUVWXYZ"

# Frase objetivo
destino = "Algoritmo genetico"

# Generar un individuo aleatorio
def definirPoblacion(longitud):
    return rand.sample(origen * 2, longitud)  # Duplicamos origen para evitar errores si longitud > len(origen)

# Evaluar cuántas letras están en la posición correcta
def funcionObjetivo(individuo):
    valor = sum(1 for letraDes, letraInd in zip(destino, individuo) if letraDes == letraInd)
    return valor

# Cruce genético: inserta fragmentos del destino en el individuo
def cruce(ind):
    individuoCruzado = ind.copy()
    puntoCruce = rand.randint(0, len(ind) - 2)
    individuoCruzado[puntoCruce:puntoCruce+2] = destino[puntoCruce:puntoCruce+2]
    return individuoCruzado

# Mutación aleatoria en un punto del individuo
def mutacion(individuo):
    individuoMutado = individuo.copy()
    indice = rand.randint(0, len(individuo) - 1)
    nuevoValor = rand.choice(origen)
    if individuoMutado[indice] != destino[indice]:
        individuoMutado[indice] = nuevoValor
    return individuoMutado

# Crear padre inicial
padre = definirPoblacion(len(destino))
print("Padre inicial:", "".join(padre))
adaptacionPadre = funcionObjetivo(padre)

cont = 0
iteraciones = 0

# Evolución
while True:
    iteraciones += 1
    hijo = mutacion(padre)
    adaptacionHijo = funcionObjetivo(hijo)
    cont += 1

    if adaptacionPadre >= adaptacionHijo:
        continue
    if adaptacionHijo >= len(destino):
        break

    padre = hijo
    adaptacionPadre = adaptacionHijo

print(f"Generación {cont}: {''.join(hijo)} (adaptación = {adaptacionHijo})")
