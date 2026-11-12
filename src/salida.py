import os
from src.config import IDX_ID, IDX_RESTANTE, IDX_TAM
from src.estado import memoria_central, PROEST_listo, PROEST_lisus, PROEST_raning, PROEST_finished
from src.memoria import generar_tabla_particiones
from src.reloj import obtener_clock


def limpiar_pantalla():
    """Limpia la consola según el sistema operativo."""
    os.system("cls" if os.name == "nt" else "clear")


def imprimir_mapa_mc():
    """Muestra la Memoria Central (550K) en filas de 25 celdas."""
    print("\n--- MAPA VISUAL DE MEMORIA CENTRAL (SO: # | Libre: ~) ---")
    for i in range(0, len(memoria_central), 25):
        print(" ".join(memoria_central[i : i + 25]))


def mostrar_estado_sistema(motivo_evento):
    """Presenta en pantalla el estado completo requerido por la consigna."""
    print("\n" + "=" * 72)
    print(f"INSTANTE DE TIEMPO (CLOCK): {obtener_clock()}  |  DISPARADOR: {motivo_evento}")
    print("=" * 72)

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
    print("\n3) COLAS DE PLANIFICACIÓN:")
    listos_str = [f"{p[IDX_ID]} (rest:{p[IDX_RESTANTE]})" for p in PROEST_listo]
    lisus_str = [f"{p[IDX_ID]} (tam:{p[IDX_TAM]}K)" for p in PROEST_lisus]
    fin_str = [p[IDX_ID] for p in PROEST_finished]

    print(f"   -> Cola de Listos:              {listos_str if listos_str else '[]'}")
    print(f"   -> Cola de Listos/Suspendidos:  {lisus_str if lisus_str else '[]'}")
    print(f"   -> Terminados (control):        {fin_str if fin_str else '[]'}")

    imprimir_mapa_mc()
    print("=" * 72)


def pausar_simulacion():
    """Detiene la ejecución hasta que el usuario presione ENTER (evita corridas ininterrumpidas)."""
    input("\nPresione ENTER para continuar la simulación...")