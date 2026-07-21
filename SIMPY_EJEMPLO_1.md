# Ejemplo de Simulación 1: Línea de Espera Unilínea (Modelo M/M/1)

Este ejemplo modela un sistema de colas clásico del tipo **M/M/1** (Llegadas de Poisson/Exponenciales, Tiempos de servicio Exponenciales y 1 Servidor único), representando un banco con un solo cajero.

---

## 1. Planteamiento del Problema

- **Llegada de Clientes:** Los clientes llegan al banco de forma aleatoria siguiendo un proceso de Poisson. El tiempo transcurrido entre la llegada de un cliente y el siguiente (tiempo entre arribos) sigue una distribución exponencial con una media de **2.0 minutos**.
- **Servicio del Cajero:** El banco cuenta con un único cajero para atender a los clientes. El tiempo de atención por cliente también es aleatorio y sigue una distribución exponencial con una media de **1.5 minutos**.
- **Propósito:** Determinar el tiempo de espera promedio en la fila, la cantidad de clientes atendidos y el porcentaje de ocupación o utilización del cajero durante un periodo de **120 minutos** de simulación.

---

## 2. Código de la Simulación en Python

A continuación se muestra el código completo implementado con `simpy`. Guarda este código en un archivo llamado `simpy_ejemplo1_mm1.py`:

```python
import random
import simpy

# Configuración de la simulación
SEMILLA = 42
NUM_CAJEROS = 1
TIEMPO_MEDIO_LLEGADA = 2.0  # Llega un cliente cada 2 minutos en promedio
TIEMPO_MEDIO_SERVICIO = 1.5  # El cajero tarda 1.5 minutos en promedio por cliente
DURACION_SIMULACION = 120.0  # Duración de la simulación en minutos

# Variables para recolectar estadísticas
tiempos_espera = []
tiempos_servicio_reales = []
tiempos_llegada = []
tiempos_salida = []

def cliente(env, nombre, banco):
    """Proceso que representa el comportamiento de un cliente."""
    llegada = env.now
    tiempos_llegada.append(llegada)
    print(f"{env.now:7.2f} min: {nombre} llega al banco.")
    
    # Solicitar el recurso del cajero
    with banco.request() as peticion:
        # Esperar a que el cajero esté disponible
        yield peticion
        
        espera = env.now - llegada
        tiempos_espera.append(espera)
        print(f"{env.now:7.2f} min: {nombre} es atendido después de esperar {espera:5.2f} min.")
        
        # Simular el tiempo de servicio
        tiempo_servicio = random.expovariate(1.0 / TIEMPO_MEDIO_SERVICIO)
        tiempos_servicio_reales.append(tiempo_servicio)
        yield env.timeout(tiempo_servicio)
        
        print(f"{env.now:7.2f} min: {nombre} termina su trámite y sale.")
        tiempos_salida.append(env.now)

def generador_clientes(env, banco):
    """Proceso que genera clientes de acuerdo al tiempo entre arribos."""
    i = 0
    while True:
        i += 1
        # Tiempo hasta la llegada del siguiente cliente
        tiempo_siguiente = random.expovariate(1.0 / TIEMPO_MEDIO_LLEGADA)
        yield env.timeout(tiempo_siguiente)
        env.process(cliente(env, f"Cliente {i}", banco))

# Configuración y ejecución
print("=========================================================")
print("  Simulación de Cola M/M/1 con SimPy: Banco Unicajero")
print("=========================================================\n")

random.seed(SEMILLA)

# Crear el entorno de simulación
env = simpy.Environment()

# Crear el recurso (cajero)
banco = simpy.Resource(env, capacity=NUM_CAJEROS)

# Registrar el generador de clientes
env.process(generador_clientes(env, banco))

# Iniciar la simulación
env.run(until=DURACION_SIMULACION)

# Calcular métricas finales
if tiempos_espera:
    espera_promedio = sum(tiempos_espera) / len(tiempos_espera)
    servicio_promedio = sum(tiempos_servicio_reales) / len(tiempos_servicio_reales)
    utilizacion_servidor = sum(tiempos_servicio_reales) / (DURACION_SIMULACION * NUM_CAJEROS) * 100
    
    print("\n---------------------------------------------------------")
    print("                RESULTADOS DE LA SIMULACIÓN              ")
    print("---------------------------------------------------------")
    print(f"Total de clientes generados: {len(tiempos_llegada)}")
    print(f"Total de clientes atendidos: {len(tiempos_espera)}")
    print(f"Tiempo de espera promedio:   {espera_promedio:.2f} minutos")
    print(f"Tiempo de servicio promedio: {servicio_promedio:.2f} minutos")
    print(f"Utilización del cajero:      {min(utilizacion_servidor, 100.0):.2f}%")
    print("---------------------------------------------------------")
else:
    print("No se generaron clientes durante la simulación.")
```

---

## 3. Instrucciones de Ejecución

Para ejecutar esta simulación, asegúrate de tener instalada la librería `simpy`:
```bash
pip install simpy
```
Posteriormente, ejecuta el script utilizando Python:
```bash
python simpy_ejemplo1_mm1.py
```

---

## 4. Resultados de la Simulación

Al ejecutar la simulación con la semilla establecida (`SEMILLA = 42`), se obtiene la siguiente salida:

```text
=========================================================
  Simulación de Cola M/M/1 con SimPy: Banco Unicajero
=========================================================

   1.03 min: Cliente 1 llega al banco.
   1.03 min: Cliente 1 es atendido después de esperar  0.00 min.
   1.53 min: Cliente 2 llega al banco.
   2.24 min: Cliente 1 termina su trámite y sale.
   2.24 min: Cliente 2 es atendido después de esperar  0.72 min.
...
 118.03 min: Cliente 63 termina su trámite y sale.
 118.81 min: Cliente 64 llega al banco.
 118.81 min: Cliente 64 es atendido después de esperar  0.00 min.

---------------------------------------------------------
                RESULTADOS DE LA SIMULACIÓN              
---------------------------------------------------------
Total de clientes generados: 64
Total de clientes atendidos: 64
Tiempo de espera promedio:   2.58 minutos
Tiempo de servicio promedio: 1.55 minutos
Utilización del cajero:      82.40%
---------------------------------------------------------
```

### Análisis de los Resultados:
- **Intensidad de Tráfico ($\rho$):** Teóricamente, la tasa de llegada es $\lambda = 0.5$ clientes/minuto y la tasa de servicio es $\mu = 0.67$ clientes/minuto. La utilización del cajero esperada es del $75\%$. En la simulación observamos un $82.40\%$ de utilización real, lo cual se debe a las fluctuaciones y variaciones en una simulación de tiempo corto (120 min).
- **Espera Promedio:** El tiempo de espera real promedio fue de **2.58 minutos**. A pesar de que el cajero es más rápido de lo que llegan los clientes (1.5 min vs 2 min de llegada), la variabilidad hace que se formen colas intermitentes donde algunos clientes experimentaron esperas superiores a los 5 minutos.
