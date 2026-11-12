import csv
import os
from src.config import TAM_USUARIO, MAX_PROCESOS_VALIDOS, IDX_TA
from src.estado import PROEST_nuevo


def _validar_y_agregar_proceso(raw_id, raw_ta, raw_ti, raw_tam, ids_registrados):
    """Valida los 4 campos de un proceso y, si cumple, lo agrega a PROEST_nuevo."""
    proc_id = str(raw_id).strip()
    if not proc_id:
        print("Rechazado: el 'proc_id' no puede estar vacío.")
        return False

    if proc_id in ids_registrados:
        print(f"Proceso '{proc_id}' rechazado: identificador duplicado.")
        return False

    try:
        proc_ta = int(str(raw_ta).strip())
        proc_ti = int(str(raw_ti).strip())
        proc_tam = int(str(raw_tam).strip())
    except ValueError:
        print(f"Proceso '{proc_id}' rechazado: ta, ti y tam deben ser números enteros.")
        return False

    if proc_ta < 0:
        print(f"Proceso '{proc_id}' rechazado: el tiempo de arribo ({proc_ta}) no puede ser negativo.")
        return False

    if proc_ti <= 0:
        print(f"Proceso '{proc_id}' rechazado: el tiempo de irrupción ({proc_ti}) debe ser mayor a 0.")
        return False

    if proc_tam <= 0 or proc_tam > TAM_USUARIO:
        print(
            f"Proceso '{proc_id}' rechazado: tamaño ({proc_tam}K) fuera del rango permitido (1K a {TAM_USUARIO}K)."
        )
        return False

    if len(PROEST_nuevo) >= MAX_PROCESOS_VALIDOS:
        print(f"Proceso '{proc_id}' rechazado: se alcanzó el máximo de {MAX_PROCESOS_VALIDOS} procesos válidos.")
        return False

    # Estructura: [proc_id, proc_ta, proc_ti, proc_tam, tiempo_restante, dir_memoria, tiempo_fin]
    proceso = [proc_id, proc_ta, proc_ti, proc_tam, proc_ti, -1, -1]
    PROEST_nuevo.append(proceso)
    ids_registrados.add(proc_id)
    print(f"Proceso '{proc_id}' válido -> TA: {proc_ta} | TI: {proc_ti} | TAM: {proc_tam}K.")
    return True


def cargar_desde_csv(ruta_archivo):
    """Lee y valida procesos desde un archivo CSV con columnas: proc_id, proc_ta, proc_ti, proc_tam."""
    if not os.path.exists(ruta_archivo):
        print(f"Error: No se encontró el archivo '{ruta_archivo}'.")
        return False

    ids_registrados = set()
    try:
        with open(ruta_archivo, mode="r", encoding="utf-8-sig") as archivo:
            lector = csv.DictReader(archivo)
            columnas_requeridas = {"proc_id", "proc_ta", "proc_ti", "proc_tam"}
            if not lector.fieldnames or not columnas_requeridas.issubset(
                {c.strip() for c in lector.fieldnames}
            ):
                print("Error: El CSV debe tener las columnas: proc_id, proc_ta, proc_ti, proc_tam")
                return False

            for fila in lector:
                # Normalizar claves por si hay espacios en el encabezado
                fila_limpia = {k.strip(): v for k, v in fila.items()}
                _validar_y_agregar_proceso(
                    fila_limpia["proc_id"],
                    fila_limpia["proc_ta"],
                    fila_limpia["proc_ti"],
                    fila_limpia["proc_tam"],
                    ids_registrados,
                )

        PROEST_nuevo.sort(key=lambda p: p[IDX_TA])
        return len(PROEST_nuevo) > 0

    except Exception as e:
        print(f"Error al procesar el archivo CSV: {e}")
        return False


def cargar_manual():
    """Permite al usuario ingresar procesos por teclado hasta un máximo de 10 válidos."""
    ids_registrados = set()
    print(f"\n--- CARGA MANUAL DE PROCESOS (Máximo {MAX_PROCESOS_VALIDOS} válidos) ---")

    while len(PROEST_nuevo) < MAX_PROCESOS_VALIDOS:
        opcion = input(
            f"\nProcesos válidos cargados: {len(PROEST_nuevo)}/{MAX_PROCESOS_VALIDOS}. ¿Agregar proceso? (s/n): "
        ).strip().lower()
        if opcion != "s":
            break

        raw_id = input("  proc_id (ej. P1): ")
        raw_ta = input("  proc_ta (tiempo de arribo, entero >= 0): ")
        raw_ti = input("  proc_ti (tiempo de irrupción, entero > 0): ")
        raw_tam = input(f"  proc_tam (tamaño en K, entero 1..{TAM_USUARIO}): ")

        _validar_y_agregar_proceso(raw_id, raw_ta, raw_ti, raw_tam, ids_registrados)

    PROEST_nuevo.sort(key=lambda p: p[IDX_TA])
    return len(PROEST_nuevo) > 0