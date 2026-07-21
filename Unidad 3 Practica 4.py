import math

def ejercicio_1(u1, u2):
    print("--- EJERCICIO 1: Hiperexponencial ---")
    p1 = 0.5
    print(f"(a) Componentes y pesos: \n    - C1: Exp(lambda=2), p1 = {p1}\n    - C2: Exp(lambda=4), p2 = 0.5")
    
    # Selección de componente
    print(f"(b) Selección con u1 = {u1}:")
    if u1 <= p1:
        print(f"    Como u1 ({u1}) <= p1 ({p1}), elegimos la Componente 1 (Exp(2)).")
        lam = 2
    else:
        print(f"    Como u1 ({u1}) > p1 ({p1}), elegimos la Componente 2 (Exp(4)).")
        lam = 4
        
    # Generación con u2
    x = -math.log(1 - u2) / lam
    print(f"(c) Generación con u2 = {u2} (Transformada Inversa):")
    print(f"    x = -ln(1 - {u2}) / {lam} = {x:.4f}\n")
    return x

def ejercicio_2(u1, u2):
    print("--- EJERCICIO 2: Densidad Definida por Tramos ---")
    p1 = 0.4  # Área del primer tramo: base (1-0) * altura (0.4)
    p2 = 0.6  # Área del segundo tramo: base (2-1) * altura (0.6)
    print(f"(a) Componentes y pesos (áreas): \n    - C1: U(0, 1), p1 = {p1}\n    - C2: U(1, 2), p2 = {p2}")
    
    # Selección de componente
    print(f"(b) Selección con u1 = {u1}:")
    if u1 <= p1:
        print(f"    Como u1 ({u1}) <= p1 ({p1}), elegimos la Componente 1 (U(0, 1)).")
        a, b = 0, 1
    else:
        print(f"    Como u1 ({u1}) > p1 ({p1}), elegimos la Componente 2 (U(1, 2)).")
        a, b = 1, 2
        
    # Generación con u2
    x = a + (b - a) * u2
    print(f"(c) Generación con u2 = {u2} (Transformada Inversa):")
    print(f"    x = {a} + ({b} - {a}) * {u2} = {x:.4f}\n")
    return x

def ejercicio_3(u1, u2):
    print("--- EJERCICIO 3: Mezcla de dos Uniformes ---")
    p1 = 0.7
    print(f"(a) Componentes y pesos: \n    - C1: U(0, 10), p1 = {p1}\n    - C2: U(10, 20), p2 = 0.3")
    
    # Selección de componente
    print(f"(b) Selección con u1 = {u1}:")
    if u1 <= p1:
        print(f"    Como u1 ({u1}) <= p1 ({p1}), elegimos la Componente 1 (U(0, 10)).")
        a, b = 0, 10
    else:
        print(f"    Como u1 ({u1}) > p1 ({p1}), elegimos la Componente 2 (U(10, 20)).")
        a, b = 10, 20
        
    # Generación con u2
    x = a + (b - a) * u2
    print(f"(c) Generación con u2 = {u2} (Transformada Inversa):")
    print(f"    x = {a} + ({b} - {a}) * {u2} = {x:.4f}\n")
    return x

if __name__ == "__main__":
    ejercicio_1(u1=0.3, u2=0.8)
    ejercicio_2(u1=0.25, u2=0.5)
    ejercicio_3(u1=0.9, u2=0.5)