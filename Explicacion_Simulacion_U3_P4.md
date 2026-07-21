# Reporte: Resolución de Ejercicios por el Método de Composición (Práctica #4)

Este documento contiene el desglose analítico y procedimental para resolver los ejercicios de la **Práctica #4 (Unidad 3)** utilizando el **Método de Composición**. 

El método de composición se aplica cuando la función de densidad de probabilidad (FDP) de una variable aleatoria compleja puede expresarse como una mezcla o combinación lineal de $m$ funciones de densidad más simples, es decir:
$$f_X(x) = \sum_{i=1}^{m} p_i f_i(x)$$
Donde cada $p_i$ representa el peso (probabilidad) de elegir la componente $f_i(x)$, cumpliendo rigurosamente que $\sum p_i = 1$. Este método requiere el gasto coordinado de **dos números uniformes**: $u_1$ para seleccionar la componente y $u_2$ para generar el valor a partir de la componente seleccionada.

---

## Ejercicio 1: Hiperexponencial (Mezcla de dos exponenciales)
**Enunciado:** Sea la densidad $f_X(x) = 0.5(2e^{-2x}) + 0.5(4e^{-4x})$ para $x \ge 0$. Genere una observación con $u_1 = 0.3$ y $u_2 = 0.8$.

### (a) Identificación de componentes y sus pesos $p_i$
La función dada está explícitamente estructurada como una composición de dos densidades exponenciales:
*   **Componente 1 ($f_1(x)$):** Distribución Exponencial con tasa $\lambda_1 = 2$ ($2e^{-2x}$). Su peso asociado es **$p_1 = 0.5$**.
*   **Componente 2 ($f_2(x)$):** Distribución Exponencial con tasa $\lambda_2 = 4$ ($4e^{-4x}$). Su peso asociado es **$p_2 = 0.5$**.

### (b) Selección de la componente con $u_1 = 0.3$
Calculamos los pesos acumulados del sistema para definir las fronteras de decisión:
*   Intervalo para la Componente 1: $[0.0, 0.5]$
*   Intervalo para la Componente 2: $(0.5, 1.0]$

Evaluamos el primer número pseudoaleatorio $u_1 = 0.3$:
¿$u_1 \le 0.5$? **Sí ($0.3 \le 0.5$)**.
*   **Decisión:** Se selecciona la **Componente 1** (Distribución Exponencial con $\lambda = 2$).

### (c) Generación del valor de la componente elegida con $u_2 = 0.8$
Aplicamos el método de la transformada inversa a la componente seleccionada. La fórmula generadora de una distribución exponencial basada en el despeje analítico formal es:
$$x = -\frac{\ln(1 - u_2)}{\lambda}$$

Sustituyendo los valores del problema ($\lambda_1 = 2$ y $u_2 = 0.8$):
$$x = -\frac{\ln(1 - 0.8)}{2}$$
$$x = -\frac{\ln(0.2)}{2}$$
$$x = -\frac{-1.6094379}{2}$$
$$x = 0.8047189...$$

Redondeando a cuatro cifras decimales:
*   **Resultado Final:** $x = 0.8047$

---

## Ejercicio 2: Densidad Definida por Tramos
**Enunciado:** Sea $f_X(x) = 0.4$ en $0 \le x \le 1$ y $f_X(x) = 0.6$ en $1 < x \le 2$. Genere una observación con $u_1 = 0.25$ y $u_2 = 0.5$.

### (a) Identificación de componentes y sus pesos $p_i$
Para funciones definidas por tramos constantes (rectángulos), el peso $p_i$ de cada tramo equivale al área geométrica bajo la curva en dicho intervalo ($A = \text{base} \times \text{altura}$):
*   **Componente 1 ($f_1(x)$):** Intervalo $[0, 1]$. Área = $(1 - 0) \times 0.4 = 0.4$. Su peso es **$p_1 = 0.4$** y su comportamiento es una distribución **Uniforme continua $\mathcal{U}(0, 1)$**.
*   **Componente 2 ($f_2(x)$):** Intervalo $(1, 2]$. Área = $(2 - 1) \times 0.6 = 0.6$. Su peso es **$p_2 = 0.6$** y su comportamiento es una distribución **Uniforme continua $\mathcal{U}(1, 2)$**.

*Nota de verificación: $\sum p_i = 0.4 + 0.6 = 1.0$, lo que valida que es una función de densidad legítima.*

### (b) Selección de la componente con $u_1 = 0.25$
Establecemos los límites basados en la probabilidad acumulada:
*   Intervalo para la Componente 1: $[0.0, 0.4]$
*   Intervalo para la Componente 2: $(0.4, 1.0]$

Evaluamos el número pseudoaleatorio $u_1 = 0.25$:
¿$u_1 \le 0.4$? **Sí ($0.25 \le 0.4$)**.
*   **Decisión:** Se selecciona la **Componente 1** (Distribución Uniforme $\mathcal{U}(0, 1)$).

### (c) Generación del valor de la componente elegida con $u_2 = 0.5$
Utilizamos la fórmula generadora estándar para una distribución uniforme en el intervalo $[a, b]$, dada por $x = a + (b - a)u_2$:
Sustituyendo los límites de la primera componente ($a = 0, b = 1$) junto a $u_2 = 0.5$:
$$x = 0 + (1 - 0)(0.5)$$
$$x = 0.5000$$

Redondeando a cuatro cifras decimales:
*   **Resultado Final:** $x = 0.5000$

---

## Ejercicio 3: Mezcla de dos Uniformes
**Enunciado:** Una señal es de tipo A con probabilidad 0.7 (valor en $\mathcal{U}(0,10)$) o de tipo B con probabilidad 0.3 (valor en $\mathcal{U}(10,20)$). Genere una observación con $u_1 = 0.9$ y $u_2 = 0.5$.

### (a) Identificación de componentes y sus pesos $p_i$
El enunciado define directamente las probabilidades de activación y los rangos de salida:
*   **Componente 1 (Tipo A):** Distribución Uniforme continua $\mathcal{U}(0, 10)$ con un peso de **$p_1 = 0.7$**.
*   **Componente 2 (Tipo B):** Distribución Uniforme continua $\mathcal{U}(10, 20)$ con un peso de **$p_2 = 0.3$**.

### (b) Selección de la componente con $u_1 = 0.9$
Definimos las regiones de decisión mediante la acumulación de los pesos:
*   Región Tipo A (Componente 1): $[0.0, 0.7]$
*   Región Tipo B (Componente 2): $(0.7, 1.0]$

Evaluamos el número pseudoaleatorio $u_1 = 0.9$:
¿$u_1 \le 0.7$? **No ($0.9 > 0.7$)**.
*   **Decisión:** Al superar la frontera del primer peso acumulado, caemos en la segunda región. Se selecciona la **Componente 2** (Tipo B, Distribución $\mathcal{U}(10, 20)$).

### (c) Generación del valor de la componente elegida con $u_2 = 0.5$
Aplicamos la fórmula de asignación para la distribución uniforme continua general $x = a + (b - a)u_2$:
Sustituyendo los parámetros de la componente B ($a = 10, b = 20$) junto con el valor asignado $u_2 = 0.5$:
$$x = 10 + (20 - 10)(0.5)$$
$$x = 10 + 10(0.5)$$
$$x = 10 + 5$$
$$x = 15$$

*   **Resultado Final:** $x = 15$