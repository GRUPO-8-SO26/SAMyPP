# ==============================================================================
# MÓDULO: src/estado.py
# DESCRIPCIÓN:
#   Mantiene las estructuras de datos compartidas en memoria (arreglo de
#   Memoria Central, colas de estados de procesos y tabla de estadísticas) y
#   provee funciones de inicialización y conteo del grado de multiprogramación.
#
# VARIABLES GLOBALES TOCADAS:
#   - Definidas y mutadas en este módulo:
#     memoria_central, PROEST_nuevo, PROEST_listo, PROEST_lisus,
#     PROEST_raning, PROEST_finished, DATOS_ESTADISTICOS.
#   - Importadas (solo lectura desde src.config):
#     TAM_SO, TAM_USUARIO, MEM_SO, MEM_LIBRE.
#
# VARIABLES LOCALES CREADAS:
#   - Ninguna (opera directamente sobre las listas compartidas).
#
# OTROS BLOQUES O FUNCIONES USADAS (EXTERNAS / INTERNAS):
#   - Métodos nativos de listas: .clear(), len(), slicing [:].
# ==============================================================================

from src.config import TAM_SO, TAM_USUARIO, MEM_SO, MEM_LIBRE

# Memoria Central inicializada: 100K para SO (#) y 450K libres (~)
memoria_central = [MEM_SO] * TAM_SO + [MEM_LIBRE] * TAM_USUARIO

# Listas de estados de procesos
PROEST_nuevo = []
PROEST_listo = []
PROEST_lisus = []
PROEST_raning = []
PROEST_finished = []

# Registro estadístico: [proc_id, proc_ta, proc_ti, proc_tam, retorno, espera]
DATOS_ESTADISTICOS = []


def reiniciar_estado():
    """Restaura la memoria central y todas las listas de estado a su valor inicial."""
    memoria_central[:] = [MEM_SO] * TAM_SO + [MEM_LIBRE] * TAM_USUARIO
    PROEST_nuevo.clear()
    PROEST_listo.clear()
    PROEST_lisus.clear()
    PROEST_raning.clear()
    PROEST_finished.clear()
    DATOS_ESTADISTICOS.clear()


def contar_procesos_activos():
    """Retorna la cantidad total de procesos en Ejecución, Listos y Listos/Suspendidos."""
    return len(PROEST_raning) + len(PROEST_listo) + len(PROEST_lisus)