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
        
        tiempo_ensamble = random.expovariate(1.0 / TIEMPO_ENSAMBLE)
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
