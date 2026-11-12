from src.config import MAX_PROCESOS_ACTIVOS, IDX_ID, IDX_TA, IDX_TAM, IDX_DIR
from src.estado import PROEST_nuevo, PROEST_listo, PROEST_lisus, contar_procesos_activos
from src.memoria import asignar_bestfit
from src.reloj import obtener_clock


def reingresar_suspendidos():
    """Intenta cargar en memoria procesos de PROEST_lisus mediante Best-Fit.
    Nota: estos procesos ya están contabilizados dentro del límite de 5 activos.
    """
    hubo_cambio = False
    i = 0
    while i < len(PROEST_lisus):
        proc = PROEST_lisus[i]
        dir_asignada = asignar_bestfit(proc[IDX_TAM], proc[IDX_ID])
        if dir_asignada != -1:
            proc[IDX_DIR] = dir_asignada
            PROEST_listo.append(proc)
            PROEST_lisus.pop(i)
            print(
                f"[EVENTO] Proceso '{proc[IDX_ID]}' reingresó de Listo/Susp a Listo (Dir: {dir_asignada})."
            )
            hubo_cambio = True
        else:
            i += 1
    return hubo_cambio


def admitir_nuevos():
    """Evalúa los procesos en PROEST_nuevo cuyo tiempo de arribo <= CLOCK actual."""
    hubo_arribo = False
    clock_actual = obtener_clock()
    i = 0

    while i < len(PROEST_nuevo):
        proc = PROEST_nuevo[i]
        if proc[IDX_TA] <= clock_actual:
            if contar_procesos_activos() >= MAX_PROCESOS_ACTIVOS:
                # Se alcanzó el grado máximo de multiprogramación (5 procesos activos)
                i += 1
                continue

            dir_asignada = asignar_bestfit(proc[IDX_TAM], proc[IDX_ID])
            if dir_asignada != -1:
                proc[IDX_DIR] = dir_asignada
                PROEST_listo.append(proc)
                PROEST_nuevo.pop(i)
                print(
                    f"[EVENTO] Arribó proceso '{proc[IDX_ID]}' -> Admitido en Memoria (Dir: {dir_asignada}) -> LISTO."
                )
            else:
                PROEST_lisus.append(proc)
                PROEST_nuevo.pop(i)
                print(
                    f"[EVENTO] Arribó proceso '{proc[IDX_ID]}' ({proc[IDX_TAM]}K) -> Sin hueco contiguo -> LISTO Y SUSPENDIDO."
                )
            hubo_arribo = True
        else:
            i += 1

    return hubo_arribo