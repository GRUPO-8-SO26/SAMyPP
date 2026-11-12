# ==============================================================================
# MÓDULO: src/reloj.py
# DESCRIPCIÓN:
#   Encapsula y gobierna exclusivamente la variable temporal CLOCK del sistema.
#   Ningún otro módulo puede modificar directamente el reloj.
#
# VARIABLES GLOBALES TOCADAS:
#   - CLOCK (definida en este módulo; modificada por reset_clock y clocking;
#     leída por obtener_clock).
#
# VARIABLES LOCALES CREADAS:
#   - unidades (parámetro de clocking).
#
# OTROS BLOQUES O FUNCIONES USADAS (EXTERNAS / INTERNAS):
#   - Ninguna (módulo autocontenido).
# ==============================================================================

CLOCK = 0


def reset_clock():
    """Pone la variable global CLOCK en cero."""
    global CLOCK
    CLOCK = 0


def clocking(unidades=1):
    """Avanza el CLOCK una cantidad entera de unidades de tiempo."""
    global CLOCK
    if unidades > 0:
        CLOCK += unidades


def obtener_clock():
    """Devuelve el valor actual del CLOCK."""
    return CLOCK