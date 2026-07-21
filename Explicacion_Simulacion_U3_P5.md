# Reporte: Resolución de Ejercicios por el Método de Montecarlo (Práctica #5)

Este documento expone la resolución paso a paso de los problemas de la **Práctica #5 (Unidad 3)**, empleando la metodología de **Simulación de Montecarlo**. Este método permite recrear el comportamiento de variables aleatorias (tanto discretas como continuas) a partir de números pseudoaleatorios uniformemente distribuidos entre 0 y 1, $r \sim \mathcal{U}(0,1)$.

---

## Ejercicio 1: Súper Ferretería Tobi (Distribución Discreta)
**Enunciado:** Construir la tabla de probabilidades acumuladas para los ingresos mensuales y determinar el volumen de ventas correspondiente al número aleatorio $r = 0.6500$.

### Paso a paso:
1. **Calcular el total de meses registrados:**
   $$\text{Total} = 2 + 3 + 4 + 6 + 5 + 3 + 1 = 24 \text{ meses}$$

2. **Calcular la probabilidad individual $P(X = x)$ y la probabilidad acumulada $F_X(x)$:**
   La probabilidad se obtiene dividiendo la frecuencia de cada tramo entre el total de meses (24). La acumulada es la suma progresiva de estas probabilidades.

| Volumen de Ventas ($M\$) | Frecuencia (Meses) | Probabilidad $P(X=x)$ | Probabilidad Acumulada $F_X(x)$ | Rango de Números Aleatorios ($r$) |
| :---: | :---: | :---: | :---: | :---: |
| **10** | 2 | $2/24 \approx 0.0833$ | $2/24 \approx 0.0833$ | $0.0000 < r \le 0.0833$ |
| **12** | 3 | $3/24 \approx 0.1250$ | $5/24 \approx 0.2083$ | $0.0833 < r \le 0.2083$ |
| **14** | 4 | $4/24 \approx 0.1667$ | $9/24 = 0.3750$ | $0.2083 < r \le 0.3750$ |
| **16** | 6 | $6/24 \approx 0.2500$ | $15/24 = 0.6250$ | $0.3750 < r \le 0.6250$ |
| **18** | 5 | $5/24 \approx 0.2083$ | $20/24 \approx 0.8333$ | $0.6250 < r \le 0.8333$ |
| **20** | 3 | $3/24 \approx 0.1250$ | $23/24 \approx 0.9583$ | $0.8333 < r \le 0.9583$ |
| **22** | 1 | $1/24 \approx 0.0417$ | $24/24 = 1.0000$ | $0.9583 < r \le 1.0000$ |

3. **Evaluación para $r = 0.6500$:**
   Ubicamos el valor $0.6500$ dentro de los rangos asignados. Observamos que:
   $$0.6250 < 0.6500 \le 0.8333$$
   Este intervalo corresponde exactamente a la fila de la acumulada de **18**.
   * **Resultado:** El volumen de ventas simulado para $r = 0.6500$ es **18 M\$**.

---

## Ejercicio 2: Generación de 24 Valores y Análisis Estadístico
**Enunciado:** Usar los 24 números aleatorios del apéndice (leídos renglón por renglón) para simular 24 meses de ventas, obtener su media y desviación estándar, y compararlos con los datos reales.

