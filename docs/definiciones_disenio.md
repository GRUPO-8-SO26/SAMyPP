## PROGRAMACION:
-Estructurada.
-Funciones en Bloques Independientes.

## DE LOS PROCESOS DE ENTRADA
Se definen en un archivo .csv de entrada, con los siguientes campos:
- ***proc_id***: identificador unico del proceso, falta definir formato (numerico consecutivo, combinacion de letras/numeros, etc)
- ***proc_ta***: Tiempo de Arribo del Proceso. Unidades ENTERAS. representa la "unidad de tiempo" en la que el proceso debe intentar pasar de nuevo a listo.
- ***proc_ti***: Tiempo de Irrupcion del Proceso. Unidades ENTERAS. Representa el tiempo en unidades de tiempo que el proceso necesita para ejecutarse.
- ***proc_tam***: Tamaño del Proceso. Unidades ENTERAS. Representa la cantidad de palabras de memoria que el proceso necesita para alojarse en la Memoria Central. Expresado en "miles de palabras", de modo que un proceso de 15000 palabras se ingresa como "15".

## DEL ARCHIVO DE ENTRADA
Los procesos del archivo de entrada deben pasar por un proceso de validacion, antes de ser asignados a la cola de nuevos.
Validar:
- Campos de entrada cumplan las restricciones de tipo de datos.
- *proc_tam* no puede ser mayor al espacio asignado para el usuario en Memoria Central.
- Cantidad maxima de 10 procesos "validos". Descartar los invalidos y mostrar en pantalla los rechazados y su motivo.

## DE LA DEFINICION DEL TIEMPO
El tiempo en el simulador es gobernado por una variable llamada "CLOCK"
Como definicion general, ninguna funcion o accion debe modificar directamente esta variable.
La Variable CLOCK solo puede ser alterada por las funciones:
- ***clocking(unidades)***: funcion para avanza el "clock" una cantidad de "unidades" de tiempo.
- ***reset_clock()***: funcion que pone el clock en cero.

## DE LOS ESTADOS DE PROCESOS
Se definen los nombres de los estados de los procesos, cada uno sería el nombre del puntero de la lista que contendra cada uno de los procesos.
Los mismos son:
- ***PROEST_nuevo***: Estado "nuevo", se toma por la carga de los procesos desde el csv de procesos de entrada. Solo se asignan procesos que cumplieron las validaciones.
- ***PROEST_listo***: Estado "listo", son los procesos que llegaron al tiempo de de arribo, y tenian espacio para ser asignados a la memoria central
- ***PROEST_lisus***: Estado "Listo y Suspendido", son los procesos que llegaron al tiempo de arribo, y NO tenian espacio en memoria central para ser asignados.
- ***PROEST_raning***: Estado "En ejecucion", es el proceso que esta siendo ejecutado por el procesador. solo puede haber 1 proceso en esta lista en una misma unidad de tiempo.
- ***PROEST_finished***: Estado "Terminado", no existe como tal en términos teoricos, pero lo creamos para listar los procesos ya finalizados que salieron de memoria, para facilitar debugueos y controles estadisticos.
