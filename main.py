# ==============================================================================
# MÓDULO: main.py
# DESCRIPCIÓN:
#   Punto de entrada del simulador. Orquesta el menú principal (carga directa
#   desde archivo CSV y consulta de condiciones de entrada) y el bucle de
#   simulación paso a paso deteniéndose en cada arribo o finalización.
#
# VARIABLES GLOBALES TOCADAS:
#   - PROEST_nuevo, PROEST_listo, PROEST_lisus, PROEST_raning
#     (importadas de src.estado; solo lectura para condición de corte del bucle).
#
# VARIABLES LOCALES CREADAS:
#   - En ejecutar_simulacion: hubo_reingreso, hubo_arribo, termino_proceso.
#   - En menu_principal: ruta_csv, opcion.
#
# OTROS BLOQUES O FUNCIONES USADAS (EXTERNAS / INTERNAS):
#   - Importadas: reiniciar_estado() (src.estado), reset_clock() y clocking()
#     (src.reloj), cargar_desde_csv() (src.carga), admitir_nuevos() y
#     reingresar_suspendidos() (src.admision), planificar_srtf() y
#     ejecutar_unidad_cpu() (src.planificador), limpiar_pantalla(),
#     mostrar_estado_sistema(), pausar_simulacion() y
#     mostrar_condiciones_sistema() (src.salida),
#     mostrar_informe_estadistico() (src.estadisticas).
#   - Interna del bloque: ejecutar_simulacion() (invocada por menu_principal).
# ==============================================================================

from src.estado import (
    PROEST_nuevo,
    PROEST_listo,
    PROEST_lisus,
    PROEST_raning,
    reiniciar_estado,
)
from src.reloj import reset_clock, clocking
from src.carga import cargar_desde_csv
from src.admision import admitir_nuevos, reingresar_suspendidos
from src.planificador import planificar_srtf, ejecutar_unidad_cpu
from src.salida import (
    limpiar_pantalla,
    mostrar_estado_sistema,
    pausar_simulacion,
    mostrar_condiciones_sistema,
)
from src.estadisticas import mostrar_informe_estadistico


def ejecutar_simulacion():
    """Bucle principal del simulador con pausas en cada arribo o finalización de proceso."""
    reset_clock()
    mostrar_estado_sistema("INICIO DE SIMULACIÓN (Memoria Inicializada)")
    pausar_simulacion()

    while PROEST_nuevo or PROEST_listo or PROEST_lisus or PROEST_raning:
        # 1. Intentar reingresar procesos suspendidos si hay memoria disponible
        hubo_reingreso = reingresar_suspendidos()

        # 2. Evaluar arribo de procesos nuevos en el CLOCK actual
        hubo_arribo = admitir_nuevos()

        # 3. Planificar CPU con SRTF (incluye desalojo si corresponde)
        planificar_srtf()

        # 4. Si llegó un nuevo proceso (o reingresó), mostrar estado y pausar según consigna
        if hubo_arribo or hubo_reingreso:
            mostrar_estado_sistema("ARRIBO / ADMISIÓN DE PROCESO")
            pausar_simulacion()

        # 5. Ejecutar 1 unidad de tiempo en CPU
        termino_proceso = ejecutar_unidad_cpu()

        # 6. Avanzar el reloj del sistema en 1 unidad
        clocking(1)

        # 7. Si terminó un proceso en este ciclo, liberar/reingresar y mostrar estado obligatorio
        if termino_proceso:
            reingresar_suspendidos()
            mostrar_estado_sistema("FINALIZACIÓN DE PROCESO EN EJECUCIÓN")
            pausar_simulacion()

    mostrar_informe_estadistico()


def menu_principal():
    """Menú de inicio para ejecutar la simulación o consultar las condiciones del CSV."""
    ruta_csv = "data/procesos.csv"

    while True:
        reiniciar_estado()
        limpiar_pantalla()
        print("======================================================")
        print("   SIMULADOR DE GESTIÓN DE PROCESOS Y MEMORIA (MVT)   ")
        print("        Planificación: SRTF  |  Memoria: Best-Fit     ")
        print("======================================================")
        print(f"1. Iniciar simulación desde archivo CSV ({ruta_csv})")
        print("2. Ver condiciones del archivo CSV, columnas y sistema")
        print("3. Salir")

        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == "1":
            if cargar_desde_csv(ruta_csv):
                pausar_simulacion()
                ejecutar_simulacion()
            pausar_simulacion()

        elif opcion == "2":
            mostrar_condiciones_sistema()
            pausar_simulacion()

        elif opcion == "3":
            print("Saliendo del simulador...")
            break
        else:
            print("Opción inválida.")
            pausar_simulacion()


if __name__ == "__main__":
    menu_principal()