### Mapeo de los 24 valores:
Usor los rangos definidos en el Ejercicio 1 para convertir cada $r$ en un valor de ventas:
1. $0.4764 \rightarrow \mathbf{16}$ (pues $0.3750 < 0.4764 \le 0.6250$)
2. $0.6279 \rightarrow \mathbf{18}$ (pues $0.6250 < 0.6279 \le 0.8333$)
3. $0.4446 \rightarrow \mathbf{16}$
4. $0.5582 \rightarrow \mathbf{16}$
5. $0.1634 \rightarrow \mathbf{1 2}$ (pues $0.0833 < 0.1634 \le 0.2083$)
6. $0.8416 \rightarrow \mathbf{20}$ (pues $0.8333 < 0.8416 \le 0.9583$)
7. $0.8234 \rightarrow \mathbf{18}$
8. $0.6427 \rightarrow \mathbf{18}$
9. $0.4959 \rightarrow \mathbf{16}$
10. $0.7344 \rightarrow \mathbf{18}$
11. $0.9434 \rightarrow \mathbf{20}$
12. $0.5273 \rightarrow \mathbf{16}$
13. $0.5902 \rightarrow \mathbf{16}$
14. $0.1824 \rightarrow \mathbf{1 2}$
15. $0.2809 \rightarrow \mathbf{14}$ (pues $0.2083 < 0.2809 \le 0.3750$)
16. $0.3420 \rightarrow \mathbf{14}$
17. $0.1820 \rightarrow \mathbf{1 2}$
18. $0.0318 \rightarrow \mathbf{10}$ (pues $0.0000 < 0.0318 \le 0.0833$)
19. $0.7041 \rightarrow \mathbf{18}$
20. $0.0746 \rightarrow \mathbf{10}$
21. $0.6827 \rightarrow \mathbf{18}$
22. $0.6383 \rightarrow \mathbf{18}$
23. $0.5901 \rightarrow \mathbf{16}$
24. $0.3555 \rightarrow \mathbf{14}$

**Lista de valores simulados:** `[16, 18, 16, 16, 12, 20, 18, 18, 16, 18, 20, 16, 16, 12, 14, 14, 12, 10, 18, 10, 18, 18, 16, 14]`

### a) Cálculo de Métricas Estadísticas de los Datos Generados:
* **Media Muestral ($\bar{x}$):**
  $$\bar{x} = \frac{\sum x_i}{24} = \frac{376}{24} = \mathbf{15.6667}$$
* **Desviación Estándar Muestral ($s$ - con $n-1$):**
  $$s = \sqrt{\frac{\sum (x_i - \bar{x})^2}{23}} = \mathbf{2.8691}$$
* **Desviación Estándar Poblacional ($\sigma$ - con $n$):**
  $$\sigma = \sqrt{\frac{\sum (x_i - \bar{x})^2}{24}} = \mathbf{2.8087}$$

### b) Comparación con los Datos Reales del Historial:
Calculamos las métricas reales a partir de las frecuencias originales:
* **Media Real ($\mu_{\text{real}}$):**
  $$\mu_{\text{real}} = \frac{(10\times2)+(12\times3)+(14\times4)+(16\times6)+(18\times5)+(20\times3)+(22\times1)}{24} = \frac{380}{24} = \mathbf{15.8333}$$
* **Desviación Estándar Poblacional Real ($\sigma_{\text{real}}$):**
  $$\sigma_{\text{real}} = \mathbf{3.1579}$$
* **Desviación Estándar Muestral Real ($s_{\text{real}}$):**
  $$s_{\text{real}} = \mathbf{3.2258}$$

**Conclusión:** Los valores simulados mediante Montecarlo reproducen con gran fidelidad el comportamiento real del sistema. La media simulada ($15.6667$) presenta una variación menor al 1% respecto a la real ($15.8333$), y la desviación estándar refleja la dispersión natural del histórico.

---

## Ejercicio 3: Distribución Uniforme Continua
**Enunciado:** Generar 10 valores para una distribución uniforme en el intervalo $[50, 180]$ usando la segunda columna de números aleatorios.

La fórmula de transformación inversa para una distribución uniforme continua es:
$$x = U + r(V - U)$$
Sustituyendo los límites dados ($U = 50, V = 180$):
$$x = 50 + r(180 - 50) \implies x = 50 + 130r$$

