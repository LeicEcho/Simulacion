#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simulación de Sistema de Colas en Serie (Oficina de Rentas)
Autor: Antigravity Coding Assistant
"""

import math
import random
import sys

# Forzar codificación UTF-8 en stdout si es posible en Windows
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass  # En Python antiguo reconfigure podría no existir

# Códigos ANSI para dar formato y color a la terminal
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[32m"
BLUE = "\033[34m"
CYAN = "\033[36m"
YELLOW = "\033[33m"
RED = "\033[31m"
MAGENTA = "\033[35m"

# Configuración por defecto
CONFIG_DEFECTO = {
    'tiempo_arribo': 3.0,     # Clientes llegan cada 3 min
    'servicio_s1': 4.0,       # Servidor 1 tarda 4 min
    'servicio_s2': 2.0,       # Servidor 2 tarda 2 min
    'tiempo_simulacion': 60.0 # Duración de 1 hora (60 min)
}

def imprimir_banner():
    banner = f"""
{CYAN}{BOLD}+--------------------------------------------------------+
|  SIMULADOR DE COLAS EN SERIE - OFICINA DE RENTAS       |
+--------------------------------------------------------+{RESET}
{YELLOW}Problema:{RESET}
* Clientes llegan cada {CONFIG_DEFECTO['tiempo_arribo']} min.
* Servidor 1 (S1): tarda {CONFIG_DEFECTO['servicio_s1']} min en atender.
* Servidor 2 (S2): tarda {CONFIG_DEFECTO['servicio_s2']} min en atender.
* Tiempo de labor: {CONFIG_DEFECTO['tiempo_simulacion']} min (1 hora).
"""
    print(banner)

def simular_determinista(config, primer_arribo_cero=False):
    """
    Simulación determinista exacta donde los tiempos de llegada y servicio
    son constantes.
    """
    t_limite = config['tiempo_simulacion']
    t_arribo_cte = config['tiempo_arribo']
    t_s1_cte = config['servicio_s1']
    t_s2_cte = config['servicio_s2']

    # Generar arribos de clientes
    tiempos_arribo = []
    t = 0.0 if primer_arribo_cero else t_arribo_cte
    while t <= t_limite:
        tiempos_arribo.append(t)
        t += t_arribo_cte

    clientes = []
    s1_disponible = 0.0
    s2_disponible = 0.0

    for i, arr in enumerate(tiempos_arribo):
        c_id = i + 1
        
        # Servidor 1
        s1_ini = max(arr, s1_disponible)
        s1_fin = s1_ini + t_s1_cte
        s1_disponible = s1_fin
        
        # Servidor 2
        s2_ini = max(s1_fin, s2_disponible)
        s2_fin = s2_ini + t_s2_cte
        s2_disponible = s2_fin
        
        clientes.append({
            'id': c_id,
            'arribo': arr,
            's1_inicio': s1_ini,
            's1_fin': s1_fin,
            's2_inicio': s2_ini,
            's2_fin': s2_fin
        })

    # Clasificar el estado de cada cliente al t_limite (e.g. t = 60.0)
    cola_s1 = []
    en_s1 = None
    atendidos_s1 = 0

    cola_s2 = []
    en_s2 = None
    atendidos_s2 = 0

    for c in clientes:
        # Evaluar en Servidor 1
        if c['arribo'] <= t_limite:
            if c['s1_inicio'] <= t_limite < c['s1_fin']:
                en_s1 = c['id']
            elif c['arribo'] <= t_limite < c['s1_inicio']:
                cola_s1.append(c['id'])
            elif c['s1_fin'] <= t_limite:
                atendidos_s1 += 1

        # Evaluar en Servidor 2
        if c['s1_fin'] <= t_limite:
            if c['s2_inicio'] <= t_limite < c['s2_fin']:
                en_s2 = c['id']
            elif c['s1_fin'] <= t_limite < c['s2_inicio']:
                cola_s2.append(c['id'])
            elif c['s2_fin'] <= t_limite:
                atendidos_s2 += 1

    return {
        'clientes': clientes,
        'cola_s1': cola_s1,
        'en_s1': en_s1,
        'atendidos_s1': atendidos_s1,
        'cola_s2': cola_s2,
        'en_s2': en_s2,
        'atendidos_s2': atendidos_s2
    }

def simular_estocastica_una_vez(config):
    """
    Realiza una corrida de simulación estocástica (tiempos de llegada y 
    servicio distribuidos exponencialmente) usando simulación de eventos discretos.
    """
    t_limite = config['tiempo_simulacion']
    t_arribo_prom = config['tiempo_arribo']
    t_s1_prom = config['servicio_s1']
    t_s2_prom = config['servicio_s2']

    t_actual = 0.0
    eventos = []
    
    # Programar primer arribo
    t_primer_arribo = random.expovariate(1.0 / t_arribo_prom)
    eventos.append((t_primer_arribo, 'ARR', 1))
    
    clientes_datos = {}
    servidor_1 = None
    servidor_2 = None
    cola_s1 = []
    cola_s2 = []
    
    ultimo_cliente_creado = 1
    clientes_atendidos_s1 = 0
    clientes_atendidos_s2 = 0
    
    while eventos:
        eventos.sort(key=lambda x: x[0])
        ev_t, ev_tipo, ev_c_id = eventos.pop(0)
        
        if ev_t > t_limite:
            break
            
        t_actual = ev_t
        
        if ev_tipo == 'ARR':
            clientes_datos[ev_c_id] = {
                'arribo': t_actual, 's1_ini': None, 's1_fin': None,
                's2_ini': None, 's2_fin': None
            }
            
            ultimo_cliente_creado += 1
            t_sig_arribo = t_actual + random.expovariate(1.0 / t_arribo_prom)
            eventos.append((t_sig_arribo, 'ARR', ultimo_cliente_creado))
            
            if servidor_1 is None:
                servidor_1 = ev_c_id
                clientes_datos[ev_c_id]['s1_ini'] = t_actual
                duracion_s1 = random.expovariate(1.0 / t_s1_prom)
                eventos.append((t_actual + duracion_s1, 'FIN_S1', ev_c_id))
            else:
                cola_s1.append(ev_c_id)
                
        elif ev_tipo == 'FIN_S1':
            clientes_datos[ev_c_id]['s1_fin'] = t_actual
            clientes_atendidos_s1 += 1
            servidor_1 = None
            
            if cola_s1:
                sig_c = cola_s1.pop(0)
                servidor_1 = sig_c
                clientes_datos[sig_c]['s1_ini'] = t_actual
                duracion_s1 = random.expovariate(1.0 / t_s1_prom)
                eventos.append((t_actual + duracion_s1, 'FIN_S1', sig_c))
                
            if servidor_2 is None:
                servidor_2 = ev_c_id
                clientes_datos[ev_c_id]['s2_ini'] = t_actual
                duracion_s2 = random.expovariate(1.0 / t_s2_prom)
                eventos.append((t_actual + duracion_s2, 'FIN_S2', ev_c_id))
            else:
                cola_s2.append(ev_c_id)
                
        elif ev_tipo == 'FIN_S2':
            clientes_datos[ev_c_id]['s2_fin'] = t_actual
            clientes_atendidos_s2 += 1
            servidor_2 = None
            
            if cola_s2:
                sig_c = cola_s2.pop(0)
                servidor_2 = sig_c
                clientes_datos[sig_c]['s2_ini'] = t_actual
                duracion_s2 = random.expovariate(1.0 / t_s2_prom)
                eventos.append((t_actual + duracion_s2, 'FIN_S2', sig_c))

    cola_s1_final = []
    for c_id, datos in clientes_datos.items():
        if datos['arribo'] <= t_limite and (datos['s1_ini'] is None or datos['s1_ini'] > t_limite):
            cola_s1_final.append(c_id)
            
    cola_s2_final = []
    for c_id, datos in clientes_datos.items():
        if datos['s1_fin'] is not None and datos['s1_fin'] <= t_limite:
            if datos['s2_ini'] is None or datos['s2_ini'] > t_limite:
                cola_s2_final.append(c_id)

    return {
        'cola_s1_size': len(cola_s1_final),
        'cola_s2_size': len(cola_s2_final),
        'atendidos_s1': clientes_atendidos_s1,
        'atendidos_s2': clientes_atendidos_s2
    }

def simular_montecarlo(config, corridas=5000):
    total_cola1 = 0
    total_cola2 = 0
    total_atendidos1 = 0
    total_atendidos2 = 0
    
    for _ in range(corridas):
        res = simular_estocastica_una_vez(config)
        total_cola1 += res['cola_s1_size']
        total_cola2 += res['cola_s2_size']
        total_atendidos1 += res['atendidos_s1']
        total_atendidos2 += res['atendidos_s2']
        
    return {
        'prom_cola_s1': total_cola1 / corridas,
        'prom_cola_s2': total_cola2 / corridas,
        'prom_atendidos_s1': total_atendidos1 / corridas,
        'prom_atendidos_s2': total_atendidos2 / corridas
    }

def mostrar_analisis_teorico(config):
    t_arr = config['tiempo_arribo']
    t_s1 = config['servicio_s1']
    t_s2 = config['servicio_s2']
    
    lmbda = 1.0 / t_arr
    mu1 = 1.0 / t_s1
    mu2 = 1.0 / t_s2
    
    rho1 = lmbda / mu1
    rho2 = lmbda / mu2
    
    print(f"\n{BOLD}{CYAN}=== ANALISIS TEORICO (TEORIA DE COLAS M/M/1 EN SERIE) ==={RESET}")
    print(f"Tasa de llegada (lambda) = 1/{t_arr:.1f} = {lmbda:.3f} clientes/minuto")
    print(f"Tasa de servicio Servidor 1 (mu1) = 1/{t_s1:.1f} = {mu1:.3f} clientes/minuto")
    print(f"Tasa de servicio Servidor 2 (mu2) = 1/{t_s2:.1f} = {mu2:.3f} clientes/minuto")
    
    print(f"\n{BOLD}1. Servidor 1:{RESET}")
    print(f"  * Intensidad de trafico (rho1) = lambda / mu1 = {rho1:.3f}")
    if rho1 >= 1.0:
        print(f"  * {RED}!SISTEMA INESTABLE! (rho1 >= 1){RESET}")
        print(f"    Dado que la tasa de llegada ({lmbda:.3f}) supera a la tasa de servicio ({mu1:.3f}),")
        print(f"    la cola del Servidor 1 crecera de forma indefinida con el tiempo.")
        crecimiento_minuto = lmbda - mu1
        crecimiento_hora = crecimiento_minuto * config['tiempo_simulacion']
        print(f"    Tasa neta de acumulacion = {crecimiento_minuto:.4f} clientes/minuto")
        print(f"    Crecimiento teorico estimado en {config['tiempo_simulacion']:.1f} min = {crecimiento_hora:.2f} clientes")
    else:
        L1 = rho1 / (1 - rho1)
        Lq1 = (rho1**2) / (1 - rho1)
        print(f"  * {GREEN}Estable (rho1 < 1){RESET}")
        print(f"  * Clientes promedio en el sistema 1 (L1) = {L1:.2f}")
        print(f"  * Clientes promedio en la cola 1 (Lq1) = {Lq1:.2f}")
        
    print(f"\n{BOLD}2. Servidor 2:{RESET}")
    print(f"  * Dado que el Servidor 1 esta saturado (rho1 >= 1), este trabaja de manera continua.")
    print(f"    Por ende, la tasa de salida real de S1 (que es la tasa de llegada efectiva a S2)")
    print(f"    se limita a su tasa maxima de servicio: {BOLD}lambda2 = mu1 = {mu1:.3f} clientes/minuto{RESET}.")
    
    rho2_efectivo = mu1 / mu2
    print(f"  * Intensidad de trafico efectiva (rho2) = lambda2 / mu2 = mu1 / mu2 = {rho2_efectivo:.3f}")
    
    if rho2_efectivo >= 1.0:
        print(f"  * {RED}!SISTEMA INESTABLE! (rho2 >= 1){RESET}")
    else:
        L2 = rho2_efectivo / (1 - rho2_efectivo)
        Lq2 = (rho2_efectivo**2) / (1 - rho2_efectivo)
        print(f"  * {GREEN}Estable (rho2 < 1){RESET}")
        print(f"  * Clientes promedio en el sistema 2 (L2) = {L2:.2f}")
        print(f"  * Clientes promedio en la cola 2 (Lq2) = {Lq2:.2f}")

def mostrar_tabla_clientes(clientes, t_limite):
    print(f"\n{BOLD}{CYAN}=== TRAZA DETALLADA DE CLIENTES (Simulacion Determinista) ==={RESET}")
    header = f"{'Cliente ID':^12}|{'Arribo':^10}|{'S1 Inicio':^10}|{'S1 Fin':^10}|{'S2 Inicio':^10}|{'S2 Fin':^10}|{'Estado a t=' + str(int(t_limite)):^22}"
    print(header)
    print("-" * len(header))
    
    for c in clientes:
        estado = ""
        if c['arribo'] > t_limite:
            estado = "No ha llegado"
        elif c['s1_inicio'] > t_limite:
            estado = "En Cola 1"
        elif c['s1_inicio'] <= t_limite < c['s1_fin']:
            estado = "En Servicio 1"
        elif c['s1_fin'] <= t_limite and (c['s2_inicio'] > t_limite or c['s2_inicio'] is None):
            estado = "En Cola 2"
        elif c['s2_inicio'] <= t_limite < c['s2_fin']:
            estado = "En Servicio 2"
        elif c['s2_fin'] <= t_limite:
            estado = "Atendido S1 y S2"
            
        if "Cola" in estado:
            estado_c = f"{YELLOW}{estado}{RESET}"
        elif "Servicio" in estado:
            estado_c = f"{CYAN}{estado}{RESET}"
        elif "Atendido" in estado:
            estado_c = f"{GREEN}{estado}{RESET}"
        else:
            estado_c = f"{RESET}{estado}{RESET}"
            
        print(f"{c['id']:^12}|{c['arribo']:^10.1f}|{c['s1_inicio']:^10.1f}|{c['s1_fin']:^10.1f}|{c['s2_inicio']:^10.1f}|{c['s2_fin']:^10.1f}| {estado_c:<22}")

def ejecutar_caso_determinista(config):
    print(f"\n{BOLD}{GREEN}============================================================")
    print("  CASO A: SIMULACION DETERMINISTA (Valores Constantes)")
    print(f"============================================================{RESET}")
    
    res_t3 = simular_determinista(config, primer_arribo_cero=False)
    res_t0 = simular_determinista(config, primer_arribo_cero=True)
    
    print(f"\n{BOLD}Opcion 1: Primer cliente llega a los {config['tiempo_arribo']} minutos (t=3){RESET}")
    print(f"  * Clientes arribados en {config['tiempo_simulacion']:.1f} min: {len(res_t3['clientes'])}")
    print(f"  * Servidor 1 (S1):")
    print(f"    - Clientes que completaron S1: {BOLD}{res_t3['atendidos_s1']}{RESET}")
    print(f"    - Clientes en cola de espera 1: {BOLD}{len(res_t3['cola_s1'])}{RESET} {YELLOW}(ID clientes: {res_t3['cola_s1']}){RESET}")
    print(f"    - Cliente actualmente en servicio 1: {res_t3['en_s1']}")
    print(f"  * Servidor 2 (S2):")
    print(f"    - Clientes que completaron S2: {BOLD}{res_t3['atendidos_s2']}{RESET}")
    print(f"    - Clientes en cola de espera 2: {BOLD}{len(res_t3['cola_s2'])}{RESET}")
    print(f"    - Cliente actualmente en servicio 2: {res_t3['en_s2']}")
    
    print(f"\n{BOLD}Opcion 2: Primer cliente llega a los 0 minutos (t=0){RESET}")
    print(f"  * Clientes arribados en {config['tiempo_simulacion']:.1f} min: {len(res_t0['clientes'])}")
    print(f"  * Servidor 1 (S1):")
    print(f"    - Clientes que completaron S1: {BOLD}{res_t0['atendidos_s1']}{RESET}")
    print(f"    - Clientes en cola de espera 1: {BOLD}{len(res_t0['cola_s1'])}{RESET} {YELLOW}(ID clientes: {res_t0['cola_s1']}){RESET}")
    print(f"    - Cliente actualmente en servicio 1: {res_t0['en_s1']}")
    print(f"  * Servidor 2 (S2):")
    print(f"    - Clientes que completaron S2: {BOLD}{res_t0['atendidos_s2']}{RESET}")
    print(f"    - Clientes en cola de espera 2: {BOLD}{len(res_t0['cola_s2'])}{RESET}")
    print(f"    - Cliente actualmente en servicio 2: {res_t0['en_s2']}")

    opcion = input(f"\n¿Desea ver la tabla detallada de clientes de la Opcion 1 (t_inicial=3)? (s/n): ").strip().lower()
    if opcion == 's':
        mostrar_tabla_clientes(res_t3['clientes'], config['tiempo_simulacion'])

def ejecutar_caso_estocastico(config):
    print(f"\n{BOLD}{GREEN}============================================================")
    print("  CASO B: SIMULACION ESTOCASTICA (Monte Carlo)")
    print("  (Arribos de Poisson y Servicios Exponenciales)")
    print(f"============================================================{RESET}")
    
    corridas = 10000
    print(f"Ejecutando {corridas} simulaciones de una hora de duracion...")
    res = simular_montecarlo(config, corridas)
    
    print(f"\n{BOLD}Resultados Promedio despues de {config['tiempo_simulacion']:.1f} minutos:{RESET}")
    print(f"  * Servidor 1 (S1) [Servicio promedio: {config['servicio_s1']} min]:")
    print(f"    - Clientes atendidos promedio: {BOLD}{res['prom_atendidos_s1']:.2f}{RESET}")
    print(f"    - Tamano promedio de la cola 1: {BOLD}{res['prom_cola_s1']:.2f}{RESET}")
    print(f"  * Servidor 2 (S2) [Servicio promedio: {config['servicio_s2']} min]:")
    print(f"    - Clientes atendidos promedio: {BOLD}{res['prom_atendidos_s2']:.2f}{RESET}")
    print(f"    - Tamano promedio de la cola 2: {BOLD}{res['prom_cola_s2']:.2f}{RESET}")
    
    print(f"\n{YELLOW}Nota de interpretacion:{RESET}")
    print("En un entorno real (estocastico), la variabilidad hace que se forme una pequena cola")
    print("en el segundo servidor (promedio de ~0.5 a 1 cliente), a diferencia de la simulacion")
    print("determinista exacta donde la cola del segundo servidor es siempre 0.")

def editar_parametros(config):
    print(f"\n{BOLD}{CYAN}=== EDITAR PARAMETROS DE LA SIMULACION ==={RESET}")
    try:
        arr = float(input(f"Tiempo promedio entre arribos (actual {config['tiempo_arribo']} min): ") or config['tiempo_arribo'])
        s1 = float(input(f"Tiempo promedio servicio Servidor 1 (actual {config['servicio_s1']} min): ") or config['servicio_s1'])
        s2 = float(input(f"Tiempo promedio servicio Servidor 2 (actual {config['servicio_s2']} min): ") or config['servicio_s2'])
        ts = float(input(f"Tiempo total de simulacion (actual {config['tiempo_simulacion']} min): ") or config['tiempo_simulacion'])
        
        config['tiempo_arribo'] = arr
        config['servicio_s1'] = s1
        config['servicio_s2'] = s2
        config['tiempo_simulacion'] = ts
        print(f"\n{GREEN}[OK] Parametros actualizados correctamente.{RESET}")
    except ValueError:
        print(f"\n{RED}[ERROR] Entrada no valida. Se conservan los parametros anteriores.{RESET}")

def menu_principal():
    config = CONFIG_DEFECTO.copy()
    
    while True:
        imprimir_banner()
        print(f"{BOLD}Seleccione una opcion del menu:{RESET}")
        print(f"  {BLUE}1.{RESET} Ejecutar Simulacion Determinista (Caso exacto)")
        print(f"  {BLUE}2.{RESET} Ejecutar Simulacion Estocastica (Monte Carlo con 10,000 corridas)")
        print(f"  {BLUE}3.{RESET} Mostrar Analisis Teorico y Formulas Matematicas")
        print(f"  {BLUE}4.{RESET} Modificar Parametros de la Simulacion")
        print(f"  {BLUE}5.{RESET} Salir del programa")
        
        opc = input(f"\n{BOLD}Ingrese su eleccion (1-5): {RESET}").strip()
        
        if opc == '1':
            ejecutar_caso_determinista(config)
        elif opc == '2':
            ejecutar_caso_estocastico(config)
        elif opc == '3':
            mostrar_analisis_teorico(config)
        elif opc == '4':
            editar_parametros(config)
        elif opc == '5':
            print(f"\n{GREEN}¡Gracias por usar el simulador de colas en serie! Hasta luego.{RESET}\n")
            sys.exit(0)
        else:
            print(f"\n{RED}Opcion no valida. Intente de nuevo.{RESET}")
            
        input(f"\nPresione Enter para continuar...")

if __name__ == "__main__":
    try:
        menu_principal()
    except KeyboardInterrupt:
        print(f"\n\n{RED}Simulacion cancelada por el usuario. Saliendo...{RESET}\n")
        sys.exit(0)
