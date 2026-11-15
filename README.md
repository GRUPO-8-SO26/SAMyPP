# SAMyPP — Simulador de Asignación de Memoria y Planificación de Procesos

**Trabajo Práctico Integrador — Sistemas Operativos (2026)**  
**Universidad Tecnológica Nacional — Facultad Regional Resistencia (UTN FRRe)**  
**Grupo N° 8**

---

## Integrantes del Grupo 8

* Burgos Kaenel, Guido Martin
* Dos Santo, Ayel Daniela
* González, María Teresa
* Marín Sosa, José Manuel
* Pastori, Jose María
* Retamozo Cabaña, Ivo Luciano Emanuel
* Saleh, Maximo

---

## Descripción del Proyecto

**SAMyPP** es un simulador de consola desarrollado en **Python bajo paradigma de programación estructurada** que modela de manera conjunta la administración de Memoria Central y la planificación de CPU de un Sistema Operativo:

* **Gestión de Memoria:** Particiones Variables (**MVT**) sin compactación, con política de asignación **Best-Fit** (Mejor Ajuste).
* **Planificación de CPU:** **SRTF** (*Shortest Remaining Time First*) apropiativo con desempate por menor tiempo de arribo (`proc_ta`).
* **Parámetros y Restricciones del Sistema:**
  * **Memoria Central Total:** `550K` (`100K` reservados para el Sistema Operativo `#` + `450K` disponibles para procesos de usuario `~`).
  * **Carga Máxima:** Hasta `10` procesos válidos por lote desde archivo CSV.
  * **Grado de Multiprogramación:** Máximo `5` procesos activos simultáneamente en el sistema (`En Ejecución + Listos + Listos/Suspendidos`).
  * **Control Temporal:** Gobernado exclusivamente por la variable `CLOCK` a través de las funciones `reset_clock()` y `clocking(unidades)`.

---

## Arquitectura del Repositorio

El código está organizado en bloques funcionales independientes dentro de `src/`, coordinados desde el punto de entrada `main.py`:

```text
SAMyPP/
├── main.py                  # Punto de entrada, menú principal y bucle de simulación por eventos
├── README.md                # Documentación general y guía de ejecución (How-To)
├── LICENSE                  # Licencia del proyecto
├── .gitignore               # Exclusión de borradores locales y artefactos de compilación
├── data/
│   └── procesos.csv         # Archivo de entrada con el lote de procesos a simular
├── docs/
│   └── definiciones_disenio.md # Decisiones de diseño, convenciones y criterios de desempate
└── src/
    ├── __init__.py          # Inicialización del paquete src
    ├── config.py            # Constantes del sistema, símbolos visuales e índices de proceso
    ├── reloj.py             # Encapsulamiento del reloj global (CLOCK, clocking, reset_clock)
    ├── estado.py            # Memoria central, colas de estados (PROEST_*) y tabla estadística
    ├── carga.py             # Lectura, validación y ordenamiento de procesos desde CSV
    ├── memoria.py           # Algoritmo Best-Fit, liberación contigua y tabla de particiones MVT
    ├── admision.py          # Admisión de nuevos arribos y reingreso desde Listo/Suspendido
    ├── planificador.py      # Planificador a corto plazo SRTF con desalojo y ejecución por ciclo
    ├── salida.py            # Renderizado por consola, mapa visual alineado y pausas por evento
    └── estadisticas.py      # Cálculo de tiempos de retorno, espera y rendimiento del sistema