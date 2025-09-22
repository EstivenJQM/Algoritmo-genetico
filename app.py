import tkinter as tk
from tkinter import ttk
import random as rand
import threading
import time

# Caracteres posibles
origen = " abcdefghijklmnñopqrstuvwxyzABCDEFGHIJKLMNÑOPQRSTUVWXYZ"

# Función objetivo
def funcionObjetivo(individuo, destino):
    return sum(1 for letraDes, letraInd in zip(destino, individuo) if letraDes == letraInd)

# Mutación
def mutacion(individuo, destino):
    individuoMutado = individuo.copy()
    indice = rand.randint(0, len(individuo) - 1)
    nuevoValor = rand.choice(origen)
    if individuoMutado[indice] != destino[indice]:
        individuoMutado[indice] = nuevoValor
    return individuoMutado

# Definir individuo aleatorio
def definirPoblacion(longitud):
    return rand.sample(origen * 2, longitud)

# Función que corre el algoritmo genético
def ejecutar_algoritmo(destino, update_callback):
    padre = definirPoblacion(len(destino))
    adaptacionPadre = funcionObjetivo(padre, destino)
    cont = 0

    update_callback("".join(padre), cont, adaptacionPadre, "".join(padre))

    while True:
        time.sleep(0.05)  # hace la animación más visible
        hijo = mutacion(padre, destino)
        adaptacionHijo = funcionObjetivo(hijo, destino)
        cont += 1

        if adaptacionPadre >= adaptacionHijo:
            continue

        padre = hijo
        adaptacionPadre = adaptacionHijo

        update_callback("".join(padre), cont, adaptacionPadre, "".join(hijo))

        if adaptacionHijo >= len(destino):
            break

# Interfaz gráfica
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Algoritmo Genético")

        # Entrada de texto
        ttk.Label(root, text="Palabra objetivo:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_destino = ttk.Entry(root, width=30)
        self.entry_destino.grid(row=0, column=1, padx=5, pady=5)

        # Botón iniciar
        self.boton_iniciar = ttk.Button(root, text="Iniciar", command=self.iniciar)
        self.boton_iniciar.grid(row=0, column=2, padx=5, pady=5)

        # Etiquetas de salida
        self.label_padre = ttk.Label(root, text="Padre inicial:")
        self.label_padre.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="w")

        self.label_generacion = ttk.Label(root, text="Generación: 0")
        self.label_generacion.grid(row=2, column=0, columnspan=1, padx=5, pady=5, sticky="w")

        self.label_adaptacion = ttk.Label(root, text="Adaptación: 0")
        self.label_adaptacion.grid(row=2, column=1, columnspan=1, padx=5, pady=5, sticky="w")

        self.label_actual = ttk.Label(root, text="Frase actual:")
        self.label_actual.grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky="w")

    def actualizar_interfaz(self, padre, generacion, adaptacion, frase):
        self.label_padre.config(text=f"Padre inicial: {padre}")
        self.label_generacion.config(text=f"Generación: {generacion}")
        self.label_adaptacion.config(text=f"Adaptación: {adaptacion}")
        self.label_actual.config(text=f"Frase actual: {frase}")
        self.root.update_idletasks()

    def iniciar(self):
        destino = self.entry_destino.get()
        if not destino:
            return

        # Iniciar el algoritmo en un hilo para no congelar la GUI
        hilo = threading.Thread(
            target=ejecutar_algoritmo,
            args=(destino, self.actualizar_interfaz),
            daemon=True
        )
        hilo.start()

# Iniciar GUI
root = tk.Tk()
app = App(root)
root.mainloop()
