# Script de Python para sumar dos números

def sumar_numeros(a, b):
    return a + b

if __name__ == "__main__":
    # Valores de prueba
    num1 = 12.5
    num2 = 7.3
    
    resultado = sumar_numeros(num1, num2)
    print(f"La suma de {num1} + {num2} es {resultado}")
    
    print("\n--- Suma Interactiva ---")
    try:
        # Nota: input() siempre lee texto (string), por lo que debemos
        # convertirlo a flotante (float) o entero (int) antes de sumar.
        entrada1 = float(input("Escribe el primer número: "))
        entrada2 = float(input("Escribe el segundo número: "))
        
        total = sumar_numeros(entrada1, entrada2)
        print(f"El resultado de la suma interactiva es: {total}")
    except ValueError:
        print("Error: Por favor, introduce solo números válidos.")
