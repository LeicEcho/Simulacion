import math
# pyrefly: ignore [missing-import]
from scipy import stats

def generador_periodo_completo(semilla, a, b, M):
    secuencia = []
    registro_apariciones = {}
    
    X = semilla % M
    ciclo_completo_alcanzado = False
    
    print(f"\nConfiguración del espacio modular:")
    print(f"Semilla operativa inicial: {X} | Multiplicador (a): {a} | Incremento (b): {b} | Módulo (M): {M}")
    print("-" * 85)

    for i in range(1, M + 2):
        X = (a * X + b) % M
        
        if X in registro_apariciones:
            p_primera = registro_apariciones[X]
            periodo_real = i - p_primera
            print(f"-> ¡Ciclo interceptado en la iteración N° {i}! (Valor repetido: {X})")
            print(f"   Primera aparición: Iteración {p_primera}")
            print(f"   Periodo real alcanzado: {periodo_real} números pseudoaleatorios.")
            
            if periodo_real == M:
                print("   [ÉXITO] ¡ÉXITO! Se ha demostrado matemáticamente el PERIODO COMPLETO.")
                ciclo_completo_alcanzado = True
            else:
                print("   [ADVERTENCIA] El periodo es parcial. Las constantes no son óptimas.")
            break
            
        registro_apariciones[X] = i
        secuencia.append(X)
        
    return secuencia if ciclo_completo_alcanzado else []

# =========================================================================
# BLOQUE DE PRUEBAS ESTADÍSTICAS (MÉTODOS UNIFICADOS)
# =========================================================================

