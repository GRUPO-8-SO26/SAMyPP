# ==============================================================================
# MÓDULO: src/memoria.py
# DESCRIPCIÓN:
#   Implementa la administración de Memoria Central bajo esquema de particiones
#   variables (MVT) con política de asignación Best-Fit, liberación contigua y
#   construcción de la tabla de particiones y fragmentación.
#
# VARIABLES GLOBALES TOCADAS:
#   - memoria_central (importada de src.estado; leída y modificada celda a celda).
#   - PROEST_lisus (importada de src.estado; solo lectura para evaluar
#     fragmentación externa en generar_tabla_particiones).
#   - TAM_SO, TAM_TOTAL_MC, MEM_LIBRE (importadas de src.config; solo lectura).
#
# VARIABLES LOCALES CREADAS:
#   - En cargar_en_memoria / liberar_memoria: dir_inicio, tam, proc_id, i.
#   - En asignar_bestfit: tam, proc_id, dir_tentativa, menor_hueco, i,
#     inicio_hueco, tam_hueco.
#   - En generar_tabla_particiones: tabla, i, part_id, hay_suspendidos,
#     contenido_actual, inicio, tam_particion, proc_asignado, fragmentacion.
#
# OTROS BLOQUES O FUNCIONES USADAS (EXTERNAS / INTERNAS):
#   - Auxiliar interna del bloque: cargar_en_memoria() (invocada por
#     asignar_bestfit).
# ==============================================================================

from src.config import TAM_SO, TAM_TOTAL_MC, MEM_LIBRE
from src.estado import memoria_central, PROEST_lisus


def cargar_en_memoria(dir_inicio, tam, proc_id):
    """Asigna el identificador del proceso en 'tam' posiciones consecutivas desde 'dir_inicio'."""
    for i in range(dir_inicio, dir_inicio + tam):
        memoria_central[i] = proc_id


def liberar_memoria(dir_inicio, tam):
    """Libera las posiciones ocupadas devolviéndolas al estado MEM_LIBRE (~)."""
    if dir_inicio != -1:
        for i in range(dir_inicio, dir_inicio + tam):
            memoria_central[i] = MEM_LIBRE


def asignar_bestfit(tam, proc_id):
    """Busca el hueco libre más pequeño donde quepa 'tam' (Best-Fit).
    Retorna la dirección inicial asignada o -1 si no hay espacio continuo suficiente.
    """
    dir_tentativa = -1
    menor_hueco = float("inf")
    i = TAM_SO

    while i < TAM_TOTAL_MC:
        if memoria_central[i] == MEM_LIBRE:
            inicio_hueco = i
            while i < TAM_TOTAL_MC and memoria_central[i] == MEM_LIBRE:
                i += 1
            tam_hueco = i - inicio_hueco

            if tam_hueco >= tam and tam_hueco < menor_hueco:
                menor_hueco = tam_hueco
                dir_tentativa = inicio_hueco
        else:
            i += 1

    if dir_tentativa != -1:
        cargar_en_memoria(dir_tentativa, tam, proc_id)
        return dir_tentativa

    return -1


def generar_tabla_particiones():
    """Recorre la zona de usuario de la Memoria Central y arma la tabla de particiones MVT:
    [id_particion, dir_comienzo, tam_particion, proc_asignado, fragmentacion]
    """
    tabla = []
    i = TAM_SO
    part_id = 1
    hay_suspendidos = len(PROEST_lisus) > 0

    while i < TAM_TOTAL_MC:
        contenido_actual = memoria_central[i]
        inicio = i

        while i < TAM_TOTAL_MC and memoria_central[i] == contenido_actual:
            i += 1

        tam_particion = i - inicio

        if contenido_actual == MEM_LIBRE:
            proc_asignado = "LIBRE"
            # En MVT, los huecos libres constituyen fragmentación externa si hay procesos esperando memoria
            fragmentacion = tam_particion if hay_suspendidos else 0
        else:
            proc_asignado = contenido_actual
            # En particiones variables (MVT) no existe fragmentación interna
            fragmentacion = 0

        tabla.append([part_id, inicio, tam_particion, proc_asignado, fragmentacion])
        part_id += 1

    return tabla