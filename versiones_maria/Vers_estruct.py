import sys

# --- VARIABLES GLOBALES DEL SISTEMA ---
reloj = 0
procesos_nuevos = []
cola_listos = []
cola_listos_susp = []
ejecucion = None
terminados = []
particiones = []
next_part_id = 2

def inicializar_sistema():
    """Reinicia las variables globales para una nueva ejecución limpia."""
    global reloj, procesos_nuevos, cola_listos, cola_listos_susp, ejecucion, terminados, particiones, next_part_id
    reloj = 0
    procesos_nuevos = []
    cola_listos = []
    cola_listos_susp = []
    ejecucion = None
    terminados = []
    # Inicialización de memoria: 100K para SO, 450K para Usuario
    particiones = [
        {'id_part': 0, 'inicio': 0, 'tamano': 100, 'estado': 'Ocupado', 'pid': 'SO', 'frag_interna': 0},
        {'id_part': 1, 'inicio': 100, 'tamano': 450, 'estado': 'Libre', 'pid': None, 'frag_interna': 0}
    ]
    next_part_id = 2

def cargar_procesos(archivo):
    """Subacción 1: Lee el archivo de texto y carga los procesos en un arreglo ordenado por arribo."""
    global procesos_nuevos
    try:
        with open(archivo, 'r') as f:
            for linea in f:
                if linea.strip():
                    datos = linea.split(',')
                    proceso = {
                        'pid': int(datos[0]),
                        'tamano': int(datos[1]),
                        'arribo': int(datos[2]),
                        'irrupcion': int(datos[3]),
                        'restante': int(datos[3]),
                        'estado': 'Nuevo',
                        'retorno': 0,
                        'espera': 0,
                        'finalizacion': 0
                    }
                    procesos_nuevos.append(proceso)
        procesos_nuevos.sort(key=lambda x: x['arribo'])
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{archivo}'.")
        sys.exit(1)

def contar_procesos_activos():
    """Retorna la cantidad total de procesos activos en el sistema (tope 5)."""
    activos = len(cola_listos) + len(cola_listos_susp)
    if ejecucion is not None:
        activos += 1
    return activos

def asignar_memoria_best_fit(proceso):
    """Subacción de Memoria: Asigna partición usando Best-Fit (MVT) y divide huecos si sobra espacio."""
    global next_part_id, particiones
    mejor_particion = None
    menor_diferencia = float('inf')

    for part in particiones:
        if part['estado'] == 'Libre' and part['tamano'] >= proceso['tamano']:
            diferencia = part['tamano'] - proceso['tamano']
            if diferencia < menor_diferencia:
                menor_diferencia = diferencia
                mejor_particion = part

    if mejor_particion:
        if mejor_particion['tamano'] > proceso['tamano']:
            nueva_part = {
                'id_part': next_part_id,
                'inicio': mejor_particion['inicio'] + proceso['tamano'],
                'tamano': mejor_particion['tamano'] - proceso['tamano'],
                'estado': 'Libre',
                'pid': None,
                'frag_interna': 0
            }
            next_part_id += 1
            particiones.append(nueva_part)
            
        mejor_particion['tamano'] = proceso['tamano']
        mejor_particion['estado'] = 'Ocupado'
        mejor_particion['pid'] = proceso['pid']
        
        particiones.sort(key=lambda x: x['inicio'])
        return True
    return False

def liberar_memoria(proceso):
    """Libera la partición correspondiente al proceso que finalizó."""
    for part in particiones:
        if part['pid'] == proceso['pid']:
            part['estado'] = 'Libre'
            part['pid'] = None
            break
    unificar_particiones_libres()

def unificar_particiones_libres():
    """Fusiona huecos contiguos libres en la memoria."""
    global particiones
    particiones.sort(key=lambda x: x['inicio'])
    i = 0
    while i < len(particiones) - 1:
        if particiones[i]['estado'] == 'Libre' and particiones[i+1]['estado'] == 'Libre':
            particiones[i]['tamano'] += particiones[i+1]['tamano']
            del particiones[i+1]
        else:
            i += 1

