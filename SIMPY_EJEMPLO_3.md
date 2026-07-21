# Ejemplo de Simulación 3: Proceso de Manufactura en Dos Etapas con Retrabajo

Este ejemplo avanza hacia un escenario industrial más realista y complejo. Modela una línea de manufactura secuencial de dos etapas (**Ensamblado** e **Inspección**) con un ciclo de retroalimentación (**retrabajo** o reparación) para las piezas defectuosas.

---

## 1. Planteamiento del Problema

- **Llegada de Materiales:** Las piezas de metal en bruto llegan al taller con un tiempo entre arribos que sigue una distribución exponencial con media de **6.0 minutos**.
- **Etapa 1 (Ensamble):** Cada pieza debe pasar por una máquina de ensamblado (capacidad = 1 recurso compartido). El tiempo de ensamble sigue una distribución exponencial con media de **4.0 minutos**.
- **Etapa 2 (Inspección):** Una vez ensamblada, la pieza pasa a una estación de control de calidad inspeccionada por 1 operario (capacidad = 1 recurso). El tiempo de inspección sigue una distribución uniforme continua de entre **2.0 y 5.0 minutos**.
- **Control de Calidad (Retrabajo):** Al terminar la inspección, se determina que el **15% de las piezas** presentan imperfecciones y son rechazadas. Estas deben volver a ingresar al inicio del proceso de ensamble y ser inspeccionadas nuevamente hasta pasar la prueba.
- **Propósito:** Calcular el tiempo de ciclo promedio (tiempo total transcurrido desde que la pieza entra al taller hasta que es aprobada), contar la cantidad de piezas completadas y medir el volumen de piezas que requirieron retrabajo durante **120 minutos** de simulación.

---

## 2. Código de la Simulación en Python

Guarda el siguiente código en un archivo llamado `simpy_ejemplo3_manufactura.py`:

```python
import random
import simpy

# Configuración de la simulación
SEMILLA = 42
TIEMPO_MEDIO_LLEGADA = 6.0    # Llega una pieza en bruto cada 6 minutos en promedio
TIEMPO_ENSAMBLE = 4.0         # Ensamblado toma 4 minutos en promedio
INSPECCION_MIN = 2.0          # Tiempo mínimo de inspección
INSPECCION_MAX = 5.0          # Tiempo máximo de inspección
TASA_DEFECTOS = 0.15          # 15% de las piezas fallan y requieren retrabajo
DURACION_SIMULACION = 120.0   # Simulación por 120 minutos

# Estadísticas
piezas_producidas = 0
tiempos_ciclo = []            # Tiempo total desde llegada hasta pieza aprobada
veces_retrabajo = []          # Historial de retrabajos por pieza

def proceso_inspeccion(env, nombre, inspector, llegada_original, n_retrabajos):
    """Proceso de inspección de calidad."""
    global piezas_producidas
    
    print(f"{env.now:7.2f} min: {nombre} llega a la cola de inspección.")
    with inspector.request() as peticion_inspector:
        yield peticion_inspector
        
        print(f"{env.now:7.2f} min: {nombre} inicia inspección de calidad.")
        tiempo_inspeccion = random.uniform(INSPECCION_MIN, INSPECCION_MAX)
        yield env.timeout(tiempo_inspeccion)
        
        # Determinar si aprueba el control de calidad
        aprobado = random.random() > TASA_DEFECTOS
        
        if aprobado:
            print(f"{env.now:7.2f} min: {nombre} APRUEBA inspección y se completa.")
            piezas_producidas += 1
            tiempos_ciclo.append(env.now - llegada_original)
            veces_retrabajo.append(n_retrabajos)
        else:
            print(f"{env.now:7.2f} min: {nombre} RECHAZADA. Reenviada a retrabajo.")
            # Si falla, inicia el ciclo de retrabajo en paralelo
            env.process(pieza_proceso(env, nombre, assembler_global, inspector_global, llegada_original, n_retrabajos + 1))

def pieza_proceso(env, nombre, assembler, inspector, llegada_original=None, n_retrabajos=0):
    """Proceso completo por el que pasa una pieza."""
    if llegada_original is None:
        llegada_original = env.now
        
    print(f"{env.now:7.2f} min: {nombre} inicia ensamblado (Retrabajo #{n_retrabajos}).")
    
    # Etapa 1: Ensamblado
    with assembler.request() as peticion_ensamble:
        yield peticion_ensamble
        
        tiempo_ensamble = random.expovariate(1.0 / TIEMPO_MEDIO_ENSAMBLE_O_SERVICIO) if 'TIEMPO_MEDIO_ENSAMBLE_O_SERVICIO' in globals() else random.expovariate(1.0 / TIEMPO_ENSAMBLE)
        yield env.timeout(tiempo_ensamble)
        print(f"{env.now:7.2f} min: {nombre} termina ensamblado.")
        
    # Etapa 2: Inspección
    yield env.process(proceso_inspeccion(env, nombre, inspector, llegada_original, n_retrabajos))

def generador_piezas(env, assembler, inspector):
    """Genera nuevas piezas para la línea de producción."""
    i = 0
    while True:
        i += 1
        yield env.timeout(random.expovariate(1.0 / TIEMPO_MEDIO_LLEGADA))
        env.process(pieza_proceso(env, f"Pieza {i}", assembler, inspector))

# Configuración del entorno
print("=========================================================")
print("  Simulación de Taller de Manufactura en Dos Etapas")
print("=========================================================\n")

random.seed(SEMILLA)
env = simpy.Environment()

# Recursos globales del taller
assembler_global = simpy.Resource(env, capacity=1)  # 1 Estación de ensamble
inspector_global = simpy.Resource(env, capacity=1)  # 1 Inspector de calidad

# Iniciar procesos de simulación
env.process(generador_piezas(env, assembler_global, inspector_global))
env.run(until=DURACION_SIMULACION)

# Impresión de estadísticas
if piezas_producidas > 0:
    t_ciclo_promedio = sum(tiempos_ciclo) / len(tiempos_ciclo)
    porcentaje_retrabajo = (sum(1 for r in veces_retrabajo if r > 0) / len(veces_retrabajo)) * 100
    max_retrabajos = max(veces_retrabajo)
    
    print("\n---------------------------------------------------------")
    print("                RESULTADOS DE LA SIMULACIÓN              ")
    print("---------------------------------------------------------")
    print(f"Piezas aprobadas (completas): {piezas_producidas}")
    print(f"Tiempo de ciclo promedio:     {t_ciclo_promedio:.2f} minutos")
    print(f"Piezas que requirieron retrabajo: {porcentaje_retrabajo:.1f}%")
    print(f"Máximo retrabajos en una pieza:   {max_retrabajos}")
    print("---------------------------------------------------------")
else:
    print("\nNo se completó ninguna pieza en la simulación.")
```

