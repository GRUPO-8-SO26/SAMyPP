def limpiar_pantalla():
    """Limpia la pantalla de la consola según el sistema operativo."""
    os.system("cls" if os.name == "nt" else "clear")

def mapa_MC(mc):
    """Muestra los elementos de la memoria central en filas de 25 columnas."""
    for i in range(0, len(mc), 25):
        fila = mc[i : i + 25]  # Toma un segmento de 25 posiciones
        print(" ".join(fila))  # Imprime los elementos separados por espacios