def imprimir_estado(evento):
    """Muestra el estado actual del reloj, CPU, particiones de memoria y colas."""
    print(f"\n--- TIEMPO {reloj}: {evento} ---")
    if ejecucion is not None:
        print(f"PROCESADOR: Ejecutando Proceso {ejecucion['pid']} (Restante: {ejecucion['restante']})")
    else:
        print("PROCESADOR: Inactivo")
        
    print("\nTABLA DE PARTICIONES DE MEMORIA:")
    print(f"{'ID Part':<10} | {'Inicio':<10} | {'Tamaño':<10} | {'Proceso ID':<12} | {'Frag. Interna':<15}")
    print("-" * 65)
    for p in particiones:
        pid_str = str(p['pid']) if p['pid'] is not None else "-"
        print(f"{p['id_part']:<10} | {p['inicio']:<10} | {p['tamano']:<10} | {pid_str:<12} | {p['frag_interna']:<15}")

    print("\nESTADO DE COLAS:")
    listos = [str(p['pid']) for p in cola_listos]
    listos_susp = [str(p['pid']) for p in cola_listos_susp]
    print(f"Listos            : [{', '.join(listos)}]")
    print(f"Listos/Suspendidos: [{', '.join(listos_susp)}]")
    print("==================================================")

def buscar_menor_srtf():
    """Busca en la cola de listos el proceso con el menor tiempo restante (SRTF)."""
    menor = None
    for p in cola_listos:
        if menor is None or p['restante'] < menor['restante']:
            menor = p
    return menor

def gestionar_finalizacion():
    """Subacción: Verifica si el proceso en ejecución terminó y libera sus recursos."""
    global ejecucion
    if ejecucion is not None and ejecucion['restante'] == 0:
        liberar_memoria(ejecucion)
        ejecucion['estado'] = 'Terminado'
        ejecucion['finalizacion'] = reloj
        ejecucion['retorno'] = ejecucion['finalizacion'] - ejecucion['arribo']
        ejecucion['espera'] = ejecucion['retorno'] - ejecucion['irrupcion']
        terminados.append(ejecucion)
        
        evento_desc = f"Terminó Proceso {ejecucion['pid']}"
        ejecucion = None
        return True, evento_desc
    return False, ""

def gestionar_suspendidos():
    """Subacción: Intenta reingresar procesos de Listo/Suspendido a Listos si hay memoria."""
    susp_a_remover = []
    for p in cola_listos_susp:
        if asignar_memoria_best_fit(p):
            p['estado'] = 'Listo'
            cola_listos.append(p)
            susp_a_remover.append(p)
    for p in susp_a_remover:
        cola_listos_susp.remove(p)

def gestionar_arribos():
    """Subacción: Maneja la llegada de nuevos procesos al tiempo actual del reloj."""
    global procesos_nuevos
    nuevos_llegados = [p for p in procesos_nuevos if p['arribo'] == reloj]
    imprimir = False
    eventos = []

    for p in nuevos_llegados:
        if contar_procesos_activos() < 5:
            if asignar_memoria_best_fit(p):
                p['estado'] = 'Listo'
                cola_listos.append(p)
            else:
                p['estado'] = 'Listo/Suspendido'
                cola_listos_susp.append(p)
            eventos.append(f"Arribo {p['pid']}")
            imprimir = True
            procesos_nuevos.remove(p)
        else:
            p['arribo'] += 1

    return imprimir, ", ".join(eventos)

def aplicar_planificador_srtf():
    """Subacción: Aplica el algoritmo SRTF para asignación o desalojo en la CPU."""
    global ejecucion
    menor_listo = buscar_menor_srtf()
    if menor_listo is not None:
        if ejecucion is None:
            ejecucion = menor_listo
            cola_listos.remove(menor_listo)
            ejecucion['estado'] = 'Ejecucion'
        elif menor_listo['restante'] < ejecucion['restante']:
            ejecucion['estado'] = 'Listo'
            cola_listos.append(ejecucion)
            ejecucion = menor_listo
            cola_listos.remove(menor_listo)
            ejecucion['estado'] = 'Ejecucion'

