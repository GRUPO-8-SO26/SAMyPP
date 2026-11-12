import string
import os
import csv

# --- BLOQUE 1: CONFIGURACIÓN Y VARIABLES GLOBALES DEL SISTEMA ---

# Variable global que gobierna el tiempo del simulador
CLOCK = 0

# Definición de estados de memoria central
MEM_LIBRE = ["~"]   # Espacio libre sin usar
MEM_FRAG = ["*"]    # Espacio con fragmentación externa
MEM_VACIA = MEM_LIBRE + MEM_FRAG  # Espacio asignable
MEM_SO = ["#"]      # Espacio reservado para el Sistema Operativo

# Creación de Memoria Central (MC): 100K para SO y 450K para usuarios (Total 550)
TAM_SO = 100
memoria_central = MEM_SO * TAM_SO + [MEM_LIBRE[0] for _ in range(550 - TAM_SO)]

# Estructuras de listas para los estados de los procesos
PROEST_nuevo = []      # Lista de procesos validados pendientes de ingresar
PROEST_listo = []      # Lista de procesos en memoria listos para ejecutar
PROEST_lisus = []      # Lista de procesos listos pero suspendidos por falta de memoria
PROEST_raning = []     # Lista (máximo 1 elemento) con el proceso en ejecución
PROEST_finished = []   # Lista de procesos terminados para estadísticas

# Registro para estadísticas (guardará los tiempos de cada proceso al finalizar)
# Estructura: [id, ta, ti, tam, tiempo_retorno, tiempo_espera]
DATOS_ESTADISTICOS = []
