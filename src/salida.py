# ==============================================================================
# MÓDULO: src/salida.py
# DESCRIPCIÓN:
#   Administra toda la presentación por consola en cada evento clave del
#   simulador: resumen de totales de memoria y estados, estado del procesador,
#   tabla de particiones MVT, colas de planificación, mapa visual alineado de
#   Memoria Central, condiciones del sistema y pausas de control.
#
# VARIABLES GLOBALES TOCADAS:
#   - memoria_central, PROEST_nuevo, PROEST_listo, PROEST_lisus, PROEST_raning,
#     PROEST_finished (importadas de src.estado; solo lectura).
#   - TAM_SO, TAM_USUARIO, MEM_LIBRE, MAX_PROCESOS_ACTIVOS, IDX_ID, IDX_TA,
#     IDX_RESTANTE, IDX_TAM (importadas de src.config; solo lectura).
#
# VARIABLES LOCALES CREADAS:
#   - En imprimir_mapa_mc: simbolos_mapa, siguiente_letra, celda, referencias,
#     pid, letra, i, fila_visual.
#   - En mostrar_estado_sistema: motivo_evento, mem_libre_total,
#     mem_ocupada_usuario, activos_total, total_cargados, p, part,
#     listos_str, lisus_str, nuevos_str, fin_str.
#
# OTROS BLOQUES O FUNCIONES USADAS (EXTERNAS / INTERNAS):
#   - Importadas: os.system, generar_tabla_particiones() (src.memoria),
#     contar_procesos_activos() (src.estado), obtener_clock() (src.reloj).
#   - Auxiliar interna del bloque: imprimir_mapa_mc().
# ==============================================================================

import os
from src.config import (
    TAM_SO,
    TAM_USUARIO,
    MEM_LIBRE,
    MAX_PROCESOS_ACTIVOS,
    IDX_ID,
    IDX_TA,
    IDX_RESTANTE,
    IDX_TAM,
)
from src.estado import (
    memoria_central,
    PROEST_nuevo,
    PROEST_listo,
    PROEST_lisus,
    PROEST_raning,
    PROEST_finished,
    contar_procesos_activos,
)
from src.memoria import generar_tabla_particiones
from src.reloj import obtener_clock


def limpiar_pantalla():
    """Limpia la consola según el sistema operativo."""
    os.system("cls" if os.name == "nt" else "clear")


def mostrar_condiciones_sistema():
    """Muestra las condiciones del archivo CSV, columnas, tipos de datos y reglas del sistema."""
    limpiar_pantalla()
    print("========================================================================")
    print("         CONDICIONES DE ENTRADA Y RESTRICCIONES DEL SIMULADOR           ")
    print("========================================================================")
    print("\n1) CONDICIONES DEL ARCHIVO DE ENTRADA:")
    print("   * Ubicación y formato:  Archivo CSV en 'data/procesos.csv' (separado por comas).")
    print("   * Encabezado obligatorio: Debe incluir exactamente los nombres de columnas en la fila 1.")
    print("   * Límite de carga:      Máximo 10 procesos válidos (los excedentes se descartan).")

    print("\n2) CONDICIONES DE COLUMNAS Y TIPOS DE DATOS:")
    print("   * proc_id  -> Texto / Identificador único no vacío (ej: P1, P2, A).")
    print("   * proc_ta  -> Entero >= 0  (Tiempo de arribo en unidades de tiempo).")
    print("   * proc_ti  -> Entero > 0   (Tiempo de irrupción / ráfaga de CPU).")
    print("   * proc_tam -> Entero 1..450 (Tamaño del proceso en K; no puede superar 450K).")

    print("\n3) REGLAS DE MEMORIA Y PLANIFICACIÓN:")
    print("   * Memoria Central:      550K totales (100K Sistema Operativo + 450K Usuario).")
    print("   * Gestión de Memoria:   Particiones Variables (MVT) con Best-Fit (sin compactación).")
    print("   * Planificación CPU:    SRTF (Shortest Remaining Time First - Apropiativo).")
    print("   * Multiprogramación:    Máximo 5 procesos activos (Ejecución + Listos + Listos/Susp).")
    print("========================================================================")


