def simular_sistema_rapido_con_tabla():
    # --- 1. CONFIGURACIÓN DE PARÁMETROS Y VARIABLES ---
    tiempo_total = 120  # 2 horas en minutos
    cola = []           # Cola real con IDs de clientes
    cola_visual = []    # Lista auxiliar para mantener el formato de impresión
    tabla_log = []      # Almacena las filas de la tabla textualmente
    
    tiempo_s1 = 4
    tiempo_s2 = 5
    
    servidor1_libre_at = 0
    servidor2_libre_at = 0
    
    id_s1 = 0
    id_s2 = 0
    next_cliente_id = 1
    
    suma_clientes_en_cola = 0

    # --- 2. BUCLE DE SIMULACIÓN MINUTO A MINUTO ---
    for t in range(tiempo_total+2):
        
        # Detectar eventos de cambio antes de alterar estados
        cambio_s1 = (id_s1 != 0 and t == servidor1_libre_at)
        cambio_s2 = (id_s2 != 0 and t == servidor2_libre_at)
        arribo = (t % 2 == 0)
        
        # Liberar servidores si su tiempo concluyó
        if cambio_s1: id_s1 = 0
        if cambio_s2: id_s2 = 0
        
        # Acción A: Atender clientes en espera inmediatamente si se liberó un servidor
        if id_s1 == 0 and len(cola) > 0:
            id_s1 = cola.pop(0)
            cola_visual.pop(0)
            servidor1_libre_at = t + tiempo_s1
            
        if id_s2 == 0 and len(cola) > 0:
            id_s2 = cola.pop(0)
            cola_visual.pop(0)
            servidor2_libre_at = t + tiempo_s2

        # Acción B: Procesar la llegada de un nuevo cliente
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

        # Registrar métrica continua del tamaño de la cola
        suma_clientes_en_cola += len(cola)

        # Acción C: Registrar fila si ocurrió un evento (arribo o fin de servicio)
        if cambio_s1 or cambio_s2 or arribo:
            # Formatear el tiempo simulado comenzando a las 9:00 AM
            hora_str = f"{9 + t // 60:02d}:{t % 60:02d}"
            
            # Construir la cadena de texto de la cola
            cola_str = ", ".join([f"C{c}" for c in cola_visual]) if cola_visual else "-"
            s1_str = f"C{id_s1}" if id_s1 != 0 else "-"
            s2_str = f"C{id_s2}" if id_s2 != 0 else "-"
            
            # Formatear columnas alineadas a la izquierda con anchos fijos
            tabla_log.append(f"| {hora_str:<10} | {cola_str:<28} | {s1_str:<19} | {s2_str:<19} |")

    # --- 3. IMPRESIÓN DE LA TABLA EN CONSOLA ---
    print("\n======================= TABLA DE SIMULACIÓN (9:00 - 11:00) =======================")
    print("| Hora       | Clientes en Espera (Cola) | Servidor 1 (4 min)  | Servidor 2 (5 min)  |")
    print("-----------------------------------------------------------------------------------------")
    for fila in tabla_log:
        print(fila)
    print("=========================================================================================")

    # --- 4. CÁLCULO DE MÉTRICAS FINALES ---
    promedio_clientes_cola = suma_clientes_en_cola / tiempo_total
    tamano_final_cola = len(cola)

    print("\n====== MÉTRICAS FINALES ======")
    print(f"a) Número promedio de clientes en espera durante las 2 horas: {promedio_clientes_cola:.2f}")
    print(f"b) Tamaño de la línea de espera después de las 2 horas: {tamano_final_cola} clientes")

if __name__ == "__main__":
    simular_sistema_rapido_con_tabla()