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

    # Mostrar solo una vez el padre
    update_callback(frase_actual="".join(padre),
                    generacion=cont,
                    adaptacion=adaptacionPadre,
                    padre="".join(padre))

    while True:
        time.sleep(0.05)  # pausa para animación
        hijo = mutacion(padre, destino)
        adaptacionHijo = funcionObjetivo(hijo, destino)
        cont += 1

        if adaptacionHijo > adaptacionPadre:
            padre = hijo
            adaptacionPadre = adaptacionHijo
            update_callback(frase_actual="".join(hijo),
                            generacion=cont,
                            adaptacion=adaptacionHijo,
                            padre=None)  # no volver a cambiar el padre

        if adaptacionHijo >= len(destino):
            break

# Interfaz gráfica
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Algoritmo Genético - Visualizador")

        # Entrada de texto
        ttk.Label(root, text="Frase objetivo:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_destino = ttk.Entry(root, width=30)
        self.entry_destino.grid(row=0, column=1, padx=5, pady=5)

        # Botón iniciar
        self.boton_iniciar = ttk.Button(root, text="Iniciar", command=self.iniciar)
        self.boton_iniciar.grid(row=0, column=2, padx=5, pady=5)

        # Frase actual (estilo grande tipo demo online)
        self.label_frase_actual = ttk.Label(root, text="", font=("Courier", 20, "bold"), foreground="blue")
        self.label_frase_actual.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        # Generación y adaptación
        self.label_generacion = ttk.Label(root, text="Generación: 0", font=("Arial", 12))
        self.label_generacion.grid(row=2, column=0, padx=5, pady=5, sticky="w")

        self.label_adaptacion = ttk.Label(root, text="Adaptación: 0", font=("Arial", 12))
        self.label_adaptacion.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        # Padre inicial
        self.label_padre = ttk.Label(root, text="Padre inicial:", font=("Arial", 10))
        self.label_padre.grid(row=3, column=0, columnspan=3, padx=5, pady=10, sticky="w")

    def actualizar_interfaz(self, frase_actual, generacion, adaptacion, padre=None):
        self.label_frase_actual.config(text=frase_actual)
        self.label_generacion.config(text=f"Generación: {generacion}")
        self.label_adaptacion.config(text=f"Adaptación: {adaptacion}")
        if padre is not None:
            self.label_padre.config(text=f"Padre inicial: {padre}")
        self.root.update_idletasks()

    def iniciar(self):
        destino = self.entry_destino.get()
        if not destino.strip():
            return

        # Limpiar etiquetas
        self.label_frase_actual.config(text="")
        self.label_generacion.config(text="Generación: 0")
        self.label_adaptacion.config(text="Adaptación: 0")
        self.label_padre.config(text="Padre inicial:")

        # Iniciar hilo del algoritmo genético
        hilo = threading.Thread(
            target=ejecutar_algoritmo,
            args=(destino, self.actualizar_interfaz),
            daemon=True
        )
        hilo.start()

# Ejecutar interfaz
root = tk.Tk()
app = App(root)
root.mainloop()