---

## 3. Instrucciones de Ejecución

Para iniciar la simulación, ejecuta en tu terminal:
```bash
python simpy_ejemplo3_manufactura.py
```

---

## 4. Resultados de la Simulación

Al ejecutar la simulación utilizando la semilla por defecto (`SEMILLA = 42`), la salida en consola es:

```text
=========================================================
  Simulación de Taller de Manufactura en Dos Etapas
=========================================================

   6.12 min: Pieza 1 inicia ensamblado (Retrabajo #0).
   6.27 min: Pieza 2 inicia ensamblado (Retrabajo #0).
   7.41 min: Pieza 1 termina ensamblado.
...
 117.02 min: Pieza 19 termina ensamblado.
 117.02 min: Pieza 19 llega a la cola de inspección.
 117.02 min: Pieza 19 inicia inspección de calidad.
 119.09 min: Pieza 20 inicia ensamblado (Retrabajo #0).
 119.29 min: Pieza 20 termina ensamblado.
 119.29 min: Pieza 20 llega a la cola de inspección.
 119.66 min: Pieza 21 inicia ensamblado (Retrabajo #0).

---------------------------------------------------------
                RESULTADOS DE LA SIMULACIÓN              
---------------------------------------------------------
Piezas aprobadas (completas): 18
Tiempo de ciclo promedio:     17.66 minutos
Piezas que requirieron retrabajo: 16.7%
Máximo retrabajos en una pieza:   2
---------------------------------------------------------
```

### Análisis de los Resultados:
- **Efecto de la Dependencia Estructural:** Aunque cada etapa tarda un promedio de 4.0 y 3.5 minutos respectivamente, el tiempo de ciclo promedio (el tiempo total real que le toma a una pieza salir del sistema) es de **17.66 minutos**. Esto ocurre debido a las colas acumulativas entre las dos estaciones y el tiempo extra gastado por las piezas rechazadas en el retrabajo.
- **Rendimiento e Inspección:** Se completaron 18 piezas en total. De estas, un **16.7%** experimentó fallas de calidad y tuvo que ser reprocesada (reensamblada e inspeccionada de nuevo). El número máximo de retrabajos sufridos por una sola pieza en esta corrida de simulación fue de **2 veces**.
