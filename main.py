# ==============================================================================
# MÓDULO: main.py
# DESCRIPCIÓN:
#   Punto de entrada del simulador. Orquesta el menú principal (carga CSV o
#   manual) y el bucle de simulación paso a paso deteniéndose en cada arribo o
#   finalización de proceso.
#
# VARIABLES GLOBALES TOCADAS:
#   - PROEST_nuevo, PROEST_listo, PROEST_lisus, PROEST_raning
#     (importadas de src.estado; solo lectura para condición de corte del bucle).
#
# VARIABLES LOCALES CREADAS:
#   - En ejecutar_simulacion: hubo_reingreso, hubo_arribo, termino_proceso.
#   - En menu_principal: opcion, ruta.
#
# OTROS BLOQUES O FUNCIONES USADAS (EXTERNAS / INTERNAS):
#   - Importadas: reiniciar_estado() (src.estado), reset_clock() y clocking()
#     (src.reloj), cargar_desde_csv() y cargar_manual() (src.carga),
#     admitir_nuevos() y reingresar_suspendidos() (src.admision),
#     planificar_srtf() y ejecutar_unidad_cpu() (src.planificador),
#     limpiar_pantalla(), mostrar_estado_sistema() y pausar_simulacion()
#     (src.salida), mostrar_informe_estadistico() (src.estadisticas).
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
from src.carga import cargar_desde_csv, cargar_manual
from src.admision import admitir_nuevos, reingresar_suspendidos
from src.planificador import planificar_srtf, ejecutar_unidad_cpu
from src.salida import limpiar_pantalla, mostrar_estado_sistema, pausar_simulacion
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
    """Menú de inicio para elegir carga por archivo CSV o ingreso manual."""
    while True:
        reiniciar_estado()
        limpiar_pantalla()
        print("======================================================")
        print("   SIMULADOR DE GESTIÓN DE PROCESOS Y MEMORIA (MVT)   ")
        print("        Planificación: SRTF  |  Memoria: Best-Fit     ")
        print("======================================================")
        print("1. Cargar procesos desde archivo CSV (data/procesos.csv)")
        print("2. Ingresar ruta de archivo CSV personalizada") #quitar
        print("3. Cargar procesos manualmente por teclado")  #quitar
        print("4. Salir")

        opcion = input("\nSeleccione una opción y presione ENTER: ").strip()

        if opcion == "1":
            if cargar_desde_csv("data/procesos.csv"):
                pausar_simulacion()
                ejecutar_simulacion()
            pausar_simulacion()

        elif opcion == "2":
            ruta = input("Ingrese la ruta del archivo CSV: ").strip()
            if cargar_desde_csv(ruta):
                pausar_simulacion()
                ejecutar_simulacion()
            pausar_simulacion()

        elif opcion == "3":
            if cargar_manual():
                pausar_simulacion()
                ejecutar_simulacion()
            pausar_simulacion()

        elif opcion == "4":
            print("Saliendo del simulador...")
            break
        else:
            print("Opción inválida.")
            pausar_simulacion()


if __name__ == "__main__":
    menu_principal()