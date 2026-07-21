def cuadrado_medio_hasta_repetir(semilla_inicial):
    secuencia = []
    repetidos = set()
    semilla = semilla_inicial
    n = len(str(semilla_inicial))  # Cantidad de dígitos (n=4) [cite: 78, 87]
    
    pos_repeticion = -1
    valor_repetido = None
    iteracion = 1

    while True:
        al_cuadrado = semilla ** 2  # Elevar la semilla al cuadrado [cite: 81]
        # Ajustar a longitud 2n (8 dígitos) agregando ceros a la izquierda si es necesario [cite: 82, 89]
        cadena_cuadrado = str(al_cuadrado).zfill(2 * n)
        
        # Extraer los n dígitos centrales [cite: 83, 91]
        inicio = (len(cadena_cuadrado) - n) // 2
        centro = int(cadena_cuadrado[inicio:inicio + n])
        
        secuencia.append(centro)
        
        if centro in repetidos:
            pos_repeticion = iteracion
            valor_repetido = centro
            break
            
        repetidos.add(centro)
        semilla = centro
        iteracion += 1
        
    return secuencia, pos_repeticion, valor_repetido


def congruencial_rastreo_ciclos(semilla_inicial, a, b, M, max_iteraciones=10000):
    # Diccionario para registrar { valor_generado: numero_de_iteracion_donde_aparecio }
    registro_apariciones = {}
    secuencia_historica = []
    
    # Ajustar la semilla al espacio modular por seguridad [cite: 125]
    X = semilla_inicial % M
    
    pos_primera = -1
    pos_segunda = -1
    valor_repetido = None

    for i in range(1, max_iteraciones + 1):
        # Fórmula congruencial mixta: X_i = (a * X_{i-1} + b) % M [cite: 108, 116]
        X = (a * X + b) % M
        secuencia_historica.append(X)
        
        if X in registro_apariciones:
            pos_primera = registro_apariciones[X]
            pos_segunda = i
            valor_repetido = X
            break
            
        registro_apariciones[X] = i
        
    return secuencia_historica, pos_primera, pos_segunda, valor_repetido


def imprimir_bloque_justificado(secuencia):
    # Imprime una lista en bloques de 10 números alineados en columnas fijas
    for i in range(0, len(secuencia), 10):
        bloque = secuencia[i:i+10]
        linea_formateada = "".join(f"{num:<7}" for num in bloque)
        print(linea_formateada)


# =========================================================================
# FLUX DE EJECUCIÓN AJUSTADO
# =========================================================================

print("="*80)
print("EJERCICIOS 1 Y 2: Método del Cuadrado Medio (Secuencia Completa)")
print("="*80)
secuencia_cm, pos_cm, val_cm = cuadrado_medio_hasta_repetir(7326) # Semilla de la práctica [cite: 953]
print(f"Semilla inicial: 7326")
print(f"La repetición ocurre en la iteración N°: {pos_cm} (Valor repetido: {val_cm})\n")
print(f"Secuencia generada desde el inicio (Números 1 al {pos_cm}):")
print("-" * 80)
imprimir_bloque_justificado(secuencia_cm)
print("-" * 80)


# Configuración estructurada SOLO para los ejercicios 3 y 4 [cite: 955, 959]
ejercicios_congruenciales = [
    {"num": "3", "a": 13, "b": 7, "M": 1024, "semillas": [473, 8432, 4728]},
    {"num": "4", "a": 25, "b": 13, "M": 2048, "semillas": [2537, 4694, 6598]}
]

for ej in ejercicios_congruenciales:
    print("\n" + "="*80)
    print(f"EJERCICIO {ej['num']}: Método Congruencial (a={ej['a']}, b={ej['b']}, M={ej['M']})")
    print("="*80)
    
    for s in ej["semillas"]:
        secuencia, p_primera, p_segunda, val = congruencial_rastreo_ciclos(s, ej["a"], ej["b"], ej["M"])
        lapso_periodo = p_segunda - p_primera
        
        print(f"-> Semilla {s} detonó ciclo en la iteración N°: {p_segunda} (Valor repetido: {val})")
        print(f"   Historial matemático: Apareció por 1° vez en iteración {p_primera} y por 2° vez en {p_segunda}.")
        print(f"   El periodo exacto de este ciclo es de: {lapso_periodo} iteraciones.\n")
        
        # --- BLOQUE 1: Ventana de la primera aparición ---
        idx_inicio_p1 = max(0, p_primera - 3)
        idx_fin_p1 = min(len(secuencia), p_primera + 2)
        bloque_primera = secuencia[idx_inicio_p1:idx_fin_p1]
        str_bloque_p1 = "  ".join(f"[{num}]" if (idx_inicio_p1 + idx + 1) == p_primera else f"{num}" for idx, num in enumerate(bloque_primera))
        
        # --- BLOQUE 2: Ventana de la segunda aparición ---
        idx_inicio_p2 = max(0, p_segunda - 5)
        bloque_segunda = secuencia[idx_inicio_p2:p_segunda]
        str_bloque_p2 = "  ".join(f"[{num}]" if (idx_inicio_p2 + idx + 1) == p_segunda else f"{num}" for idx, num in enumerate(bloque_segunda))
        
        print(f"   [Muestra Visual del Lapso]")
        print(f"   Entorno de la 1° aparición (Iteraciones {idx_inicio_p1+1} a {idx_fin_p1}):")
        print(f"     {str_bloque_p1}")
        print(f"     ...")
        print(f"   Entorno de la 2° aparición e intercepción (Iteraciones {idx_inicio_p2+1} a {p_segunda}):")
        print(f"     {str_bloque_p2}")
        print("   " + "-" * 72)


# =========================================================================
# SECCIÓN ESPECIAL: EJERCICIO 5 
# =========================================================================
print("\n" + "="*80)
print("EJERCICIO 5: Caso Especial (a=45, b=23, M=512, Semilla=9825)")
print("="*80)

# Ejecutar el algoritmo para la semilla de la práctica
secuencia_5, p_primera_5, p_segunda_5, val_5 = congruencial_rastreo_ciclos(9825, a=45, b=23, M=512)

# Imprimir los primeros 20 números generados solicitados por la práctica 
print("Primeros 20 números pseudoaleatorios generados:")
print("-" * 80)
primeros_20 = secuencia_5[:20]
imprimir_bloque_justificado(primeros_20)
print("-" * 80)

# Información complementaria del comportamiento del ciclo obtenido del análisis
print(f"\nAnálisis del ciclo:")
print(f"-> La repetición se intercepta en la iteración N°: {p_segunda_5} (Valor: {val_5})")
print(f"   Apareció por primera vez en la iteración: {p_primera_5}")
print(f"   Periodo alcanzado: {p_segunda_5 - p_primera_5} iteraciones (Periodo Completo).")
print("="*80)