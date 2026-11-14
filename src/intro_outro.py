# ==============================================================================
# MÓDULO: src/intro_outro.py
# DESCRIPCIÓN:
#   Genera pantallas de presentacion y salida del programa.
#
# VARIABLES GLOBALES TOCADAS:
#   - Definidas y modificadas en este módulo:
#     
#   - Importadas:
#     
#
# VARIABLES LOCALES CREADAS:
#   - 
#
# OTROS BLOQUES O FUNCIONES USADAS (EXTERNAS / INTERNAS):
#   - 
# ==============================================================================

## Limpia pantalla
def limpiar_pantalla():
    # Funciona en la mayoría de los casos sin importar el SO
    import os
    os.system("cls" if os.name == "nt" else "clear")


## Pausa con msj
def pausar():
    input("\nPresione ENTER para continuar...")

## Logo inicio del programa
def pantalla_inicio():
    limpiar_pantalla()
    print("  ██=============================================██  ")
    print("  ||                                             ||  ")
    print("  ||                                             ||  ")
    print("  ||                                             ||  ")
    print("  ||                                             ||  ")
    print("  ||                                             ||  ")
    print("  ||                                             ||  ")
    print("  ||                                             ||  ")
    print("  ||                                             ||  ")
    print("  ||                                             ||  ")
    print("  ||                                             ||  ")
    print("  ██=============================================██  ")
    pausar()