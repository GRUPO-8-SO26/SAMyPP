from src.config import IDX_ID, IDX_TA, IDX_TI, IDX_TAM, IDX_RESTANTE, IDX_DIR, IDX_FIN
from src.estado import PROEST_listo, PROEST_raning, PROEST_finished, DATOS_ESTADISTICOS
from src.memoria import liberar_memoria
from src.reloj import obtener_clock


def _buscar_indice_menor_srtf():
    """Retorna el índice en PROEST_listo del proceso con menor tiempo restante.
    Criterio de desempate: menor tiempo de arribo (proc_ta).
    """
    idx_mejor = 0
    for idx in range(1, len(PROEST_listo)):
        actual = PROEST_listo[idx]
        mejor = PROEST_listo[idx_mejor]
        if actual[IDX_RESTANTE] < mejor[IDX_RESTANTE]:
            idx_mejor = idx
        elif actual[IDX_RESTANTE] == mejor[IDX_RESTANTE] and actual[IDX_TA] < mejor[IDX_TA]:
            idx_mejor = idx
    return idx_mejor


def planificar_srtf():
    """Asigna la CPU al proceso más corto o realiza el desalojo si corresponde."""
    if not PROEST_listo:
        return

    idx_mejor = _buscar_indice_menor_srtf()
    candidato = PROEST_listo[idx_mejor]

    if not PROEST_raning:
        PROEST_raning.append(PROEST_listo.pop(idx_mejor))
        print(f"[CPU] Proceso '{candidato[IDX_ID]}' ingresa a EJECUCIÓN (Restante: {candidato[IDX_RESTANTE]} ut).")
    else:
        en_ejecucion = PROEST_raning[0]
        if candidato[IDX_RESTANTE] < en_ejecucion[IDX_RESTANTE]:
            print(
                f"[DESALOJO] Proceso '{candidato[IDX_ID]}' ({candidato[IDX_RESTANTE]} ut) desaloja a "
                f"'{en_ejecucion[IDX_ID]}' ({en_ejecucion[IDX_RESTANTE]} ut)."
            )
            PROEST_listo.append(PROEST_raning.pop(0))
            # Como se agregó un elemento al final, volvemos a buscar el mejor para extraerlo limpio
            idx_mejor = _buscar_indice_menor_srtf()
            PROEST_raning.append(PROEST_listo.pop(idx_mejor))


def ejecutar_unidad_cpu():
    """Ejecuta 1 unidad de tiempo del proceso en CPU.
    Retorna True si el proceso finalizó en este ciclo, False en caso contrario.
    """
    if not PROEST_raning:
        return False

    proc = PROEST_raning[0]
    proc[IDX_RESTANTE] -= 1

    if proc[IDX_RESTANTE] == 0:
        tiempo_fin = obtener_clock() + 1
        proc[IDX_FIN] = tiempo_fin
        retorno = tiempo_fin - proc[IDX_TA]
        espera = retorno - proc[IDX_TI]

        DATOS_ESTADISTICOS.append(
            [proc[IDX_ID], proc[IDX_TA], proc[IDX_TI], proc[IDX_TAM], retorno, espera]
        )

        liberar_memoria(proc[IDX_DIR], proc[IDX_TAM])
        PROEST_finished.append(PROEST_raning.pop(0))
        print(f"[EVENTO] Proceso '{proc[IDX_ID]}' FINALIZÓ en t={tiempo_fin} y liberó {proc[IDX_TAM]}K.")
        return True

    return False