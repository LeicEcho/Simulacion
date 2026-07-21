def simular_sistema_con_tabla():
    # --- 1. CONFIGURACIÓN Y VARIABLES ---
    tiempo_total = 120  # 2 horas en minutos
    cola = []           # Cola real del sistema
    cola_visual = []    # Rastreador para impresión
    tabla_log = []      # Historial de cambios
    tiempo_por_tamano = {}  # Diccionario para almacenar el tiempo por tamaño de cola

    servidor1_libre_at = 0
    servidor2_libre_at = 0
    
    id_s1 = 0
    id_s2 = 0
    next_cliente_id = 1
    
    atendidos_s1 = 0
    atendidos_s2 = 0

    # --- 2. BUCLE DE SIMULACIÓN ---
    for t in range(tiempo_total+2):
        
        # Detectar eventos de cambio
        cambio_s1 = (id_s1 != 0 and t == servidor1_libre_at)
        cambio_s2 = (id_s2 != 0 and t == servidor2_libre_at)
        arribo = (t % 6 == 0)
        
        if cambio_s1: id_s1 = 0
        if cambio_s2: id_s2 = 0
        
        # Acción A: Atender clientes en espera
        if id_s1 == 0 and len(cola) > 0:
            id_s1 = cola.pop(0)
            cola_visual.pop(0)
            servidor1_libre_at = t + 11
            atendidos_s1 += 1
            
        if id_s2 == 0 and len(cola) > 0:
            id_s2 = cola.pop(0)
            cola_visual.pop(0)
            servidor2_libre_at = t + 16
            atendidos_s2 += 1

        # Acción B: Procesar llegada de nuevo cliente
        if arribo:
            nuevo_cliente = next_cliente_id
            next_cliente_id += 1
            
            if id_s1 == 0:
                id_s1 = nuevo_cliente
                servidor1_libre_at = t + 11
                atendidos_s1 += 1
            elif id_s2 == 0:
                id_s2 = nuevo_cliente
                servidor2_libre_at = t + 16
                atendidos_s2 += 1
            else:
                cola.append(nuevo_cliente)
                cola_visual.append(nuevo_cliente)

        if t < tiempo_total:
            tam_actual = len(cola)            
            tiempo_por_tamano[tam_actual] = tiempo_por_tamano.get(tam_actual, 0) + 1

        # Acción C: Registrar fila si hubo un cambio de estado                  
        if cambio_s1 or cambio_s2 or arribo:
            hora_str = f"{9 + t // 60:02d}:{t % 60:02d}"
            cola_str = ", ".join([f"C{c}" for c in cola_visual]) if cola_visual else "-"
            s1_str = f"C{id_s1}" if id_s1 != 0 else "-"
            s2_str = f"C{id_s2}" if id_s2 != 0 else "-"
            
            tabla_log.append(f"| {hora_str:<10} | {cola_str:<25} | {s1_str:<19} | {s2_str:<19} |")

    # --- 3. IMPRESIÓN DE RESULTADOS ---
    print("\n======================= TABLA DE SIMULACIÓN =======================")
    print("| Hora       | Clientes en Espera (Cola) | Servidor 1 (11 min) | Servidor 2 (16 min) |")
    print("-------------------------------------------------------------------------------------")
    for fila in tabla_log:
        print(fila)
    print("=====================================================================================")

    numerador_formula = sum(tamano * minutos for tamano, minutos in tiempo_por_tamano.items())
    promedio_clientes_cola = numerador_formula / tiempo_total
    print("\n====== MÉTRICAS FINALES ======")
    print(f"a) Número promedio de clientes en espera: {promedio_clientes_cola:.3f}")
    print(f"b) Clientes atendidos por el Primer Servidor: {atendidos_s1}")
    print(f"c) Clientes atendidos por el Segundo Servidor: {atendidos_s2}")

if __name__ == "__main__":
    simular_sistema_con_tabla()