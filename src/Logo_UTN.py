import time
import msvcrt # Librería nativa de Windows para detectar teclas sin congelar el programa

## Limpiador de Pantalla
def limpiar_pantalla():
    # Funciona en la mayoría de los casos sin importar el SO
    import os
    os.system("cls" if os.name == "nt" else "clear")

## Logos Estaticos
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

## Logos Dinamicos
def esperar_con_deteccion(segundos):
    """
    Revisa cada 0.05 segundos si el usuario presionó Enter para
    salir inmediatamente sin trabar la animación.
    """
    pasos = int(segundos / 0.05)
    for _ in range(pasos):
        if msvcrt.kbhit():  # ¿El usuario presionó una tecla?
            tecla = msvcrt.getch()
            if tecla == b'\r':  # b'\r' es la tecla Enter en bytes
                return True     # Señal de que queremos salir
        time.sleep(0.05)
    return False

def logo_UTN_animado():
    while True:
        # 1. Mostrar logo normal
        limpiar_pantalla()
        Logo_UTN_arania()
        
        # Espera 2 segundos (monitoreando si presionan Enter)
        if esperar_con_deteccion(1.0): 
            break

        # 2. Mostrar logo parpadeando
        limpiar_pantalla()
        Logo_UTN_nombre()
        
        # Espera 0.2 segundos (monitoreando si presionan Enter)
        if esperar_con_deteccion(1.0): 
            break

    # Al salir del bucle limpia y continúa al programa principal
    limpiar_pantalla()
    print(r"<< Iniciando programa... >>")
    time.sleep(1)

# Ejecución de logo UTN
if __name__ == "__main__":
    logo_UTN_animado()

