import sys

class Proceso:
    def __init__(self, pid, tamano, arribo, irrupcion):
        self.pid = pid
        self.tamano = tamano
        self.arribo = arribo
        self.irrupcion = irrupcion
        self.restante = irrupcion
        self.estado = "Nuevo"
        self.retorno = 0
        self.espera = 0
        self.finalizacion = 0  

class Particion:
    def __init__(self, id_part, inicio, tamano, estado="Libre", pid=None):
        self.id_part = id_part
        self.inicio = inicio
        self.tamano = tamano
        self.estado = estado
        self.pid = pid
        # En particiones variables (MVT), se asigna el tamaño exacto, 
        # dejando el resto como un nuevo hueco libre. Por ende, no hay fragmentación interna.
        self.frag_interna = 0 

class Simulador:
    def __init__(self):
        self.reloj = 0
        self.procesos_nuevos = []
        self.cola_listos = []
        self.cola_listos_susp = []
        self.ejecucion = None
        self.terminados = []
        
        # Inicialización de memoria (100K SO, 450K Usuario)
        self.particiones = [
            Particion(0, 0, 100, "Ocupado", "SO"),
            Particion(1, 100, 450, "Libre", None)
        ]
        self.next_part_id = 2

    def cargar_procesos(self, archivo):
        try:
            with open(archivo, 'r') as f:
                for linea in f:
                    if linea.strip():
                        datos = linea.split(',')
                        p = Proceso(int(datos[0]), int(datos[1]), int(datos[2]), int(datos[3]))
                        self.procesos_nuevos.append(p)
            self.procesos_nuevos.sort(key=lambda x: x.arribo)
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo {archivo}")
            sys.exit(1)

    def procesos_activos(self):
        activos = len(self.cola_listos) + len(self.cola_listos_susp)
        if self.ejecucion:
            activos += 1
        return activos

    def asignar_memoria_best_fit(self, proceso):
        mejor_particion = None
        menor_diferencia = float('inf')

        # Algoritmo Best-Fit
        for part in self.particiones:
            if part.estado == "Libre" and part.tamano >= proceso.tamano:
                diferencia = part.tamano - proceso.tamano
                if diferencia < menor_diferencia:
                    menor_diferencia = diferencia
                    mejor_particion = part

        if mejor_particion:
            # División de partición (MVT)
            if mejor_particion.tamano > proceso.tamano:
                nueva_part = Particion(
                    self.next_part_id, 
                    mejor_particion.inicio + proceso.tamano, 
                    mejor_particion.tamano - proceso.tamano
                )
                self.next_part_id += 1
                self.particiones.append(nueva_part)
                
            mejor_particion.tamano = proceso.tamano
            mejor_particion.estado = "Ocupado"
            mejor_particion.pid = proceso.pid
            
            # Reordenar tabla por dirección de memoria
            self.particiones.sort(key=lambda x: x.inicio)
            return True
        return False

    def liberar_memoria(self, proceso):
        for part in self.particiones:
            if part.pid == proceso.pid:
                part.estado = "Libre"
                part.pid = None
                break
        self.unificar_particiones_libres()

    def unificar_particiones_libres(self):
        self.particiones.sort(key=lambda x: x.inicio)
        i = 0
        while i < len(self.particiones) - 1:
            if self.particiones[i].estado == "Libre" and self.particiones[i+1].estado == "Libre":
                self.particiones[i].tamano += self.particiones[i+1].tamano
                del self.particiones[i+1]
            else:
                i += 1

    def imprimir_estado(self, evento):
        print(f"\n--- TIEMPO {self.reloj}: {evento} ---")
        if self.ejecucion:
            print(f"PROCESADOR: Ejecutando Proceso {self.ejecucion.pid} (Restante: {self.ejecucion.restante})")
        else:
            print("PROCESADOR: Inactivo")
            
        print("\nTABLA DE PARTICIONES DE MEMORIA:")
        print(f"{'ID Part':<10} | {'Inicio':<10} | {'Tamaño':<10} | {'Proceso ID':<12} | {'Frag. Interna':<15}")
        print("-" * 65)
        for p in self.particiones:
            pid_str = str(p.pid) if p.pid else "-"
            print(f"{p.id_part:<10} | {p.inicio:<10} | {p.tamano:<10} | {pid_str:<12} | {p.frag_interna:<15}")

        print("\nESTADO DE COLAS:")
        listos = [str(p.pid) for p in self.cola_listos]
        listos_susp = [str(p.pid) for p in self.cola_listos_susp]
        print(f"Listos            : [{', '.join(listos)}]")
        print(f"Listos/Suspendidos: [{', '.join(listos_susp)}]")
        print("==================================================")

    def buscar_menor_srtf(self):
        menor = None
        # Recorrido sin reordenamiento físico
        for p in self.cola_listos:
            if menor is None or p.restante < menor.restante:
                menor = p
        return menor

    def simular(self):
        total_procesos = len(self.procesos_nuevos)
        
        while len(self.terminados) < total_procesos:
            imprimir = False
            evento_desc = ""

            # 1. Liberar proceso en ejecución si terminó
            if self.ejecucion and self.ejecucion.restante == 0:
                self.liberar_memoria(self.ejecucion)
                self.ejecucion.estado = "Terminado"
                self.ejecucion.finalizacion = self.reloj
                self.ejecucion.retorno = self.ejecucion.finalizacion - self.ejecucion.arribo
                self.ejecucion.espera = self.ejecucion.retorno - self.ejecucion.irrupcion
                self.terminados.append(self.ejecucion)
                
                evento_desc = f"Terminó Proceso {self.ejecucion.pid}"
                self.ejecucion = None
                imprimir = True

            # 2. Transición Listo/Suspendido -> Listo
            # Se evalúa si hay memoria disponible para los suspendidos
            susp_a_remover = []
            for p in self.cola_listos_susp:
                if self.asignar_memoria_best_fit(p):
                    p.estado = "Listo"
                    self.cola_listos.append(p)
                    susp_a_remover.append(p)
            for p in susp_a_remover:
                self.cola_listos_susp.remove(p)

            # 3. Llegada de nuevos procesos al tiempo actual
            nuevos_llegados = [p for p in self.procesos_nuevos if p.arribo == self.reloj]
            for p in nuevos_llegados:
                if self.procesos_activos() < 5:
                    if self.asignar_memoria_best_fit(p):
                        p.estado = "Listo"
                        self.cola_listos.append(p)
                    else:
                        p.estado = "Listo/Suspendido" 
                        self.cola_listos_susp.append(p)
                    evento_desc = f"Arribo Proceso {p.pid}" if not evento_desc else evento_desc + f", Arribo {p.pid}"
                    imprimir = True
                    self.procesos_nuevos.remove(p)
                else:
                    # Si ya hay 5 activos, se retrasa su ingreso al sistema
                    p.arribo += 1 

            # 4. Planificador SRTF (Desalojo / Cambio de contexto)
            menor_listo = self.buscar_menor_srtf()
            if menor_listo:
                if self.ejecucion is None:
                    self.ejecucion = menor_listo
                    self.cola_listos.remove(menor_listo)
                    self.ejecucion.estado = "Ejecucion"
                elif menor_listo.restante < self.ejecucion.restante:
                    # Desalojo
                    self.ejecucion.estado = "Listo"
                    self.cola_listos.append(self.ejecucion)
                    self.ejecucion = menor_listo
                    self.cola_listos.remove(menor_listo)
                    self.ejecucion.estado = "Ejecucion"

            # 5. Imprimir estado si hubo arribos o terminaciones
            if imprimir:
                self.imprimir_estado(evento_desc)

            # 6. Avanzar Reloj y ejecutar
            if self.ejecucion:
                self.ejecucion.restante -= 1
                
            self.reloj += 1

        self.mostrar_informe_final()

    def mostrar_informe_final(self):
        print("\n\n" + "="*50)
        print("          INFORME ESTADÍSTICO FINAL")
        print("="*50)
        print(f"{'PID':<5} | {'Retorno (TR)':<15} | {'Espera (TE)':<15}")
        print("-" * 40)
        
        suma_retorno = 0
        suma_espera = 0
        
        # Ordenar para presentación
        self.terminados.sort(key=lambda x: x.pid)
        for p in self.terminados:
            print(f"{p.pid:<5} | {p.retorno:<15} | {p.espera:<15}")
            suma_retorno += p.retorno
            suma_espera += p.espera
            
        prom_retorno = suma_retorno / len(self.terminados)
        prom_espera = suma_espera / len(self.terminados)
        rendimiento = len(self.terminados) / self.reloj
        
        print("-" * 40)
        print(f"Tiempo Promedio de Retorno : {prom_retorno:.2f} ut")
        print(f"Tiempo Promedio de Espera  : {prom_espera:.2f} ut")
        print(f"Rendimiento del Sistema    : {rendimiento:.4f} trabajos/ut")
        print("="*50)

if __name__ == "__main__":
    simulador = Simulador()
    simulador.cargar_procesos("procesos.txt")
    simulador.simular()

