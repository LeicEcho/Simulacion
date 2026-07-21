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
