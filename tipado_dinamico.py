# Script para demostrar el tipado dinámico en Python

def demostrar_tipado_dinamico():
    print("=== Demostración de Tipado Dinámico en Python ===\n")
    
    # 1. Asignación de un número entero (int)
    variable = 42
    print(f"Asignación 1: {variable}")
    print(f"Tipo determinado por Python: {type(variable)}\n")
    
    # 2. Asignación de texto (str) sin declarar nada nuevo
    variable = "Texto en la misma variable"
    print(f"Asignación 2: '{variable}'")
    print(f"Tipo cambiado a: {type(variable)}\n")
    
    # 3. Asignación de una lista (list)
    variable = [1, 2, 3, "cuatro"]
    print(f"Asignación 3: {variable}")
    print(f"Tipo cambiado a: {type(variable)}\n")
    
    print("¡Como ves, no es necesario decirle a Python qué tipo de dato vas a almacenar!")

if __name__ == "__main__":
    demostrar_tipado_dinamico()
