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


## Pantalla inicial del programa.
def pantalla_inicio():
    limpiar_pantalla()
    print("  ██=============================================██  ")
    print("  ||                                             ||  ")
    print("  ||      UNIVERSIDAD TECNOLOGICA NACIONAL       ||  ")
    print("  ||       FACULTAD REGIONAL RESISTENCIA         ||  ")
    print("  ||                                             ||  ")
    print("  ||                                             ||  ")
    print("  ||                                             ||  ")
    print("  ||             Sistemas Operativos             ||  ")
    print("  ||      Trabajo Práctico Integrador 2026       ||  ")
    print("  ||           Equipo 8 - Turno Tarde            ||  ")
    print("  ||                                             ||  ")
    print("  ██=============================================██  ")
    pausar()

## Pantalla final del programa.
def pantalla_final():
    limpiar_pantalla()
    print("  ██==============================================██  ")
    print("  ||░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░||  ")
    print("  ||░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░||  ")
    print("  ||░░░░░░░░░░░░░░░░▄░░░░░▄▄░░░░░▄░░░░░░░░░░░░░░░░||  ")
    print("  ||░░░░░░░░░░░░░░░░▀█░░░░██░░░░█▀░░░░░░░░░░░░░░░░||  ")
    print("  ||░░░░░░░░░░░░░░░░░▀█▄▄░██░▄▄█▀░░░░░░░░░░░░░░░░░||  ")
    print("  ||░░░░░░░░░░░░░░░░░░░░█▄██▄█░░░░░░░░░░░░░░░░░░░░||  ")
    print("  ||░░░░░░░░░░░░░░░░██████████████░░░░░░░░░░░░░░░░||  ")
    print("  ||░░░░░░░░░░░░░░░░░░░░█▀██▀█░░░░░░░░░░░░░░░░░░░░||  ")
    print("  ||░░░░░░░░░░░░░░░░░▄█▀▀░██░▀▀█▄░░░░░░░░░░░░░░░░░||  ")
    print("  ||░░░░░░░░░░░░░░░░▄█░░░░██░░░░█▄░░░░░░░░░░░░░░░░||  ")
    print("  ||░░░░░░░░░░░░░░░░▀░░░░░▀▀░░░░░▀░░░░░░░░░░░░░░░░||  ")
    print("  ||░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░||  ")
    print("  ||░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░||  ")
    print("  ||░░░░░╔╗░╔╦════╦═╗░╔╗░░░░╔═══╦═══╦═══╦═══╗░░░░░||  ")
    print("  ||░░░░░║║░║║╔╗╔╗║║╚╗║║░░░░║╔══╣╔═╗║╔═╗║╔══╝░░░░░||  ")
    print("  ||░░░░░║║░║╠╝║║╚╣╔╗╚╝║░░░░║╚══╣╚═╝║╚═╝║╚══╗░░░░░||  ")
    print("  ||░░░░░║║░║║░║║░║║╚╗║║╔══╗║╔══╣╔╗╔╣╔╗╔╣╔══╝░░░░░||  ")
    print("  ||░░░░░║╚═╝║░║║░║║░║║║╚══╝║║░░║║║╚╣║║╚╣╚══╗░░░░░||  ")
    print("  ||░░░░░╚═══╝░╚╝░╚╝░╚═╝░░░░╚╝░░╚╝╚═╩╝╚═╩═══╝░░░░░||  ")
    print("  ||░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░||  ")
    print("  ||░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░||  ")
    print("  ██==============================================██  ")
    #print("  ██==============================================██  ")
    print("  ||                                              ||  ")
    print("  ||      UNIVERSIDAD TECNOLOGICA NACIONAL        ||  ")
    print("  ||       FACULTAD REGIONAL RESISTENCIA          ||  ")
    print("  ||                                              ||  ")
    print("  ||             Sistemas Operativos              ||  ")
    print("  ||         Trabajo Práctico Integrador          ||  ")
    print("  ||                                              ||  ")
    print("  ||                    2026                      ||  ")
    print("  ||                                              ||  ")
    print("  ||         - Equipo 8 - Turno Tarde -           ||  ")
    print("  ||     Integrantes:                             ||  ")
    print("  ||     Burgos Kaenel, Guido Martin              ||  ")
    print("  ||     Dos Santo, Ayel Daniela                  ||  ")
    print("  ||     González, María Teresa                   ||  ")
    print("  ||     Marín Sosa, José Manuel                  ||  ")
    print("  ||     Pastori, Jose María                      ||  ")
    print("  ||     Retamozo Cabaña, Ivo Luciano Emanuel     ||  ")
    print("  ||     Saleh, Maximo                            ||  ")
    print("  ||                                              ||  ")
    print("  ██==============================================██  ")
    input("\nPresione ENTER para finalizar.")

# Ejecución local para testing
if __name__ == "__main__":
    pantalla_inicio()
    pantalla_final()

