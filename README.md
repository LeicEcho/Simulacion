# Práctica 6: Batería Completa de Pruebas Estadísticas de Independencia y Uniformidad
**Autor:** Luis Alberto Castro Zúñiga

---

## 1. Introducción Teórica

En el ámbito de la simulación matemática, la generación de números pseudoaleatorios es fundamental para modelar sistemas estocásticos. Para que una secuencia de números pseudoaleatorios $\{U_i\}$ en el intervalo $[0, 1)$ sea estadísticamente válida, debe cumplir rigurosamente con dos propiedades fundamentales:

1. **Uniformidad**: Los números generados deben estar distribuidos de manera uniforme a lo largo del intervalo $(0, 1)$. Esto implica que cualquier subintervalo de igual longitud tiene la misma probabilidad de contener un número de la secuencia. Matemáticamente, la función de densidad de probabilidad de la variable aleatoria $U$ debe ser: <img src="https://latex.codecogs.com/svg.image?\color{white}f(u)%20=%20\begin{cases}%201%20&%20\text{si%20}%200%20\le%20u%20\le%201%20\\%200%20&%20\text{en%20otro%20caso}%20\end{cases}" title="f(u)" style="background-color: #1A1A1A; padding: 10px; border-radius: 5px;" />

2. **Independencia**: No debe existir correlación, patrón o dependencia entre los números sucesivos de la secuencia. La ocurrencia de un valor no debe influir ni permitir predecir el valor del siguiente número generado. Matemáticamente, para cualquier par de variables aleatorias $U_i$ y $U_j$ (con $i \neq j$):
   $$P(U_i \le u_i, U_j \le u_j) = P(U_i \le u_i) \cdot P(U_j \le u_j)$$

Para validar que nuestro generador cumple con estas propiedades, se implementa una batería completa de pruebas estadísticas divididas en dos categorías principales:
* **Pruebas de Uniformidad**: Prueba de los Promedios y Prueba de Frecuencias.
* **Pruebas de Independencia**: Prueba de Póquer y Prueba de las Corridas Arriba/Abajo.
## 2. Desglose de las 4 Pruebas Estadísticas

### A) Prueba de los Promedios (Uniformidad)
Esta prueba evalúa si el promedio de la muestra es estadísticamente igual al promedio teórico esperado de una distribución uniforme continua en el intervalo $(0, 1)$, el cual es $\mu = 0.5$.

* **Hipótesis**:
  $$H_0: \mu = 0.5 \quad \text{(La media de la población es compatible con 0.5)}$$
  $$H_1: \mu \neq 0.5 \quad \text{(La media de la población no es compatible con 0.5)}$$

* **Estadístico de Prueba**:
  El promedio muestral se calcula como:
  $$\bar{x} = \frac{1}{N} \sum_{i=1}^{N} U_i$$
  
  Dado que la varianza teórica de una distribución uniforme continua es $\sigma^2 = \frac{1}{12}$, el estadístico de prueba estandarizado $Z_0$ sigue una distribución normal estándar bajo $H_0$:
  $$Z_0 = \frac{(\bar{x} - 0.5)\sqrt{N}}{\sqrt{1/12}} = (\bar{x} - 0.5)\sqrt{12N}$$

* **Criterio de Aceptación/Rechazo (Zona Crítica)**:
  Se acepta la hipótesis nula $H_0$ si el valor absoluto del estadístico calculado es menor o igual al valor crítico de la distribución normal estándar para un nivel de significancia $\alpha$:
  $$|Z_0| \le Z_{\alpha/2}$$
  Para $\alpha = 0.05$, el valor crítico es $Z_{0.025} \approx 1.96$. Si $|Z_0| \le 1.96$, no se rechaza $H_0$.

---

### B) Prueba de Frecuencias (Uniformidad por Reparto)
Determina si los números pseudoaleatorios se distribuyen uniformemente en subintervalos del mismo tamaño dentro del intervalo $(0, 1)$.

* **Hipótesis**:
  $$H_0: \text{Los números se distribuyen uniformemente en el intervalo } (0, 1)$$
  $$H_1: \text{Los números no se distribuyen uniformemente en el intervalo } (0, 1)$$

* **Estadístico de Prueba**:
  Se divide el intervalo $(0, 1)$ en $k$ subintervalos de igual ancho. Se cuenta la frecuencia observada ($O_i$) en cada subintervalo y se compara con la frecuencia esperada teórica ($E_i = N/k$). El estadístico de prueba sigue una distribución Chi-cuadrada con $k-1$ grados de libertad:
  $$\chi_0^2 = \sum_{i=1}^{k} \frac{(O_i - E_i)^2}{E_i}$$

