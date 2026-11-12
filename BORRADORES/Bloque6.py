def gestionar_cola_suspendidos():
    """Verifica si los procesos en 'Listos y Suspendidos' (PROEST_lisus) 
       ahora pueden ingresar a memoria principal gracias al espacio liberado.
    """
    global PROEST_lisus, PROEST_listo
    i = 0
    while i < len(PROEST_lisus):
        total_activos = len(PROEST_listo) + len(PROEST_lisus) + len(PROEST_raning)
        if total_activos >= 5:
            break

        proc = PROEST_lisus[i]
        dir_asignada = asignar_bestfit(tam=proc[3], proc=proc[0])
        if dir_asignada != -1:
            proc[5] = dir_asignada
            PROEST_listo.append(proc)
            PROEST_lisus.pop(i)
            print(f"EVENTO CLAVE: Proceso '{proc[0]}' recuperado de Listos/Suspendidos a Listos (Dir {dir_asignada}).")
        else:
            i += 1

def planificador_srtf():
    """Selecciona el proceso con menor tiempo restante (SRTF) mediante un recorrido 
       secuencial con variable auxiliar, sin alterar el orden estructural físico.
    """
    if not PROEST_listo:
        return None

    indice_menor = 0
    menor_tiempo_restante = PROEST_listo[0][4]

    for idx in range(1, len(PROEST_listo)):
        if PROEST_listo[idx][4] < menor_tiempo_restante:
            menor_tiempo_restante = PROEST_listo[idx][4]
            indice_menor = idx

    return PROEST_listo.pop(indice_menor)