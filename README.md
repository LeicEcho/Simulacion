# Práctica 6: Batería Completa de Pruebas Estadísticas de Independencia y Uniformidad
**Autor:** Luis Alberto Castro Zúñiga

---

## 1. Introducción Teórica

En el ámbito de la simulación matemática, la generación de números pseudoaleatorios es fundamental para modelar sistemas estocásticos. Para que una secuencia de números pseudoaleatorios $\{U_i\}$ en el intervalo $[0, 1)$ sea estadísticamente válida, debe cumplir rigurosamente con dos propiedades fundamentales:

1. **Uniformidad**: Los números generados deben estar distribuidos de manera uniforme a lo largo del intervalo $(0, 1)$. Esto implica que cualquier subintervalo de igual longitud tiene la misma probabilidad de contener un número de la secuencia. Matemáticamente, la función de densidad de probabilidad de la variable aleatoria $U$ debe ser:
   $$f(u) = \begin{cases} 1 & \text{si } 0 \le u \le 1 \\ 0 & \text{en otro caso} \end{cases}$$

2. **Independencia**: No debe existir correlación, patrón o dependencia entre los números sucesivos de la secuencia. La ocurrencia de un valor no debe influir ni permitir predecir el valor del siguiente número generado. Matemáticamente, para cualquier par de variables aleatorias $U_i$ y $U_j$ (con $i \neq j$):
   $$P(U_i \le u_i, U_j \le u_j) = P(U_i \le u_i) \cdot P(U_j \le u_j)$$

Para validar que nuestro generador cumple con estas propiedades, se implementa una batería completa de pruebas estadísticas divididas en dos categorías principales:
* **Pruebas de Uniformidad**: Prueba de los Promedios y Prueba de Frecuencias.
* **Pruebas de Independencia**: Prueba de Póquer y Prueba de las Corridas Arriba/Abajo.
