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