### Evaluaciones numéricas (Columna 2):
1. Para $r = 0.6279 \implies x = 50 + 130(0.6279) = 50 + 81.627 = \mathbf{131.6270}$
2. Para $r = 0.8234 \implies x = 50 + 130(0.8234) = 50 + 107.042 = \mathbf{157.0420}$
3. Para $r = 0.5273 \implies x = 50 + 130(0.5273) = 50 + 68.549 = \mathbf{118.5490}$
4. Para $r = 0.1820 \implies x = 50 + 130(0.1820) = 50 + 23.66 = \mathbf{73.6600}$
5. Para $r = 0.6383 \implies x = 50 + 130(0.6383) = 50 + 82.979 = \mathbf{132.9790}$
6. Para $r = 0.1471 \implies x = 50 + 130(0.1471) = 50 + 19.123 = \mathbf{69.1230}$
7. Para $r = 0.3208 \implies x = 50 + 130(0.3208) = 50 + 41.704 = \mathbf{91.7040}$
8. Para $r = 0.8224 \implies x = 50 + 130(0.8224) = 50 + 106.912 = \mathbf{156.9120}$
9. Para $r = 0.6331 \implies x = 50 + 130(0.6331) = 50 + 82.303 = \mathbf{132.3030}$
10. Para $r = 0.5482 \implies x = 50 + 130(0.5482) = 50 + 71.266 = \mathbf{121.2660}$

---

## Ejercicio 4: Tiempos de Servicio Exponenciales
**Enunciado:** Obtener 10 valores de tiempos de servicio distribuidos exponencialmente con parámetro de tasa $\mu = 8$ utilizando la tercera columna de números aleatorios y comparar la media muestral con el valor teórico real.

La fórmula de generación dada en las instrucciones es:
$$x = -\frac{1}{\mu} \ln r$$
Sustituyendo $\mu = 8$:
$$x = -\frac{1}{8} \ln r = -0.125 \ln r$$

### Evaluaciones numéricas (Columna 3):
1. Para $r = 0.4446 \implies x = -0.125 \ln(0.4446) = -0.125(-0.81057) = \mathbf{0.1013}$
2. Para $r = 0.6427 \implies x = -0.125 \ln(0.6427) = -0.125(-0.44209) = \mathbf{0.0553}$
3. Para $r = 0.5902 \implies x = -0.125 \ln(0.5902) = -0.125(-0.52730) = \mathbf{0.0659}$
4. Para $r = 0.0318 \implies x = -0.125 \ln(0.0318) = -0.125(-3.44830) = \mathbf{0.4310}$
5. Para $r = 0.5901 \implies x = -0.125 \ln(0.5901) = -0.125(-0.52747) = \mathbf{0.0659}$
6. Para $r = 0.3044 \implies x = -0.125 \ln(0.3044) = -0.125(-1.18941) = \mathbf{0.1487}$
7. Para $r = 0.1699 \implies x = -0.125 \ln(0.1699) = -0.125(-1.77259) = \mathbf{0.2216}$
8. Para $r = 0.5783 \implies x = -0.125 \ln(0.5783) = -0.125(-0.54768) = \mathbf{0.0685}$
9. Para $r = 0.8764 \implies x = -0.125 \ln(0.8764) = -0.125(-0.13193) = \mathbf{0.0165}$
10. Para $r = 0.2161 \implies x = -0.125 \ln(0.2161) = -0.125(-1.53201) = \mathbf{0.1915}$

### Comparación de medias:
* **Media Muestral Simulada ($\bar{x}_{\text{exp}}$):**
  $$\bar{x}_{\text{exp}} = \frac{0.1013 + 0.0553 + 0.0659 + 0.4310 + 0.0659 + 0.1487 + 0.2216 + 0.0685 + 0.0165 + 0.1915}{10} = \mathbf{0.1366}$$
* **Valor Real Esperado (Teórico):**
  Dado que la fórmula estructural es $x = -\frac{1}{\mu} \ln r$, la media teórica esperada es la inversa del parámetro de tasa:
  $$E(X) = \frac{1}{\mu} = \frac{1}{8} = \mathbf{0.1250}$$

**Conclusión:** La media obtenida mediante la simulación de 10 valores es **0.1366**, la cual está muy próxima al valor esperado real de **0.1250** (diferencia absoluta de apenas 0.0116). A medida que el número de iteraciones aumente (Ley de los Grandes Números), la media muestral convergerá exactamente a 0.1250.