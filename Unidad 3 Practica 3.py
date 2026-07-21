import math

def ejercicio_1():
    print("--- EJERCICIO 1: Distribución Erlang (Suma de Exponenciales) ---")
    # Parámetros
    k = 2
    lam = 0.4
    u = [0.35, 0.62]
    print(f"(a) Identificación: X ~ Erlang({k}, {lam}). Consta de {k} sumandos Y_i, donde cada uno sigue una distribución Exponencial con tasa lambda = {lam}.")    
    # Generación de sumandos: y_i = -1/lambda * ln(u_i)
    y1 = -(1 / lam) * math.log(u[0])
    y2 = -(1 / lam) * math.log(u[1])    
    print(f"(b) Generación de sumandos:")
    print(f"    y_1 = -(1/{lam}) * ln({u[0]}) = {y1:.4f}")
    print(f"    y_2 = -(1/{lam}) * ln({u[1]}) = {y2:.4f}")    
    # Suma (Convolución)
    x = y1 + y2
    print(f"(c) Suma final: x = y_1 + y_2 = {y1:.4f} + {y2:.4f} = {x:.4f}\n")

def ejercicio_2():
    print("--- EJERCICIO 2: Distribución Binomial (Suma de Bernoulli) ---")
    # Parámetros
    n = 4
    p = 0.5
    u = [0.66, 0.28, 0.91, 0.04]
    umbral = 1 - p    
    print(f"(a) Identificación: X ~ Binomial(n={n}, p={p}). Consta de {n} sumandos Y_i, donde cada uno sigue una distribución de Bernoulli con p = {p}.")
    print(f"    Regla de decisión: Éxito (1) si u_i > {umbral}, Fracaso (0) en caso contrario.")    
    y = []
    print(f"(b) Generación de sumandos:")
    for i, ui in enumerate(u):
        val = 1 if ui > umbral else 0
        y.append(val)
        evaluacion = f"{ui} > {umbral} -> Éxito (1)" if val == 1 else f"{ui} <= {umbral} -> Fracaso (0)"
        print(f"    y_{i+1}: u_{i+1} = {ui} | ¿{evaluacion}?")        
    # Suma (Convolución)
    x = sum(y)
    print(f"(c) Suma final: x = " + " + ".join(map(str, y)) + f" = {x:.4f}\n")

def ejercicio_3():
    print("--- EJERCICIO 3: Distribución Triangular (Suma de Uniformes) ---")
    # Parámetros
    u1 = 0.45
    u2 = 0.15    
    print("(a) Identificación: T ~ Triangular(0, 2) con moda 1. Consta de la convolución (suma) de 2 variables independientes U_i ~ Uniforme(0, 1).")    
    # En la convolución directa de dos estándar U(0,1), y_i = u_i
    y1 = u1
    y2 = u2    
    print(f"(b) Generación de sumandos:")
    print(f"    y_1 = u_1 = {y1:.4f}")
    print(f"    y_2 = u_2 = {y2:.4f}")    
    # Suma (Convolución)
    t = y1 + y2
    print(f"(c) Suma final: t = y_1 + y_2 = {y1:.4f} + {y2:.4f} = {t:.4f}\n")

if __name__ == "__main__":
    ejercicio_1()
    ejercicio_2()
    ejercicio_3()