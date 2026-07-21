# Script de Python para aprender sobre entrada de datos y conversión de tipos

def capturar_datos():
    print("=== Captura de Datos en Python ===\n")
    
    # 1. Ingresar una cadena de caracteres (String)
    # Por defecto, input() siempre retorna un String.
    nombre = input("1. Introduce tu nombre (texto): ")
    print(f"Recibido: '{nombre}' | Tipo: {type(nombre)}\n")
    
    # 2. Ingresar un número entero (Integer)
    # Convertimos la entrada a entero usando int().
    try:
        edad_entrada = input("2. Introduce tu edad (entero): ")
        edad = int(edad_entrada)
        print(f"Recibido: {edad} | Tipo: {type(edad)}\n")
    except ValueError:
        print("¡Error! Lo que ingresaste no se pudo convertir a número entero.\n")
        
    # 3. Ingresar un número flotante/decimal (Float)
    # Convertimos la entrada a flotante usando float().
    try:
        estatura_entrada = input("3. Introduce tu estatura en metros (decimal, ej: 1.72): ")
        estatura = float(estatura_entrada)
        print(f"Recibido: {estatura} | Tipo: {type(estatura)}\n")
    except ValueError:
        print("¡Error! Lo que ingresaste no se pudo convertir a número decimal.\n")

if __name__ == "__main__":
    capturar_datos()
