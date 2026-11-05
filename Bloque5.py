def carga_memoria_fisica(dir, tam, proc):
    """Carga físicamente el carácter del proceso en la estructura de 'memoria_central'."""
    for i in range(dir, dir + tam):
        memoria_central[i] = proc
    return True

def liberar_memoria_fisica(dir, tam):
    """Libera el espacio ocupado en la memoria central devolviéndolo a MEM_LIBRE (~)."""
    if dir != -1:
        for i in range(dir, dir + tam):
            memoria_central[i] = MEM_LIBRE[0]

def asignar_bestfit(tam, proc):
    """Aplica la política Best-Fit para buscar el hueco libre que mejor se ajuste al tamaño.
       Retorna la dirección de memoria asignada o -1 si no hay espacio suficiente.
    """
    dir_tentativa = -1
    menor_tamano_hueco = float("inf")
    i = 100  # La memoria de usuario arranca en la posición 100 (dejando el SO atrás)
    n = len(memoria_central)

    while i < n:
        if memoria_central[i] in MEM_VACIA:
            inicio_hueco = i
            while i < n and memoria_central[i] in MEM_VACIA:
                i += 1
            tamano_hueco = i - inicio_hueco

            if tamano_hueco >= tam:
                if tamano_hueco < menor_tamano_hueco:
                    menor_tamano_hueco = tamano_hueco
                    dir_tentativa = inicio_hueco
        else:
            i += 1

    if dir_tentativa != -1:
        carga_memoria_fisica(dir=dir_tentativa, tam=tam, proc=proc)
        return dir_tentativa
    else:
        return -1

def generar_tabla_particiones():
    """Recorre la memoria central y genera la tabla de particiones MVT exigida,
       mostrando ID de partición, dirección de comienzo, tamaño, proceso asignado y fragmentación externa.
    """
    tabla = []
    i = 100  # Arranca en la zona de usuario
    n = len(memoria_central)
    part_id = 1

    while i < n:
        char_actual = memoria_central[i]
        inicio = i
        
        # Agrupa bloques consecutivos idénticos en la memoria central
        while i < n and memoria_central[i] == char_actual:
            i += 1
        
        tam_particion = i - inicio
        
        # Determinar el contenido y calcular la fragmentación externa en bloques libres
        if char_actual in MEM_LIBRE:
            proc_asig = "LIBRE (~)"
            frag_externa = tam_particion  # El espacio libre no contiguo se considera fragmentación externa potencial
        elif char_actual in MEM_FRAG:
            proc_asig = "FRAG. EXT (*)"
            frag_externa = tam_particion
        else:
            proc_asig = f"Proceso {char_actual}"
            frag_externa = 0

        tabla.append([part_id, inicio, tam_particion, proc_asig, frag_externa])
        part_id += 1

    return tabla