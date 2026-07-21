import math

def ejercicio_1(u):
    print("--- EJERCICIO 1: Uniforme General ---")
    print(f"Instancia: U(3, 15) con u = {u}")
    # Fórmula generadora: x = 3 + 12 * u
    x = 3 + 12 * u
    print(f"(a) FDA: F_X(x) = (x - 3) / 12")
    print(f"(b) Igualar: u = (x - 3) / 12")
    print(f"(c) Fórmula generadora: x = 3 + 12u")
    print(f"(d) Resultado: x = {x:.4f}\n")
    return x

def ejercicio_2(u):
    print("--- EJERCICIO 2: Exponencial ---")
    print(f"Instancia: lambda = 0.25 con u = {u}")
    # Fórmula generadora: x = -ln(1 - u) / lambda
    lam = 0.25
    x = -math.log(1 - u) / lam
    print(f"(a) FDA: F_X(x) = 1 - e^(-0.25x)")
    print(f"(b) Igualar: u = 1 - e^(-0.25x)")
    print(f"(c) Fórmula generadora: x = -ln(1 - u) / 0.25")
    print(f"(d) Resultado: x = {x:.4f}\n")
    return x

def ejercicio_3(lista_u):
    print("--- EJERCICIO 3: Dado Cargado ---")
    # Datos del problema
    valores = [1, 2, 3, 4, 5, 6]
    cdf = [0.10, 0.25, 0.40, 0.60, 0.80, 1.00]
    
    print("Regla: Elegir el menor valor de x tal que F_X(x) >= u")
    for u in lista_u:
        asignado = None
        for x, f_x in zip(valores, cdf):
            if f_x >= u:
                asignado = x
                break
        print(f"Para u = {u:<4} -> El primer F_X(x) >= {u} es F_X({asignado}) = {f_x:.2f} -> Valor del dado: {asignado}")

# Ejecución de los ejercicios con los datos de la práctica
if __name__ == "__main__":
    ejercicio_1(0.62)
    ejercicio_2(0.40)
    ejercicio_3([0.08, 0.33, 0.72, 0.95])