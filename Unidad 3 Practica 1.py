import math

def resolver_ejercicio_1():
    print("=========================================================")
    print("EJERCICIO 1: Banco Rioverdense (3 líneas M/M/1 en paralelo)")
    print("=========================================================")
    
    # Parámetros iniciales
    # Llegadas totales: 1 cliente cada 1.5 min -> 40 clientes/hora
    # Al dividirse en 3 cajas independientes, cada una recibe la tercera parte.
    lambda_total = 60 / 1.5  
    lambda_i = lambda_total / 3  # Tasa de llegada por caja (13.333 clientes/hora)
    mu = 60 / 4                  # Tasa de servicio por cajero (15 clientes/hora)
    rho = lambda_i / mu          # Factor de utilización
    
    # a) Tiempo promedio de los clientes en espera (W_q)
    L_q_caja = (rho**2) / (1 - rho)
    W_q = L_q_caja / lambda_i  # en horas
    W_q_min = W_q * 60         # en minutos
    
    # b) Número promedio de clientes en espera (L_q)
    # Se calcula tanto por caja individual como el total retenido en el banco
    L_q_total = L_q_caja * 3
    
    # c) Probabilidad de durar en espera 30 min o más P(W_q >= t)
    # t = 30 min = 0.5 horas
    W = W_q + (1 / mu)         # Tiempo promedio total en el sistema (horas)
    t = 30 / 60
    p_wq_30 = rho * math.exp(-t / W)
    
    print(f"a) Tiempo promedio de un cliente en espera (W_q): {W_q_min:.2f} minutos ({W_q:.4f} horas)")
    print(f"b) Número promedio de clientes en espera:")
    print(f"   - Por caja individual (L_q): {L_q_caja:.4f} clientes")
    print(f"   - Total en el banco (3 cajas): {L_q_total:.4f} clientes")
    print(f"c) Probabilidad de estar en espera 30 min o más: {p_wq_30 * 100:.2f}% ({p_wq_30:.4f})")


def resolver_ejercicio_2():
    print("\n=========================================================")
    print("EJERCICIO 2: Banco Rioverdense (Sistema Unilínea M/M/3)")
    print("=========================================================")
    
    # Parámetros iniciales
    lambda_total = 60 / 1.5    # Llegadas totales distribuidas en una sola fila (40 clientes/hora)
    S = 3                      # Número de servidores
    mu = 60 / 4                # Tasa de servicio por cajero (15 clientes/hora)
    rho = lambda_total / (S * mu) # Factor de utilización del sistema unilínea
    
    # Cálculo de P_0 (Probabilidad de sistema vacío) utilizando la fórmula del PDF
    sum_terminos = 0
    for n in range(S):
        sum_terminos += ((S * rho)**n) / math.factorial(n)
    termino_extension = ((S * rho)**S) / (math.factorial(S) * (1 - rho))
    P_0 = 1 / (sum_terminos + termino_extension)
    
    # P_s0 (Probabilidad de que el sistema esté ocupado / servidores llenos)
    P_s0 = (((S * rho)**S) / (math.factorial(S) * (1 - rho))) * P_0
    
    # b) Número promedio de clientes en espera (L_q) empleando la ecuación 13.20 del PDF
    L_q = P_s0 / (1 - rho)
    
    # a) Tiempo promedio de los clientes en espera (W_q) = L_q / lambda
    W_q = L_q / lambda_total  # en horas
    W_q_min = W_q * 60        # en minutos
    
    # c) Probabilidad de durar en espera 30 min o más empleando la ecuación 13.22 del PDF
    t = 30 / 60               # 30 minutos convertidos a horas
    p_wq_30 = P_s0 * math.exp(-S * mu * t * (1 - rho))
    
    print(f"a) Tiempo promedio de un cliente en espera (W_q): {W_q_min:.2f} minutos ({W_q:.4f} horas)")
    print(f"b) Número promedio de clientes en espera (L_q): {L_q:.4f} clientes")
    print(f"c) Probabilidad de estar en espera 30 min o más: {p_wq_30 * 100:.2f}% ({p_wq_30:.4f})")


def resolver_ejercicio_3():
    print("\n=========================================================")
    print("EJERCICIO 3: Tortillas Hamasa (Modelo M/M/1)")
    print("=========================================================")
    
    # Parámetros iniciales (Trabajaremos todo en la unidad de minutos)
    lambda_val = 1 / 2        # 1 cliente cada 2 min -> 0.5 clientes/minuto
    mu = 60 / 92              # 1 cliente cada 92 segundos -> 60/92 clientes/minuto
    rho = lambda_val / mu     # Factor de utilización
    
    # a) Número promedio de clientes en espera (L_q) y en la tortillería (L)
    L = rho / (1 - rho)
    L_q = (rho**2) / (1 - rho)
    
    # b) Tiempo promedio de los clientes en espera (W_q) y en el negocio (W)
    W = L / lambda_val        # Tiempo total en el negocio (minutos)
    W_q = L_q / lambda_val    # Tiempo en espera (minutos)
    
    # c) Probabilidad de durar en espera y en la tortillería más de 10 min (t = 10)
    t = 10
    p_sistema_10 = math.exp(-t / W)        # Probabilidad en la tortillería (Ecuación 13.15)
    p_espera_10 = rho * math.exp(-t / W)   # Probabilidad en espera (Ecuación 13.16)
    
    print(f"a) Número promedio de clientes:")
    print(f"   - En la tortillería completo (L): {L:.4f} clientes")
    print(f"   - En la fila de espera (L_q): {L_q:.4f} clientes")
    print(f"b) Tiempos promedio de permanencia:")
    print(f"   - En el negocio completo (W): {W:.2f} minutos")
    print(f"   - En espera en la fila (W_q): {W_q:.2f} minutos")
    print(f"c) Probabilidades para un tiempo mayor a 10 minutos:")
    print(f"   - De permanecer en la tortillería (sistema): {p_sistema_10 * 100:.2f}% ({p_sistema_10:.4f})")
    print(f"   - De permanecer únicamente en espera (fila): {p_espera_10 * 100:.2f}% ({p_espera_10:.4f})")
    print("=========================================================")

# Ejecución de todas las soluciones
if __name__ == "__main__":
    resolver_ejercicio_1()
    resolver_ejercicio_2()
    resolver_ejercicio_3()