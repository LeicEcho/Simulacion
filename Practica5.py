import math
# pyrefly: ignore [missing-import]
from scipy import stats

numeros = [
    0.03991, 0.10461, 0.93716, 0.16894, 0.98953,
    0.38555, 0.95554, 0.32886, 0.59780, 0.09958,
    0.17546, 0.73704, 0.92052, 0.46215, 0.15917,
    0.32643, 0.52861, 0.95819, 0.06831, 0.19640,
    0.69572, 0.68777, 0.39510, 0.35905, 0.85244,
    0.24122, 0.66591, 0.27699, 0.06494, 0.03152,
    0.61196, 0.30231, 0.92962, 0.61773, 0.22109,
    0.30532, 0.21704, 0.10274, 0.12202, 0.94205,
    0.03788, 0.97599, 0.75867, 0.20717, 0.82037,
    0.48228, 0.63379, 0.85783, 0.47619, 0.87481,
    0.88618, 0.19161, 0.41290, 0.63312, 0.71857,
    0.71299, 0.23853, 0.05870, 0.01119, 0.92784,
    0.27954, 0.58909, 0.82444, 0.99005, 0.04921,
    0.80863, 0.00514, 0.20247, 0.81759, 0.45197,
    0.33564, 0.60780, 0.48460, 0.85558, 0.15191,
    0.90899, 0.75754, 0.60833, 0.25983, 0.01291,
    0.78038, 0.70267, 0.43529, 0.06318, 0.38384,
    0.55986, 0.66485, 0.88722, 0.56736, 0.66164,
    0.87539, 0.08823, 0.94813, 0.31900, 0.54155,
    0.16818, 0.60311, 0.74457, 0.90561, 0.72848
]

N = len(numeros)
alpha = 0.05

print("=" * 85)
print(f"SISTEMA UNIFICADO DE VALIDACIÓN ESTADÍSTICA (SCD-1022) - N = {N}")
print("=" * 85)

# -------------------------------------------------------------------------
# a) PRUEBA DE LOS PROMEDIOS
# -------------------------------------------------------------------------
print("\na) PRUEBA DE LOS PROMEDIOS (Uniformidad)")
print("-" * 55)
print("H0: mu = 0.5 (Los números tienen media compatible con 0.5)")
print("H1: mu != 0.5")

suma_u = sum(numeros)
promedio = suma_u / N
z_0 = (promedio - 0.5) * math.sqrt(N) / math.sqrt(1/12)
z_critico = stats.norm.ppf(1 - alpha / 2)
pasan_promedio = abs(z_0) <= z_critico

print(f"-> Sumatoria total (Σ Ui): {suma_u:.5f}")
print(f"-> Promedio muestral calculado (x̄): {promedio:.5f}")
print(f"-> Estadístico de prueba (Z_0): {z_0:.5f}")
print(f"-> Valor crítico (Z_alpha/2): ±{z_critico:.5f}")
print(f" CONCLUSIÓN: {'Pasan la prueba. No se rechaza H0.' if pasan_promedio else 'No pasan la prueba. Se rechaza H0.'}")


# -------------------------------------------------------------------------
# b) PRUEBA DE FRECUENCIAS 
# -------------------------------------------------------------------------
print("\nb) PRUEBA DE FRECUENCIAS (Uniformidad por Reparto)")
print("-" * 55)
print("H0: Los números se distribuyen uniformemente en el intervalo (0,1)")
print("H1: Los números no se distribuyen uniformemente")

k = 5  
fe = N / k  
fo = [0] * k

for num in numeros:
    rango = int(num * k)
    if rango == k:
        rango = k - 1
    fo[rango] += 1

chi_0_cuadrada = sum(((fo[i] - fe) ** 2) / fe for i in range(k))  
gl_frecuencias = k - 1  
chi_critico_frec = stats.chi2.ppf(1 - alpha, gl_frecuencias)
pasan_frecuencias = chi_0_cuadrada <= chi_critico_frec

print("Distribución por subintervalos:")
for idx in range(k):
    print(f"  Intervalo [{idx/k:.1f} - {(idx+1)/k:.1f}): FO = {fo[idx]}, FE = {fe}")

print(f"-> Estadístico de prueba (X_0^2): {chi_0_cuadrada:.2f}")
print(f"-> Valor crítico (Chi_0.05, {gl_frecuencias}): {chi_critico_frec:.2f}")
print(f"-> Explicación: Como {chi_0_cuadrada:.2f} < {chi_critico_frec:.2f}, por esa razón NO se rechaza H0.")
print(f" CONCLUSIÓN: {'Pasan la prueba. No se rechaza H0.' if pasan_frecuencias else 'No pasan la prueba. Se rechaza H0.'}")


# -------------------------------------------------------------------------
# c) PRUEBA DE LAS CORRIDAS 
# -------------------------------------------------------------------------
print("\nc) PRUEBA DE LAS CORRIDAS ")
print("-" * 55)
print("H0: Los números son independientes")
print("H1: Los números no son independientes")

bits = []
for i in range(N - 1):
    if numeros[i+1] >= numeros[i]:
        bits.append(0)  # Sube
    else:
        bits.append(1)  # Baja

print("\n[MATRIZ VISUAL DE BITS GENERADOS]")
print("Cada bloque representa un bit (0: Sube, 1: Baja):")
print("." * 55)
for idx in range(0, len(bits), 10):
    bloque_bits = bits[idx:idx+10]
    linea_bits = " ".join(str(b) for b in bloque_bits)
    print(f"  Pos [{idx:02d}-{min(idx+9, len(bits)-1):02d}]:  {linea_bits}")
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

fe_corridas = {}
for length in range(1, 6):
    num_fact = math.factorial(length + 3)
    p1 = (length**2 + 3*length + 1) * N
    p2 = (length**3 + 3*(length**2) - length - 4)
    fe_corridas[length] = 2 * (p1 - p2) / num_fact

total_esperado_c = (2 * N - 1) / 3 

# Agrupamiento dinámico (i >= 3) para cumplir con FE >= 5 
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

gl_corridas = 3 - 1  
chi_critico_corr = stats.chi2.ppf(1 - alpha, gl_corridas)
pasan_corridas = chi_corridas <= chi_critico_corr

print(f"\nResumen de Conteo de Rachas:")
print(f"  Longitud 1:   FO = {fo_1:<3} | FE = {fe_1:.2f}")
print(f"  Longitud 2:   FO = {fo_2:<3} | FE = {fe_2:.2f}")
print(f"  Longitud >=3: FO = {fo_mayor3:<3} | FE = {fe_mayor3:.2f}")
print(f"  Total:        FO = {total_corridas_obs:<3} | E(C) = {total_esperado_c:.2f}")

print(f"\n-> Estadístico de prueba (X_0^2): {chi_corridas:.2f}")
print(f"-> Valor crítico (Chi_0.05, {gl_corridas}): {chi_critico_corr:.2f}")
print(f"-> Explicación: Como {chi_corridas:.2f} < {chi_critico_corr:.2f}, por esa razón NO se rechaza H0.")
print(f" CONCLUSIÓN: {'Pasan la prueba. No se rechaza H0.' if pasan_corridas else 'No pasan la prueba. Se rechaza H0.'}")
print("=" * 85)