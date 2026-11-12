# Constantes de Memoria Central (en miles de palabras - K)
TAM_SO = 100
TAM_USUARIO = 450
TAM_TOTAL_MC = TAM_SO + TAM_USUARIO  # 550K

# Símbolos de representación en Memoria Central
MEM_LIBRE = "~"
MEM_SO = "#"

# Límites de procesos según consigna
MAX_PROCESOS_VALIDOS = 10
MAX_PROCESOS_ACTIVOS = 5  # Máximo en Ejecución + Listos + Listos/Suspendidos

# Índices de la estructura de lista de un proceso:
# [proc_id, proc_ta, proc_ti, proc_tam, tiempo_restante, dir_memoria, tiempo_fin]
IDX_ID = 0
IDX_TA = 1
IDX_TI = 2
IDX_TAM = 3
IDX_RESTANTE = 4
IDX_DIR = 5
IDX_FIN = 6