def simular_servidores_en_serie():
    # --- 1. CONFIGURACIÓN DE PARÁMETROS Y VARIABLES ---
    tiempo_total = 60 
    
    # Subsistema 1 (Entrada de la calle)
    cola1 = []           
    cola_visual1 = []    
    tiempo_s1 = 4
    servidor1_libre_at = 0
    id_s1 = 0
    atendidos_s1 = 0

    # Subsistema 2 (Recibe solo las salidas del Servidor 1)
    cola2 = []           
    cola_visual2 = []    
    tiempo_s2 = 2
    servidor2_libre_at = 0
    id_s2 = 0
    atendidos_s2 = 0
    
    next_cliente_id = 1
    tabla_log = []      # Historial de la tabla

    # --- 2. BUCLE DE SIMULACIÓN MINUTO A MINUTO ---
    for t in range(tiempo_total+1):
        
        # 1. Detectar si algún servidor completa un servicio en este minuto
        cambio_s1 = (id_s1 != 0 and t == servidor1_libre_at)
        cambio_s2 = (id_s2 != 0 and t == servidor2_libre_at)
        
        if cambio_s2:
            atendidos_s2 += 1  # Servicio completado oficialmente para S2
            id_s2 = 0
            
        cliente_saliente_s1 = None
        if cambio_s1:
            atendidos_s1 += 1  # Servicio completado oficialmente para S1
            cliente_saliente_s1 = id_s1
            id_s1 = 0
            
        # 2. El cliente que sale de S1 avanza inmediatamente al sistema de S2
        if cliente_saliente_s1 is not None:
            if id_s2 == 0 and len(cola2) == 0:
                id_s2 = cliente_saliente_s1
                servidor2_libre_at = t + tiempo_s2
            else:
                cola2.append(cliente_saliente_s1)
                cola_visual2.append(cliente_saliente_s1)
                
        # 3. Si los servidores quedaron libres, absorben al siguiente de su propia cola
        if id_s1 == 0 and len(cola1) > 0:
            id_s1 = cola1.pop(0)
            cola_visual1.pop(0)
            servidor1_libre_at = t + tiempo_s1
            
        if id_s2 == 0 and len(cola2) > 0:
            id_s2 = cola2.pop(0)
            cola_visual2.pop(0)
            servidor2_libre_at = t + tiempo_s2

        # 4. CASO LIMITE
        if t > tiempo_total:
            hora_str = f"{t // 60}:{t % 60:02d}"
            cola1_str = ", ".join([f"C{c}" for c in cola_visual1]) if cola_visual1 else "-"
            cola2_str = ", ".join([f"C{c}" for c in cola_visual2]) if cola_visual2 else "-"
            s1_str = f"C{id_s1}" if id_s1 != 0 else "-"
            s2_str = f"C{id_s2}" if id_s2 != 0 else "-"
            tabla_log.append(f"| {hora_str:<10} | {cola1_str:<18} | {cola2_str:<18} | {s1_str:<19} | {s2_str:<19} |")
            break

        # 5. Procesar arribos (Cada 3 minutos)
        arribo = (t % 3 == 0)
        if arribo:
            nuevo_cliente = next_cliente_id
            next_cliente_id += 1
            
            if id_s1 == 0:
                id_s1 = nuevo_cliente
                servidor1_libre_at = t + tiempo_s1
            else:
                cola1.append(nuevo_cliente)
                cola_visual1.append(nuevo_cliente)

        # 6. Registrar la fila en la tabla si ocurrió algún cambio en este minuto
        if cambio_s1 or cambio_s2 or arribo:
            hora_str = f"{t // 60}:{t % 60:02d}"
            cola1_str = ", ".join([f"C{c}" for c in cola_visual1]) if cola_visual1 else "-"
            cola2_str = ", ".join([f"C{c}" for c in cola_visual2]) if cola_visual2 else "-"
            s1_str = f"C{id_s1}" if id_s1 != 0 else "-"
            s2_str = f"C{id_s2}" if id_s2 != 0 else "-"
            
            tabla_log.append(f"| {hora_str:<10} | {cola1_str:<25} | {cola2_str:<14} | {s1_str:<19} | {s2_str:<19} |")

    # --- 3. IMPRESIÓN DE LA TABLA EN CONSOLA ---
    print("\n=================================== TABLA DE SIMULACIÓN EN SERIE ===================================")
    print("| Hora       | Espera Cola 1             | Espera Cola 2  | Servidor 1 (4 min)  | Servidor 2 (2 min)  |")
    print("------------------------------------------------------------------------------------------------------")
    for fila in tabla_log:
        print(fila)
    print("======================================================================================================")

    # --- 4. DESPLIEGUE DE MÉTRICAS FINALES ---
    print("\n====== MÉTRICAS FINALES (SISTEMA EN SERIE - 1 HORA) ======")
    print(f"a) Tamaño de las líneas de espera exactamente a la hora (1:00):")
    print(f"   - Línea de espera del Servidor 1: {len(cola1)} clientes")
    print(f"   - Línea de espera del Servidor 2: {len(cola2)} clientes")
    print(f"b) Número de clientes con SERVICIO COMPLETADO en una hora:")
    print(f"   - Por el Servidor 1: {atendidos_s1} clientes")
    print(f"   - Por el Servidor 2: {atendidos_s2} clientes")

if __name__ == "__main__":
    simular_servidores_en_serie()