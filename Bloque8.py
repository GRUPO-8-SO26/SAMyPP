def ejecutar_simulador():
    """Controla el ciclo de vida completo de los procesos, eventos clave y políticas SRTF."""
    global CLOCK, DATOS_ESTADISTICOS
    reset_clock()
    limpiar_pantalla()
    
    print("--- 1. CARGA Y VALIDACIÓN DE PROCESOS DESDE CSV ---")
    validar_y_cargar_procesos("procesos.csv")
    
    print("\n--- 2. ESTADO INICIAL DE LA MEMORIA CENTRAL ---")
    mapa_MC(memoria_central)
    
    input("\nPresione ENTER para iniciar los ciclos de reloj...")

    while PROEST_nuevo or PROEST_listo or PROEST_lisus or PROEST_raning:
        limpiar_pantalla()
        print(f"\n================ CLOCK ACTUAL: {CLOCK} ================")
        
        # 1. Evaluar llegada de nuevos procesos según su tiempo de arribo (ta)
        i = 0
        while i < len(PROEST_nuevo):
            proc = PROEST_nuevo[i]
            if proc[1] <= CLOCK:
                total_activos = len(PROEST_listo) + len(PROEST_lisus) + len(PROEST_raning)
                if total_activos >= 5:
                    print(f"EVENTO CLAVE: Límite máximo de 5 procesos activos alcanzado. Proceso '{proc[0]}' retenido.")
                    i += 1
                    continue

                dir_asignada = asignar_bestfit(tam=proc[3], proc=proc[0])
                if dir_asignada != -1:
                    proc[5] = dir_asignada
                    PROEST_listo.append(proc)
                    PROEST_nuevo.pop(i)
                    print(f"EVENTO CLAVE: Proceso '{proc[0]}' admitido en memoria (dir {dir_asignada}) y pasado a Listos.")
                else:
                    PROEST_lisus.append(proc)
                    PROEST_nuevo.pop(i)
                    print(f"EVENTO CLAVE: Proceso '{proc[0]}' (Tam: {proc[3]}K) sin espacio continuo, derivado a LISTOS Y SUSPENDIDOS.")
            else:
                i += 1

        # 2. Planificación a Corto Plazo (Algoritmo SRTF y Desalojo)
        if PROEST_listo:
            candidato = planificador_srtf()
            
            if not PROEST_raning:
                PROEST_raning.append(candidato)
                print(f"CPU: Proceso '{candidato[0]}' ingresa a EJECUCIÓN.")
            else:
                proc_actual = PROEST_raning[0]
                if candidato[4] < proc_actual[4]:
                    print(f"EVENTO CLAVE - DESALOJO: Proceso '{candidato[0]}' (resto {candidato[4]}) desaloja a '{proc_actual[0]}' (resto {proc_actual[4]}).")
                    PROEST_listo.append(PROEST_raning.pop(0))
                    PROEST_raning.append(candidato)
                else:
                    PROEST_listo.append(candidato)

        # 3. Ejecución del proceso en curso durante 1 unidad de tiempo
        if PROEST_raning:
            proc_actual = PROEST_raning[0]
            proc_actual[4] -= 1
            print(f"PROCESADOR: Ejecutando proceso '{proc_actual[0]}'. Tiempo restante: {proc_actual[4]}")

            if proc_actual[4] == 0:
                print(f"EVENTO CLAVE: Proceso '{proc_actual[0]}' ha TERMINADO.")
                liberar_memoria_fisica(dir=proc_actual[5], tam=proc_actual[3])
                
                # Cálculo de tiempos estadísticos al terminar el proceso:
                tiempo_finalizacion = CLOCK + 1
                tiempo_retorno = tiempo_finalizacion - proc_actual[1]
                tiempo_espera = tiempo_retorno - proc_actual[2]
                
                DATOS_ESTADISTICOS.append([proc_actual[0], proc_actual[1], proc_actual[2], proc_actual[3], tiempo_retorno, tiempo_espera])
                
                PROEST_finished.append(PROEST_raning.pop(0))
                
                # Al liberar memoria, revisamos si procesos suspendidos pueden entrar
                gestionar_cola_suspendidos()
        
        # 4. Mostrar información obligatoria por cada ciclo del reloj
        print("\n--- ESTADO DEL PROCESADOR ---")
        if PROEST_raning:
            print(f"Corriendo en CPU: Proceso '{PROEST_raning[0][0]}' (Restante: {PROEST_raning[0][4]}K)")
        else:
            print("CPU Ociosa (Sin proceso en ejecución)")

        print("\n--- TABLA DE PARTICIONES DE MEMORIA (MVT) ---")
        print(f"{'PARTICIÓN':<10} | {'INICIO':<8} | {'TAMAÑO':<8} | {'ASIGNADO':<15} | {'FRAG. EXTERNA':<15}")
        print("-" * 65)
        for part in generar_tabla_particiones():
            print(f"{part[0]:<10} | {part[1]:<8} | {part[2]:<8} | {part[3]:<15} | {part[4]:<15}")

        print("\n--- COLAS DEL SISTEMA ---")
        print(f"Cola Listos: {[p[0] for p in PROEST_listo]}")
        print(f"Cola Listos/Suspendidos: {[p[0] for p in PROEST_lisus]}")
        print(f"Procesos Terminados: {[p[0] for p in PROEST_finished]}")
        
        # 5. Avanzar el reloj del sistema en 1 unidad de tiempo
        clocking(1)
        input("\nPresione ENTER para avanzar al siguiente ciclo...")

    print("\n--- SIMULACIÓN FINALIZADA CON ÉXITO ---")
    
    # Mostrar el informe estadístico final al terminar todos los procesos
    mostrar_informe_estadistico()

if __name__ == "__main__":
    ejecutar_simulador() 