def imprimir_mapa_mc():
    """Muestra la Memoria Central (550K) en filas de 25 celdas perfectamente alineadas."""
    simbolos_mapa = {}
    siguiente_letra = ord("A")

    for celda in memoria_central:
        if celda not in ("#", "~") and celda not in simbolos_mapa:
            simbolos_mapa[celda] = chr(siguiente_letra)
            siguiente_letra += 1

    print("\n--- MAPA VISUAL DE MEMORIA CENTRAL (550K) ---")
    referencias = ["SO: #", "Libre: ~"] + [f"{pid}: {letra}" for pid, letra in simbolos_mapa.items()]
    print(f"Referencias -> {' | '.join(referencias)}")

    for i in range(0, len(memoria_central), 25):
        fila_visual = [
            celda if celda in ("#", "~") else simbolos_mapa[celda]
            for celda in memoria_central[i : i + 25]
        ]
        print(" ".join(fila_visual))


def mostrar_estado_sistema(motivo_evento):
    """Presenta en pantalla el estado completo requerido por la consigna."""
    mem_libre_total = memoria_central[TAM_SO:].count(MEM_LIBRE)
    mem_ocupada_usuario = TAM_USUARIO - mem_libre_total
    activos_total = contar_procesos_activos()
    total_cargados = len(PROEST_nuevo) + activos_total + len(PROEST_finished)

    print("\n" + "=" * 74)
    print(f"INSTANTE DE TIEMPO (CLOCK): {obtener_clock()}  |  DISPARADOR: {motivo_evento}")
    print("=" * 74)

    # 0. Resumen de totales y ubicación
    print("\n0) RESUMEN DE TOTALES Y UBICACIÓN:")
    print(
        f"   -> Memoria Usuario:  {mem_ocupada_usuario}K ocupados + {mem_libre_total}K libres = {TAM_USUARIO}K totales"
    )
    print(
        f"   -> Activos en Sist.: {activos_total}/{MAX_PROCESOS_ACTIVOS} "
        f"(Ejecución: {len(PROEST_raning)} | Listos: {len(PROEST_listo)} | Listos/Susp: {len(PROEST_lisus)})"
    )
    print(
        f"   -> Total Procesos:   {total_cargados} "
        f"(Nuevos: {len(PROEST_nuevo)} | Activos: {activos_total} | Terminados: {len(PROEST_finished)})"
    )

    # 1. Estado del procesador
    print("\n1) ESTADO DEL PROCESADOR:")
    if PROEST_raning:
        p = PROEST_raning[0]
        print(f"   -> En Ejecución: {p[IDX_ID]} (Tiempo restante: {p[IDX_RESTANTE]} ut | Tamaño: {p[IDX_TAM]}K)")
    else:
        print("   -> CPU Ociosa (ningún proceso en ejecución)")

    # 2. Tabla de particiones de memoria (MVT)
    print("\n2) TABLA DE PARTICIONES DE MEMORIA (MVT - Zona Usuario 100..549):")
    print(f"   {'ID Part.':<10} | {'Dir. Inicio':<12} | {'Tamaño (K)':<12} | {'Proceso Asig.':<15} | {'Fragmentación':<14}")
    print("   " + "-" * 71)
    for part in generar_tabla_particiones():
        print(f"   {part[0]:<10} | {part[1]:<12} | {part[2]:<12} | {part[3]:<15} | {part[4]:<14}")

    # 3. Estado de las colas de listos y listos/suspendidos
    print("\n3) COLAS DE PLANIFICACIÓN Y ESTADOS:")
    listos_str = [f"{p[IDX_ID]} (rest:{p[IDX_RESTANTE]})" for p in PROEST_listo]
    lisus_str = [f"{p[IDX_ID]} (tam:{p[IDX_TAM]}K)" for p in PROEST_lisus]
    nuevos_str = [f"{p[IDX_ID]} (TA:{p[IDX_TA]})" for p in PROEST_nuevo]
    fin_str = [p[IDX_ID] for p in PROEST_finished]

    print(f"   -> Cola de Listos:              {listos_str if listos_str else '[]'}")
    print(f"   -> Cola de Listos/Suspendidos:  {lisus_str if lisus_str else '[]'}")
    print(f"   -> Cola de Nuevos (esperando):  {nuevos_str if nuevos_str else '[]'}")
    print(f"   -> Procesos Terminados:         {fin_str if fin_str else '[]'}")

    imprimir_mapa_mc()
    print("=" * 74)


def pausar_simulacion():
    """Detiene la ejecución hasta que el usuario presione ENTER (evita corridas ininterrumpidas)."""
    input("\nPresione ENTER para continuar la simulación...")