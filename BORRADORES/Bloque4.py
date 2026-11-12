def validar_y_cargar_procesos(nombre_archivo):
    """Lee y valida los procesos directamente desde el archivo .csv real.
       Estructura esperada en el CSV: id, tamano, llegada, irrupcion
    """
    global PROEST_nuevo
    
    if not os.path.exists(nombre_archivo):
        print(f"Error: No se encontró el archivo '{nombre_archivo}'. Asegúrese de crearlo en la misma carpeta.")
        return
    
    contador_validos = 0
    
    try:
        with open(nombre_archivo, mode='r', encoding='utf-8-sig') as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                p_id = fila['id'].strip()
                p_tam = int(fila['tamano'].strip())
                p_ta = int(fila['llegada'].strip())
                p_ti = int(fila['irrupcion'].strip())
                
                # Validación 1: El tamaño no puede superar el espacio total de usuario (450K)
                if p_tam > 450:
                    print(f"Proceso '{p_id}' rechazado: Tamaño ({p_tam}K) excede la memoria total de usuario (450K).")
                    continue
                    
                # Validación 2: Cantidad máxima global de 10 procesos válidos permitidos
                if contador_validos >= 10:
                    print(f"Proceso '{p_id}' rechazado: Límite de 10 procesos válidos alcanzado.")
                    continue
                    
                # Estructura del proceso: [id, tiempo_arribo, irrupcion_total, tamaño, tiempo_restante, direccion_memoria, irrupcion_inicial]
                proceso_valido = [p_id, p_ta, p_ti, p_tam, p_ti, -1, p_ti]
                PROEST_nuevo.append(proceso_valido)
                contador_validos += 1
                print(f"Proceso '{p_id}' validado e ingresado a PROEST_nuevo (Llegada: {p_ta}, Irrupción: {p_ti}, Tamaño: {p_tam}K).")
        
        # Ordenar los procesos nuevos por su tiempo de arribo (ta) de forma ascendente
        PROEST_nuevo.sort(key=lambda x: x[1])
        
    except Exception as e:
        print(f"Error al leer el archivo CSV: {e}")