def ejecutar_ciclo_reloj():
    """Subacción central que coordina todas las operaciones de un ciclo de reloj."""
    global reloj, ejecucion
    imprimir, evento_fin = gestionar_finalizacion()
    evento_desc = evento_fin if imprimir else ""

    gestionar_suspendidos()

    imp_arribo, evento_arr = gestionar_arribos()
    if imp_arribo:
        imprimir = True
        evento_desc = f"{evento_desc}, {evento_arr}" if evento_desc else evento_arr

    aplicar_planificador_srtf()

    if imprimir:
        imprimir_estado(evento_desc)

    if ejecucion is not None:
        ejecucion['restante'] -= 1
        
    reloj += 1

def simular():
    """Bucle principal que ejecuta los ciclos hasta que todos los procesos terminen."""
    if len(procesos_nuevos) == 0:
        print("\n[Aviso] No hay procesos cargados para simular.")
        return
    
    total_procesos = len(procesos_nuevos) + len(terminados)
    while len(terminados) < total_procesos:
        ejecutar_ciclo_reloj()

    mostrar_informe_final()

def mostrar_informe_final():
    """Calcula y muestra las estadísticas finales y el rendimiento del sistema."""
    print("\n\n" + "="*50)
    print("            INFORME ESTADÍSTICO FINAL")
    print("="*50)
    print(f"{'PID':<5} | {'Retorno (TR)':<15} | {'Espera (TE)':<15}")
    print("-" * 40)
    
    suma_retorno = 0
    suma_espera = 0
    
    terminados.sort(key=lambda x: x['pid'])
    for p in terminados:
        print(f"{p['pid']:<5} | {p['retorno']:<15} | {p['espera']:<15}")
        suma_retorno += p['retorno']
        suma_espera += p['espera']
        
    total_t = len(terminados)
    prom_retorno = suma_retorno / total_t if total_t > 0 else 0
    prom_espera = suma_espera / total_t if total_t > 0 else 0
    rendimiento = total_t / reloj if reloj > 0 else 0
    
    print("-" * 40)
    print(f"Tiempo Promedio de Retorno : {prom_retorno:.2f} ut")
    print(f"Tiempo Promedio de Espera  : {prom_espera:.2f} ut")
    print(f"Rendimiento del Sistema    : {rendimiento:.4f} trabajos/ut")
    print("="*50)

def mostrar_menu():
    """Interfaz interactiva sencilla en consola por medio de un menú."""
    while True:
        print("\n==================================================")
        print("   SIMULADOR MVT Y SRTF (ESTRUCTURADO)")
        print("==================================================")
        print("1. Cargar archivo de procesos")
        print("2. Iniciar simulación")
        print("3. Salir")
        print("--------------------------------------------------")
        
        opcion = input("Seleccione una opción (1-3): ").strip()
        
        if opcion == '1':
            inicializar_sistema()
            archivo = input("Ingrese el nombre o ruta del archivo (ej. procesos.txt): ").strip()
            if not archivo:
                archivo = "procesos.txt"
            cargar_procesos(archivo)
            print(f"\n[Éxito] Procesos cargados correctamente desde '{archivo}'.")
            
        elif opcion == '2':
            if len(procesos_nuevos) == 0 and len(terminados) == 0:
                print("\n[Aviso] Debe cargar los procesos primero (Opción 1).")
            else:
                print("\n--- INICIANDO EJECUCIÓN DEL SIMULADOR ---")
                simular()
                
        elif opcion == '3':
            print("\n¡Gracias por usar el simulador! Saliendo...")
            sys.exit(0)
        else:
            print("\n[Error] Opción no válida. Ingrese un número entre 1 y 3.")

if __name__ == "__main__":
    mostrar_menu()