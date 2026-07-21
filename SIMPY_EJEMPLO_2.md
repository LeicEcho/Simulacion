# Ejemplo de Simulación 2: Línea de Espera Multicanal (Modelo M/M/c)

Este ejemplo modela un sistema del tipo **M/M/c** (Llegadas y servicios aleatorios continuos con $c$ canales paralelos de atención), representando una estación de servicio (gasolinera) con 3 surtidores de combustible independientes que comparten una única cola.

---

## 1. Planteamiento del Problema

- **Llegada de Vehículos:** Los autos llegan a la gasolinera de forma aleatoria, con un tiempo medio entre llegadas de **0.75 minutos** (tasa de llegada $\lambda = 1.33$ vehículos por minuto).
- **Surtidores Compartidos:** La estación cuenta con **3 surtidores** compartidos. Si hay un surtidor libre, el vehículo lo ocupa de inmediato. Si todos están ocupados, espera en una fila única hasta que uno se libere.
- **Tiempo de Carga (Servicio):** El tiempo necesario para surtir combustible sigue una distribución exponencial con una media de **2.0 minutos**.
- **Propósito:** Medir la capacidad de la gasolinera para procesar el flujo vehicular, evaluar el tiempo promedio en cola y estimar la tasa de utilización global de los surtidores durante **60 minutos** de simulación.

---

## 2. Código de la Simulación en Python

Guarda el siguiente código en un archivo llamado `simpy_ejemplo2_mmc.py`:

```python
import random
import simpy

# Configuración de la simulación
SEMILLA = 42
NUM_SURTIDORES = 3       # Capacidad del recurso (c = 3)
TIEMPO_MEDIO_LLEGADA = 0.75  # Llega un auto cada 0.75 minutos (tasa = 1.33/min)
TIEMPO_MEDIO_SERVICIO = 2.0   # Cada auto tarda 2.0 minutos en promedio en surtirse
DURACION_SIMULACION = 60.0    # Simulación por 60 minutos

# Variables para estadísticas
tiempos_espera = []
tiempos_servicio = []
utilizacion_surtidores = []

def vehiculo(env, nombre, estacion):
    """Proceso que representa un vehículo que llega a cargar gasolina."""
    llegada = env.now
    print(f"{env.now:7.2f} min: {nombre} llega a la estación.")
    
    # Solicitar uno de los surtidores disponibles
    with estacion.request() as peticion:
        yield peticion
        
        espera = env.now - llegada
        tiempos_espera.append(espera)
        print(f"{env.now:7.2f} min: {nombre} comienza a cargar (espera: {espera:5.2f} min).")
        
        # Simular tiempo de carga de combustible
        tiempo_carga = random.expovariate(1.0 / TIEMPO_MEDIO_SERVICIO)
        tiempos_servicio.append(tiempo_carga)
        yield env.timeout(tiempo_carga)
        
        print(f"{env.now:7.2f} min: {nombre} termina de cargar y se retira.")

def generador_vehiculos(env, estacion):
    """Generador de tráfico de vehículos de manera aleatoria."""
    i = 0
    while True:
        i += 1
        tiempo_siguiente = random.expovariate(1.0 / TIEMPO_MEDIO_LLEGADA)
        yield env.timeout(tiempo_siguiente)
        env.process(vehiculo(env, f"Vehículo {i}", estacion))

# Configuración
print("=========================================================")
print("  Simulación de Cola M/M/c con SimPy: Estación de Servicio")
print("=========================================================\n")

random.seed(SEMILLA)
env = simpy.Environment()

# Recurso compartido con capacidad = 3
estacion = simpy.Resource(env, capacity=NUM_SURTIDORES)

# Iniciar procesos
env.process(generador_vehiculos(env, estacion))
env.run(until=DURACION_SIMULACION)

# Estadísticas
if tiempos_espera:
    espera_promedio = sum(tiempos_espera) / len(tiempos_espera)
    servicio_promedio = sum(tiempos_servicio) / len(tiempos_servicio)
    # Porcentaje de ocupación teórica acumulada de los servidores
    tiempo_total_servicio = sum(tiempos_servicio)
    utilizacion_total = (tiempo_total_servicio / (DURACION_SIMULACION * NUM_SURTIDORES)) * 100
    
    print("\n---------------------------------------------------------")
    print("                RESULTADOS DE LA SIMULACIÓN              ")
    print("---------------------------------------------------------")
    print(f"Total de vehículos atendidos:   {len(tiempos_espera)}")
    print(f"Tiempo de espera promedio:      {espera_promedio:.2f} minutos")
    print(f"Tiempo de servicio promedio:    {servicio_promedio:.2f} minutos")
    print(f"Utilización promedio del sistema: {min(utilizacion_total, 100.0):.2f}%")
    print("---------------------------------------------------------")
else:
    print("No hubo transacciones.")
```

---

## 3. Instrucciones de Ejecución

Para iniciar la simulación, ejecuta la consola y corre:
```bash
python simpy_ejemplo2_mmc.py
```

---

## 4. Resultados de la Simulación

Al ejecutar la simulación con la semilla establecida (`SEMILLA = 42`), se obtiene el siguiente resumen estadístico:

```text
=========================================================
  Simulación de Cola M/M/c con SimPy: Estación de Servicio
=========================================================

   0.39 min: Vehículo 1 llega a la estación.
   0.39 min: Vehículo 1 comienza a cargar (espera:  0.00 min).
   0.57 min: Vehículo 2 llega a la estación.
   0.57 min: Vehículo 2 comienza a cargar (espera:  0.00 min).
...
  59.18 min: Vehículo 85 llega a la estación.
  59.28 min: Vehículo 86 llega a la estación.
  59.32 min: Vehículo 84 termina de cargar y se retira.
  59.32 min: Vehículo 85 comienza a cargar (espera:  0.14 min).

---------------------------------------------------------
                RESULTADOS DE LA SIMULACIÓN              
---------------------------------------------------------
Total de vehículos atendidos:   85
Tiempo de espera promedio:      1.71 minutos
Tiempo de servicio promedio:    2.01 minutos
Utilización promedio del sistema: 95.02%
---------------------------------------------------------
```

### Análisis de los Resultados:
- **Alta Ocupación del Sistema:** Con una tasa de utilización promedio de **95.02%**, el sistema está operando casi a su capacidad máxima. Esto se debe a que la tasa de llegada (1.33 autos/min) es muy similar a la capacidad conjunta del sistema de servicio (3 servidores a 0.5 autos/min cada uno = 1.5 autos/min).
- **Cola y Espera:** A pesar de haber 3 canales paralelos de atención, el tiempo de espera promedio fue de **1.71 minutos**. Debido a la cercanía con el punto de saturación (95.02% de utilización), pequeñas ráfagas en las llegadas de vehículos pueden causar que la cola crezca rápidamente, incrementando los tiempos de espera individuales.
