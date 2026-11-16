import os
import time

## Limpiador de Pantalla
def limpiar_pantalla():
    # Funciona sin importar el SO (Windows, macOS o Linux)
    os.system("cls" if os.name == "nt" else "clear")

## Logos Estáticos
def Logo_UTN_arania():
    limpiar_pantalla()
    print(r"  ██==============================================██  ")
    print(r"  ||░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░||  ")
    print(r"  ||░░░░░░░░░░░░░░░░▄░░░░░▄▄░░░░░▄░░░░░░░░░░░░░░░░||  ")
    print(r"  ||░░░░░░░░░░░░░░░░▀█░░░░██░░░░█▀░░░░░░░░░░░░░░░░||  ")
    print(r"  ||░░░░░░░░░░░░░░░░░▀█▄▄░██░▄▄█▀░░░░░░░░░░░░░░░░░||  ")
    print(r"  ||░░░░░░░░░░░░░░░░░░░░█▄██▄█░░░░░░░░░░░░░░░░░░░░||  ")
    print(r"  ||░░░░░░░░░░░░░░░░██████████████░░░░░░░░░░░░░░░░||  ")
    print(r"  ||░░░░░░░░░░░░░░░░░░░░█▀██▀█░░░░░░░░░░░░░░░░░░░░||  ")
    print(r"  ||░░░░░░░░░░░░░░░░░▄█▀▀░██░▀▀█▄░░░░░░░░░░░░░░░░░||  ")
    print(r"  ||░░░░░░░░░░░░░░░░▄█░░░░██░░░░█▄░░░░░░░░░░░░░░░░||  ")
    print(r"  ||░░░░░░░░░░░░░░░░▀░░░░░▀▀░░░░░▀░░░░░░░░░░░░░░░░||  ")
    print(r"  ||░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░||  ")
    print(r"  ██==============================================██  ")
    print("\n          >> PRESIONA ENTER PARA INGRESAR <<          ")

def Logo_UTN_nombre():
    limpiar_pantalla()
    print(r"  ██==============================================██  ")
    print(r"  ||░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░||  ")
    print(r"  ||░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░||  ")
    print(r"  ||░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░||  ")
    print(r"  ||░░░░░╔╗░╔╦════╦═╗░╔╗░░░░╔═══╦═══╦═══╦═══╗░░░░░||  ")
    print(r"  ||░░░░░║║░║║╔╗╔╗║║╚╗║║░░░░║╔══╣╔═╗║╔═╗║╔══╝░░░░░||  ")
    print(r"  ||░░░░░║║░║╠╝║║╚╣╔╗╚╝║░░░░║╚══╣╚═╝║╚═╝║╚══╗░░░░░||  ")
    print(r"  ||░░░░░║║░║║░║║░║║╚╗║║╔══╗║╔══╣╔╗╔╣╔╗╔╣╔══╝░░░░░||  ")
    print(r"  ||░░░░░║╚═╝║░║║░║║░║║║╚══╝║║░░║║║╚╣║║╚╣╚══╗░░░░░||  ")
    print(r"  ||░░░░░╚═══╝░╚╝░╚╝░╚═╝░░░░╚╝░░╚╝╚═╩╝╚═╩═══╝░░░░░||  ")
    print(r"  ||░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░||  ")
    print(r"  ||░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░||  ")
    print(r"  ██==============================================██  ")
    print("\n          >> PRESIONA ENTER PARA INGRESAR <<          ")

## Detección de tecla Enter según el Sistema Operativo
if os.name == "nt":
    import msvcrt

    def esperar_con_deteccion(segundos):
        """Revisa cada 0.05 s si se presionó Enter en Windows."""
        pasos = int(segundos / 0.05)
        for _ in range(pasos):
            if msvcrt.kbhit():
                tecla = msvcrt.getch()
                if tecla in (b"\r", b"\n"):
                    return True
            time.sleep(0.05)
        return False
else:
    import sys
    import select

    def esperar_con_deteccion(segundos):
        """Revisa si se presionó Enter en macOS / Linux (UNIX)."""
        rlist, _, _ = select.select([sys.stdin], [], [], segundos)
        if rlist:
            sys.stdin.readline()
            return True
        return False

def logo_UTN_animado():
    while True:
        # 1. Mostrar logo araña
        limpiar_pantalla()
        Logo_UTN_arania()
        if esperar_con_deteccion(1.0):
            break

        # 2. Mostrar siglas UTN FRRe
        limpiar_pantalla()
        Logo_UTN_nombre()
        if esperar_con_deteccion(1.0):
            break

    limpiar_pantalla()
    print(r"<< Iniciando programa... >>")
    time.sleep(1)

if __name__ == "__main__":
    logo_UTN_animado()