def reset_clock():
    """Pone la variable global CLOCK en cero."""
    global CLOCK
    CLOCK = 0

def clocking(unidades):
    """Avanza el reloj del sistema una cantidad de 'unidades' de tiempo."""
    global CLOCK
    CLOCK += unidades # el reloj avanza en unidades de tiempo, el += es una forma de acortar la expresión CLOCK = CLOCK + unidades