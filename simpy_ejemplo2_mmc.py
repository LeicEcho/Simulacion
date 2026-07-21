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