def ejecutar_pruebas_estadisticas(numeros_enteros, M, alpha=0.05):
    # NORMALIZACIÓN: Transformar enteros [0, M-1] a reales en el intervalo (0, 1) 
    u = [x / M for x in numeros_enteros]
    N = len(u)
    
    print("\n" + "=" * 85)
    print(f"BATERÍA DE PRUEBAS ESTADÍSTICAS DE INDEPENDENCIA Y UNIFORMIDAD (N = {N})")
    print("=" * 85)

    # 1. PRUEBA DE LOS PROMEDIOS
    print("\n1) PRUEBA DE LOS PROMEDIOS (Uniformidad)")
    print("-" * 55)
    promedio = sum(u) / N
    z_0 = (promedio - 0.5) * math.sqrt(N) / math.sqrt(1/12) 
    z_critico = stats.norm.ppf(1 - alpha / 2) 
    pasan_promedio = abs(z_0) <= z_critico
    
    print(f"-> Promedio muestral calculado (x̄): {promedio:.5f}")
    print(f"-> Estadístico de prueba (Z_0): {z_0:.2f} ")
    print(f"-> Valor crítico (Z_alpha/2): ±{z_critico:.2f} ")
    print(f" CONCLUSIÓN: {'Pasan la prueba. No se rechaza H0.' if pasan_promedio else 'No pasan la prueba. Se rechaza H0.'}")

    # 2. PRUEBA DE FRECUENCIAS (n = 5 subintervalos)
    print("\n2) PRUEBA DE FRECUENCIAS (Uniformidad por Reparto)")
    print("-" * 55)
    k = 5
    fe_frec = N / k
    fo_frec = [0] * k
    for num in u:
        rango = int(num * k)
        if rango == k: rango = k - 1
        fo_frec[rango] += 1
        
    chi_frec = sum(((fo_frec[i] - fe_frec) ** 2) / fe_frec for i in range(k))
    gl_frec = k - 1
    chi_critico_frec = stats.chi2.ppf(1 - alpha, gl_frec) 
    pasan_frecuencias = chi_frec <= chi_critico_frec 
    
    print("Distribución por subintervalos:")
    for idx in range(k):
        print(f"  Intervalo [{idx/k:.1f} - {(idx+1)/k:.1f}): FO = {fo_frec[idx]}, FE = {fe_frec}")
    print(f"-> Estadístico de prueba (X_0^2): {chi_frec:.2f}")
    print(f"-> Valor crítico (Chi_0.05, {gl_frec}): {chi_critico_frec:.2f}")
    print(f"-> Explicación: Como {chi_frec:.2f} <= {chi_critico_frec:.2f} (Estadístico <= Valor Crítico), por esa razón NO se rechaza H0.")
    print(f" CONCLUSIÓN: {'Pasan la prueba. No se rechaza H0.' if pasan_frecuencias else 'No pasan la prueba. Se rechaza H0.'}")

    # 3. PRUEBA DE PÓQUER (Clasificación de 3 dígitos)
    print("\n3) PRUEBA DE PÓQUER (Frecuencia de Dígitos - 3 Decimales)")
    print("-" * 55)
    # Probabilidades teóricas para 3 dígitos: Todos Diferentes (TD), Exactamente un Par (EP), Tercia (AM)
    prob_poker = [0.72, 0.27, 0.01]
    fe_poker = [p * N for p in prob_poker]
    fo_poker = [0, 0, 0] # [TD, EP, AM]

    for num in u:
        # Extraer los primeros 3 dígitos decimales de forma segura
        truncado = int(num * 1000)
        d1 = (truncado // 100) % 10
        d2 = (truncado // 10) % 10
        d3 = truncado % 10
        
        set_digitos = len({d1, d2, d3})
        if set_digitos == 3:   fo_poker[0] += 1 # Todos Diferentes
        elif set_digitos == 2: fo_poker[1] += 1 # Un Par
        else:                  fo_poker[2] += 1 # Tercia

    # Debido a que M = 4096, FE de tercia (0.01 * 4096 = 40.96) es >= 5, no requiere agrupación 
    chi_poker = sum(((fo_poker[i] - fe_poker[i]) ** 2) / fe_poker[i] for i in range(3)) 
    gl_poker = 3 - 1 
    chi_critico_poker = stats.chi2.ppf(1 - alpha, gl_poker) 
    pasan_poker = chi_poker <= chi_critico_poker 

    print(f"Clasificación de manos de póquer:")
    print(f"  Todos Diferentes (TD):   FO = {fo_poker[0]:<4} | FE = {fe_poker[0]:.2f}")
    print(f"  Exactamente un Par (EP): FO = {fo_poker[1]:<4} | FE = {fe_poker[1]:.2f}")
    print(f"  Tercia / Tres Iguales:   FO = {fo_poker[2]:<4} | FE = {fe_poker[2]:.2f}")
    print(f"-> Estadístico de prueba (X_0^2): {chi_poker:.2f} ")
    print(f"-> Valor crítico (Chi_0.05, {gl_poker}): {chi_critico_poker:.2f}")
    print(f"-> Explicación: Como {chi_poker:.2f} <= {chi_critico_poker:.2f} (Estadístico <= Valor Crítico), por esa razón NO se rechaza H0.")
    print(f" CONCLUSIÓN: {'Pasan la prueba. No se rechaza H0.' if pasan_poker else 'No pasan la prueba. Se rechaza H0.'}")

    # 4. PRUEBA DE LAS CORRIDAS (Versión Ascendente / Descendente) 
    print("\n4) PRUEBA DE LAS CORRIDAS (Independencia)")
    print("-" * 55)
    bits = [0 if u[i+1] >= u[i] else 1 for i in range(N - 1)] 
    
    # --- MATRIZ VISUAL DE BITS ADAPTADA DE LA PRÁCTICA 5 ---
    print("\n[MATRIZ VISUAL DE BITS GENERADOS]")
    print(f"Muestra organizada de la secuencia binaria ({len(bits)} bits totales):")
    print("." * 55)
    limite_visual = min(150, len(bits))
    for idx in range(0, limite_visual, 10):
        bloque_bits = bits[idx:idx+10]
        linea_bits = " ".join(str(b) for b in bloque_bits)
        print(f"  Pos [{idx:03d}-{min(idx+9, len(bits)-1):03d}]:  {linea_bits}")
    if len(bits) > 150:
        print("  ... [Se omiten los bits intermedios por la extensión del periodo] ...")
    print("." * 55)
    
    conteo_longitudes = {}
    corrida_actual = 1
    for i in range(1, len(bits)):
        if bits[i] == bits[i-1]:
            corrida_actual += 1
        else:
            conteo_longitudes[corrida_actual] = conteo_longitudes.get(corrida_actual, 0) + 1
            corrida_actual = 1
    conteo_longitudes[corrida_actual] = conteo_longitudes.get(corrida_actual, 0) + 1

    total_corridas_obs = sum(conteo_longitudes.values())
    total_esperado_c = (2 * N - 1) / 3 

    fe_corridas = {}
    for length in range(1, 4):
        num_fact = math.factorial(length + 3)
        p1 = (length**2 + 3*length + 1) * N
        p2 = (length**3 + 3*(length**2) - length - 4)
        fe_corridas[length] = 2 * (p1 - p2) / num_fact 

    fo_1 = conteo_longitudes.get(1, 0) 
    fo_2 = conteo_longitudes.get(2, 0) 
    fo_mayor3 = sum(conteo_longitudes.get(i, 0) for i in conteo_longitudes if i >= 3) 

    fe_1 = fe_corridas[1] 
    fe_2 = fe_corridas[2] 
    fe_mayor3 = total_esperado_c - fe_1 - fe_2 

    chi_corridas = (
        ((fo_1 - fe_1)**2 / fe_1) +
        ((fo_2 - fe_2)**2 / fe_2) +
        ((fo_mayor3 - fe_mayor3)**2 / fe_mayor3)
    ) 

    gl_corr = 3 - 1 
    chi_critico_corr = stats.chi2.ppf(1 - alpha, gl_corr)
    pasan_corridas = chi_corridas <= chi_critico_corr 

    print(f"\nResumen de Conteo de Rachas:")
    print(f"  Longitud 1:   FO = {fo_1:<4} | FE = {fe_1:.2f} ")
    print(f"  Longitud 2:   FO = {fo_2:<4} | FE = {fe_2:.2f} ")
    print(f"  Longitud >=3: FO = {fo_mayor3:<4} | FE = {fe_mayor3:.2f} ")
    print(f"-> Estadístico de prueba (X_0^2): {chi_corridas:.2f}")
    print(f"-> Valor crítico (Chi_0.05, {gl_corr}): {chi_critico_corr:.2f}")
    print(f"-> Explicación: Como {chi_corridas:.2f} <= {chi_critico_corr:.2f} (Estadístico <= Valor Crítico), por esa razón NO se rechaza H0. ")
    print(f" CONCLUSIÓN: {'Pasan la prueba. No se rechaza H0.' if pasan_corridas else 'No pasan la prueba. Se rechaza H0.'}")
    print("=" * 85)


# =========================================================================
# FLUJO PRINCIPAL
# =========================================================================
if __name__ == "__main__":
    # Forzar parámetros óptimos de la Práctica 4 por simplicidad
    semilla_input = 7326
    a_input = 21
    b_input = 11
    M_input = 4096

    # 1. Generar los números enteros de periodo completo
    numeros_enteros = generador_periodo_completo(semilla_input, a_input, b_input, M_input)

    # 2. Si el periodo es válido y completo, disparar las pruebas analíticas
    if numeros_enteros:
        ejecutar_pruebas_estadisticas(numeros_enteros, M=M_input)