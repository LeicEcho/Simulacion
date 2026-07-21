import math
import numpy as np

def ejercicio_1_y_2():
    print("--- EJERCICIOS 1 Y 2: Súper Ferretería Tobi ---")
    ventas = [10, 12, 14, 16, 18, 20, 22]
    frecuencias = [2, 3, 4, 6, 5, 3, 1]
    total_meses = sum(frecuencias)
    
    # Construcción de la tabla de probabilidad acumulada
    probabilidades = [f / total_meses for f in frecuencias]
    acumuladas = []
    curr = 0
    for p in probabilidades:
        curr += p
        acumuladas.append(curr)
        
    def mapear_montecarlo(r):
        for v, a in zip(ventas, acumuladas):
            if r <= a:
                return v
        return ventas[-1]
    
    # Ejercicio 1: r = 0.6500
    v_65 = mapear_montecarlo(0.6500)
    print(f"1. Para r = 0.6500 -> Volumen de ventas simulado: {v_65} M$")
    
    # Ejercicio 2: 24 números aleatorios
    r_24 = [
        0.4764, 0.6279, 0.4446, 0.5582, 0.1634, 0.8416, 0.8234, 0.6427,
        0.4959, 0.7344, 0.9434, 0.5273, 0.5902, 0.1824, 0.2809, 0.3420,
        0.1820, 0.0318, 0.7041, 0.0746, 0.6827, 0.6383, 0.5901, 0.3555
    ]
    
    valores_simulados = [mapear_montecarlo(r) for r in r_24]
    media_sim = np.mean(valores_simulados)
    std_muestral_sim = np.std(valores_simulados, ddof=1)
    
    # Datos reales
    media_real = sum(v * f for v, f in zip(ventas, frecuencias)) / total_meses
    std_poblacional_real = math.sqrt(sum(f * (v - media_real)**2 for v, f in zip(ventas, frecuencias)) / total_meses)
    
    print("\n2. Métricas Estadísticas:")
    print(f"   a) Media Simulada: {media_sim:.4f} | Desviación Estándar Muestral (n-1): {std_muestral_sim:.4f}")
    print(f"   b) Comparación:")
    print(f"      - Media Real Histórica: {media_real:.4f} (Variación de {abs(media_sim-media_real)/media_real*100:.2f}%)")
    print(f"      - Desviación Estándar Poblacional Real: {std_poblacional_real:.4f}\n")

def ejercicio_3():
    print("--- EJERCICIO 3: Distribución Uniforme Continua ---")
    r_col2 = [0.6279, 0.8234, 0.5273, 0.1820, 0.6383, 0.1471, 0.3208, 0.8224, 0.6331, 0.5482]
    print("Fórmula: x = 50 + 130 * r")
    for i, r in enumerate(r_col2, 1):
        x = 50 + r * 130
        print(f"   Valor {i:02d}: r = {r:.4f} -> x = {x:.4f}")
    print()

def ejercicio_4():
    print("--- EJERCICIO 4: Tiempos de Servicio Exponenciales (mu = 8) ---")
    r_col3 = [0.4446, 0.6427, 0.5902, 0.0318, 0.5901, 0.3044, 0.1699, 0.5783, 0.8764, 0.2161]
    mu = 8
    valores_exp = []
    print("Fórmula: x = -1/8 * ln(r)")
    for i, r in enumerate(r_col3, 1):
        x = -(1 / mu) * math.log(r)
        valores_exp.append(x)
        print(f"   Valor {i:02d}: r = {r:.4f} -> x = {x:.4f}")
        
    media_exp_sim = np.mean(valores_exp)
    media_exp_real = 1 / mu
    print(f"\nComparación de Medias:")
    print(f"   - Media Muestral Exponencial Simulada: {media_exp_sim:.4f}")
    print(f"   - Valor Real Esperado (1/mu): {media_exp_real:.4f}")

if __name__ == "__main__":
    ejercicio_1_y_2()
    ejercicio_3()
    ejercicio_4()