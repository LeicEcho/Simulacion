def simular_servidores_en_paralelo_corregido():
    # --- 1. CONFIGURACIÓN DE PARÁMETROS Y VARIABLES ---
    tiempo_total = 60   # 1 hora en minutos
    cola = []           # Una sola cola compartida
    cola_visual = []    
    tabla_log = []      
    
    tiempo_s1 = 4
    tiempo_s2 = 2
    
    # Estas variables se configurarán dinámicamente en el minuto 0
    servidor1_libre_at = 0
    servidor2_libre_at = 0
    id_s1 = 0
    id_s2 = 0
    next_cliente_id = 1
    
    atendidos_s1 = 0
    atendidos_s2 = 0

    # --- 2. BUCLE DE SIMULACIÓN MINUTO A MINUTO ---
    for t in range(tiempo_total + 1):
        
        # CASO INICIAL: Forzar que el sistema arranque con C1 en S1 y C2 en S2
        if t == 0:
            id_s1 = 1
            servidor1_libre_at = t + tiempo_s1  # Libre en el minuto 4
            id_s2 = 2
            servidor2_libre_at = t + tiempo_s2  # Libre en el minuto 2
            next_cliente_id = 3                 # El próximo en llegar desde la calle será C3
            
            # Registrar la fotografía inicial del minuto 0:00
            hora_str = "0:00"
            tabla_log.append(f"| {hora_str:<10} | {'-':<25} | {'C1':<19} | {'C2':<19} |")
            continue  # Brincar directamente al minuto 1
            
        # --- LÓGICA NORMAL DESDE EL MINUTO 1 EN ADELANTE ---
        
        # 1. Detectar si algún servidor completa un servicio en este minuto
        cambio_s1 = (id_s1 != 0 and t == servidor1_libre_at)
        cambio_s2 = (id_s2 != 0 and t == servidor2_libre_at)
        
        if cambio_s1:
            atendidos_s1 += 1  # Servicio completado oficialmente para S1
            id_s1 = 0
        if cambio_s2:
            atendidos_s2 += 1  # Servicio completado oficialmente para S2
            id_s2 = 0
            
        # 2. Si se liberaron servidores, consumen de inmediato la cola compartida
        if id_s1 == 0 and len(cola) > 0:
            id_s1 = cola.pop(0)
            cola_visual.pop(0)
            servidor1_libre_at = t + tiempo_s1
            
        if id_s2 == 0 and len(cola) > 0:
            id_s2 = cola.pop(0)
            cola_visual.pop(0)
            servidor2_libre_at = t + tiempo_s2

        # 3. CASO LÍMITE: Al llegar a 1:00, guardamos el estado final y salimos
        if t == tiempo_total:
            hora_str = f"{t // 60}:{t % 60:02d}"
            cola_str = ", ".join([f"C{c}" for c in cola_visual]) if cola_visual else "-"
            s1_str = f"C{id_s1}" if id_s1 != 0 else "-"
            s2_str = f"C{id_s2}" if id_s2 != 0 else "-"
            tabla_log.append(f"| {hora_str:<10} | {cola_str:<25} | {s1_str:<19} | {s2_str:<19} |")
            break

        # 4. Procesar arribos normales de la calle (Cada 3 minutos a partir del minuto 3)
        arribo = (t % 3 == 0)
        if arribo:
            nuevo_cliente = next_cliente_id
            next_cliente_id += 1
            
            if id_s1 == 0:
                id_s1 = nuevo_cliente
                servidor1_libre_at = t + tiempo_s1
            elif id_s2 == 0:
                id_s2 = nuevo_cliente
                servidor2_libre_at = t + tiempo_s2
            else:
                cola.append(nuevo_cliente)
                cola_visual.append(nuevo_cliente)

        # 5. Registrar fila en la tabla si ocurrió un evento relevante
        if cambio_s1 or cambio_s2 or arribo:
            hora_str = f"{t // 60}:{t % 60:02d}"
            cola_str = ", ".join([f"C{c}" for c in cola_visual]) if cola_visual else "-"
            s1_str = f"C{id_s1}" if id_s1 != 0 else "-"
            s2_str = f"C{id_s2}" if id_s2 != 0 else "-"
            
            tabla_log.append(f"| {hora_str:<10} | {cola_str:<25} | {s1_str:<19} | {s2_str:<19} |")

    # --- 3. IMPRESIÓN DE LA TABLA EN CONSOLA ---
    print("\n======================= TABLA DE SIMULACIÓN PARALELA (CORREGIDA) =======================")
    print("| Hora       | Clientes en Espera (Cola) | Servidor 1 (4 min)  | Servidor 2 (2 min)  |")
    print("-----------------------------------------------------------------------------------------")
    for fila in tabla_log:
        print(fila)
    print("=========================================================================================")

    # --- 4. DESPLIEGUE DE MÉTRICAS FINALES ---
    print("\n====== MÉTRICAS FINALES (SISTEMA PARALELO - 1 HORA) ======")
    print(f"a) Tamaño de la línea de espera al finalizar la hora (1:00): {len(cola)} clientes")
    print(f"b) Número de clientes con SERVICIO COMPLETADO en una hora:")
    print(f"   - Por el Servidor 1: {atendidos_s1} clientes")
    print(f"   - Por el Servidor 2: {atendidos_s2} clientes")

if __name__ == "__main__":
    simular_servidores_en_paralelo_corregido()