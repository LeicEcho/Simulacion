def generador_periodo_completo(semilla, a, b, M):
    secuencia = []
    registro_apariciones = {}
    
    X = semilla % M
    ciclo_completo_alcanzado = False
    
    print(f"\nConfiguración del espacio modular:")
    print(f"Semilla operativa inicial: {X} | Multiplicador (a): {a} | Incremento (b): {b} | Módulo (M): {M}")
    print("-" * 85)

    # Corremos el bucle hasta M + 1 para capturar la iteración exacta de la repetición
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


def mostrar_muestras_justificadas(secuencia, total_a_mostrar=50):
    # Muestra los primeros y últimos elementos para no saturar la pantalla
    print(f"\nVisualización del periodo generado (Muestra de los primeros y últimos {total_a_mostrar} números):")
    print("=" * 85)
    
    print(f"--- PRIMEROS {total_a_mostrar} NÚMEROS ---")
    bloque_inicio = secuencia[:total_a_mostrar]
    for i in range(0, len(bloque_inicio), 10):
        linea = "".join(f"{num:<8}" for num in bloque_inicio[i:i+10])
        print(f"   {linea}")
        
    print("\n   ... [Se omiten los números intermedios del periodo completo] ...\n")
    
    print(f"--- ÚLTIMOS {total_a_mostrar} NÚMEROS ---")
    bloque_fin = secuencia[-total_a_mostrar:]
    for i in range(0, len(bloque_fin), 10):
        linea = "".join(f"{num:<8}" for num in bloque_fin[i:i+10])
        print(f"   {linea}")
    print("=" * 85)


# =========================================================================
# MENÚ DE CONFIGURACIÓN DE LA NUEVA PRÁCTICA
# =========================================================================

# Parámetros sugeridos que cumplen Hull-Dobell para M = 4096:
# M = 4096 (2^12)
# b = 11 (Impar, coprimo con 4096)
# a = 21 (21 - 1 = 20, que es perfectamente divisible entre 4)
# Semilla = Cualquier entero, por ejemplo, 7326 (la de tu práctica anterior)

print("GENERADOR DE NÚMEROS PSEUDOALEATORIOS - PERIODO MÁXIMO")
print("=" * 85)

usar_defecto = input("¿Deseas usar los parámetros óptimos por defecto para garantizar M=4096? (S/N): ").strip().upper()

if usar_defecto == 'S' or usar_defecto == '':
    semilla_input = 7326
    a_input = 21
    b_input = 11
    M_input = 4096
else:
    semilla_input = int(input("Introduce la semilla inicial (X0): "))
    a_input = int(input("Introduce la constante multiplicativa (a): "))
    b_input = int(input("Introduce la constante aditiva (b): "))
    M_input = int(input("Introduce el módulo deseado (M >= 4096): "))

# Ejecución del algoritmo
numeros_generados = generador_periodo_completo(semilla_input, a_input, b_input, M_input)

if numeros_generados:
    mostrar_muestras_justificadas(numeros_generados, total_a_mostrar=50)