* **Criterio de Aceptación/Rechazo (Zona Crítica)**:
  Se acepta la hipótesis nula $H_0$ si el estadístico calculado $\chi_0^2$ es menor o igual al valor crítico de la tabla Chi-cuadrada con significancia $\alpha$ y $k-1$ grados de libertad:
  $$\chi_0^2 \le \chi_{\alpha, k-1}^2$$
  Si $\chi_0^2 > \chi_{\alpha, k-1}^2$, se rechaza $H_0$ en favor de $H_1$.

---

### C) Prueba de Póquer (Independencia por Frecuencia de Dígitos)
Analiza la frecuencia con la que se repiten ciertos dígitos decimales individuales en los números generados para determinar si existe independencia. Se extraen los 3 primeros dígitos decimales de cada número.

* **Hipótesis**:
  $$H_0: \text{Los números pseudoaleatorios son independientes}$$
  $$H_1: \text{Los números pseudoaleatorios no son independientes}$$

* **Clasificación de Manos (3 dígitos)**:
  1. **Todos Diferentes (TD)**: Los tres dígitos son distintos (ej. 0.124 $\to$ 1, 2, 4). Probabilidad teórica: $P(\text{TD}) = 0.72$
  2. **Exactamente un Par (EP)**: Dos dígitos son iguales y uno diferente (ej. 0.443 $\to$ 4, 4, 3). Probabilidad teórica: $P(\text{EP}) = 0.27$
  3. **Tercia / Tres Iguales**: Los tres dígitos son iguales (ej. 0.555 $\to$ 5, 5, 5). Probabilidad teórica: $P(\text{T}) = 0.01$

* **Estadístico de Prueba**:
  Se clasifica cada número y se calcula el estadístico Chi-cuadrada con 2 grados de libertad (3 clases menos 1):
  $$\chi_0^2 = \sum_{j=1}^{3} \frac{(O_j - E_j)^2}{E_j}$$
  Donde $E_j = P_j \cdot N$ es la frecuencia esperada para cada clase $j$.

* **Criterio de Aceptación/Rechazo (Zona Crítica)**:
  Se acepta $H_0$ si:
  $$\chi_0^2 \le \chi_{\alpha, 2}^2$$
  Para $\alpha = 0.05$, el valor crítico es $\chi_{0.05, 2}^2 \approx 5.99$.

---

### D) Prueba de las Corridas Arriba y Abajo (Independencia por Tendencia)
Evalúa la aleatoriedad secuencial contando las longitudes de rachas crecientes (corridas arriba) y decrecientes (corridas abajo).

* **Hipótesis**:
  $$H_0: \text{Los números de la secuencia son independientes}$$
  $$H_1: \text{Los números de la secuencia no son independientes}$$

* **Secuencia de Tendencia (Bits)**:
  Se genera una secuencia binaria $S_i$ de longitud $N-1$:
  <img src="https://latex.codecogs.com/svg.image?\color{white}S_i%20=%20\begin{cases}%200%20&%20\text{si%20}%20U_{i+1}%20\ge%20U_i%20\\%201%20&%20\text{si%20}%20U_{i+1}%20<%20U_i%20\end{cases}" title="S_i" style="background-color: #1A1A1A; padding: 10px; border-radius: 5px;" />

* **Frecuencias Esperadas**:
  Las corridas se agrupan en longitudes de 1, 2 y $\ge 3$. La frecuencia esperada teórica para cada longitud de corrida $j$ (para $j < N-1$) viene dada por:
  $$E(h_j) = \frac{2 \cdot \left[ (j^2 + 3j + 1)N - (j^3 + 3j^2 - j - 4) \right]}{(j + 3)!}$$
  El valor total esperado de corridas $E(C)$ es:
  $$E(C) = \frac{2N - 1}{3}$$
  Y para el intervalo de corridas largas de longitud mayor o igual a 3:
  $$E(h_{\ge 3}) = E(C) - E(h_1) - E(h_2)$$

* **Estadístico de Prueba**:
  El estadístico Chi-cuadrada se calcula con 2 grados de libertad (3 categorías de longitud de corrida):
  $$\chi_0^2 = \sum_{j=1}^{3} \frac{(O_j - E_j)^2}{E_j}$$

* **Criterio de Aceptación/Rechazo (Zona Crítica)**:
  Se acepta la independencia ($H_0$) si el estadístico calculado no supera el valor de la distribución Chi-cuadrada crítica:
  $$\chi_0^2 \le \chi_{\alpha, 2}^2$$
  Para $\alpha = 0.05$, el valor crítico es $\chi_{0.05, 2}^2 \approx 5.99$.
