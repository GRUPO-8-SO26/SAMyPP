from src.estado import DATOS_ESTADISTICOS
from src.reloj import obtener_clock


def mostrar_informe_estadistico():
    """Calcula y muestra el informe estadístico al finalizar la simulación."""
    print("\n" + "=" * 72)
    print("               INFORME ESTADÍSTICO FINAL DE LA SIMULACIÓN")
    print("=" * 72)

    if not DATOS_ESTADISTICOS:
        print("No se completaron procesos durante la simulación.")
        return

    print(f"{'PROCESO':<10} | {'ARRIBO (TA)':<12} | {'IRRUPCIÓN (TI)':<15} | {'RETORNO':<10} | {'ESPERA':<10}")
    print("-" * 68)

    suma_retorno = 0
    suma_espera = 0
    cantidad = len(DATOS_ESTADISTICOS)

    for reg in DATOS_ESTADISTICOS:
        proc_id, proc_ta, proc_ti, _, retorno, espera = reg
        suma_retorno += retorno
        suma_espera += espera
        print(f"{proc_id:<10} | {proc_ta:<12} | {proc_ti:<15} | {retorno:<10} | {espera:<10}")

    prom_retorno = suma_retorno / cantidad
    prom_espera = suma_espera / cantidad
    tiempo_total = obtener_clock()
    rendimiento = cantidad / tiempo_total if tiempo_total > 0 else 0

    print("-" * 68)
    print(f"Tiempo Total de Simulación:           {tiempo_total} unidades de tiempo")
    print(f"Tiempo de Retorno Promedio:           {prom_retorno:.2f} unidades")
    print(f"Tiempo de Espera Promedio:            {prom_espera:.2f} unidades")
    print(f"Rendimiento del Sistema (Throughput): {rendimiento:.4f} trabajos / unidad de tiempo")
    print("=" * 72)