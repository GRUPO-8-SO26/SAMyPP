def mostrar_informe_estadistico():
    """Calcula y muestra los tiempos de retorno, espera, promedios, rendimiento y fragmentación externa final."""
    global DATOS_ESTADISTICOS, CLOCK
    
    print("\n" + "="*65)
    print("         INFORME ESTADÍSTICO FINAL DE LA SIMULACIÓN")
    print("="*65)
    
    if not DATOS_ESTADISTICOS:
        print("No hay procesos finalizados para generar estadísticas.")
        return

    print(f"{'PROCESO':<10} | {'LLEGADA':<8} | {'IRRUPCIÓN':<10} | {'RETORNO':<10} | {'ESPERA':<8}")
    print("-" * 60)

    suma_retorno = 0
    suma_espera = 0
    total_procesos = len(DATOS_ESTADISTICOS)

    for p in DATOS_ESTADISTICOS:
        p_id, p_ta, p_ti, p_tam, p_retorno, p_espera = p
        suma_retorno += p_retorno
        suma_espera += p_espera
        print(f"{p_id:<10} | {p_ta:<8} | {p_ti:<10} | {p_retorno:<10} | {p_espera:<8}")

    promedio_retorno = suma_retorno / total_procesos
    promedio_espera = suma_espera / total_procesos
    
    # Rendimiento (Throughput): Trabajos terminados por unidad de tiempo total
    rendimiento = total_procesos / CLOCK if CLOCK > 0 else 0

    # Cálculo de la Fragmentación Externa total actual en la memoria central
    tabla_partes = generar_tabla_particiones()
    fragmentacion_externa_total = sum(part[4] for part in tabla_partes if "LIBRE" in part[3] or "FRAG" in part[3])

    print("-" * 60)
    print(f"Tiempo de Retorno Promedio:          {promedio_retorno:.2f} unidades")
    print(f"Tiempo de Espera Promedio:           {promedio_espera:.2f} unidades")
    print(f"Rendimiento del Sistema (Throughput): {rendimiento:.4f} trabajos/unidad")
    print(f"Fragmentación Externa Final en Memoria: {fragmentacion_externa_total} K")
    print("="*65)