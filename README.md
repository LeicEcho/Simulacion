Práctica 4: Generación de Números Pseudoaleatorios 
Este proyecto contiene la implementación de un generador de números pseudoaleatorios utilizando el **Método Congruencial Mixto**. El objetivo principal de la práctica es configurar el algoritmo matemático para garantizar un **periodo completo** de al menos 4096 números únicos antes de que ocurra la primera repetición.
Contenido del Repositorio
`Practica4.py`: Script principal en Python que solicita los parámetros, ejecuta el algoritmo modular, valida que el periodo sea completo y muestra los resultados en bloques justificados.
`Explicacion_Practica4.ipynb`: Jupyter Notebook que contiene el desglose matemático, pruebas adicionales y la justificación teórica del comportamiento del generador.

---

Fundamento Matemático
El método congruencial mixto se rige por la siguiente ecuación recursiva:
X_{i} = (aX_{i-1} + b) \pmod M

Para lograr que el generador alcance su periodo máximo (periodo completo), es decir, que genere todos los números posibles en el espacio del módulo $M$ antes de repetir el primero, debe cumplir estrictamente con el Teorema de Hull-Dobell:

1.  **Coprimatilidad:** El incremento b y el módulo M deben ser primos relativos (su único divisor común debe ser 1).
2.  **Divisibilidad de a-1:** Para cada factor primo p de M, (a - 1) debe ser divisible por $p$.
3.  **Divisibilidad por 4:** Si M es divisible por 4, entonces (a - 1) también debe ser divisible por 4.

Parámetros Óptimos Configurados

Para garantizar un periodo exacto de **4096** números pseudoaleatorios (M = 2^{12}), se seleccionaron las siguientes constantes que cumplen perfectamente con el teorema:

| Parámetro | Valor | Justificación Matemática |
| :--- | :--- | :--- |
| **Módulo ($M$)** | `4096` | Define el tamaño total del espacio modular (2^{12}). |
| **Multiplicador ($a$)** | `21` | Cumple la regla: (a - 1) = 20, el cual es perfectamente divisible entre 4. |
| **Incremento ($b$)** | `11` | Es un número impar, lo que garantiza que no comparte factores primos con 4096 (primos relativos). |
| **Semilla ($X_0$)** | *Cualquiera* | Gracias a que se cumple el teorema, el periodo completo se alcanza sin importar la semilla de arranque. |
