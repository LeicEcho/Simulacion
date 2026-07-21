# Simulaciones de Montecarlo: Fundamentos y Casos Prácticos en Python

Este repositorio contiene una **trilogía de cuadernos interactivos (Jupyter Notebooks)** dedicados al estudio, implementación y aplicación práctica del **Método de Montecarlo**. A través de estos archivos, se abordan desde los pilares teóricos y matemáticos del método hasta su aplicación directa en la optimización de decisiones comerciales y logísticas bajo condiciones de incertidumbre.

---

## Contenido de la Trilogía

### 1. `Metodo Montecarlo.ipynb` (Fundamentos y Teoría)
Este cuaderno interactivo proporciona una revisión teórica y matemática rigurosa del Método de Montecarlo, detallando sus bases probabilísticas y su flujo de trabajo estándar en la industria.
* **Orígenes Históricos:** Introducción al nacimiento del método en la década de 1940 (Proyecto Manhattan) por Stanislaw Ulam, John von Neumann y Nicholas Metropolis.
* **Fundamentos Matemáticos:** Explicación detallada de la **Ley de los Grandes Números (LGN)** y el **Teorema del Límite Central (TLC)** que garantizan la convergencia del método.
* **Integración por Montecarlo:** Estimación numérica de integrales complejas y análisis de su tasa de convergencia ($\mathcal{O}(N^{-1/2})$), ideal para evitar la "maldición de la dimensionalidad".
* **Generación de Números Pseudoaleatorios (PRNG):** Implementación de algoritmos como el Generador Congruencial Lineal (LCG), el método de la **Transformada Inversa** (para distribución exponencial) y la transformación de **Box-Muller** (para distribución normal estándar).
* **Aplicaciones Industriales:** Resumen del uso del método en Finanzas (valoración de opciones, VaR), Logística (teoría de colas), Ciencias (blindaje nuclear) y Gestión de Proyectos (estimaciones de tiempo/costo).

### 2. `Metodo Montecarlo - Caso A - Panaderia.ipynb` (Optimización de Producción)
Una simulación práctica enfocada en resolver un problema clásico de optimización de producción diaria en el sector de alimentos (la panadería artesanal *"El Retorno"*).
* **El Problema:** Decidir cuántas piezas de pan fresco ($B$) hornear cada mañana para maximizar el beneficio neto diario.
* **Variables Financieras:**
  * Costo de producción: **$1.20 USD** por pieza.
  * Precio de venta fresco: **$3.00 USD** por pieza.
  * Precio de liquidación ("pan frío"): **$0.50 USD** por pieza.
  * Costo de escasez (venta perdida e insatisfacción): **$0.80 USD** por pieza faltante.
* **Modelado de Incertidumbre:**
  * La llegada de clientes diarios sigue una distribución de **Poisson** ($\lambda = 80$ clientes/día).
  * La cantidad demandada por cada cliente sigue una **distribución empírica** (de 1 a 4 panes con diferentes probabilidades).
* **Resultados de la Simulación (5,000 días):**
  * Demanda diaria promedio: **160.02 panes**.
  * **Cantidad óptima a hornear ($B^*$): 176 panes diarios**.
  * Beneficio diario esperado (promedio): **$268.63 USD**.

### 3. `Metodo Montecarlo - Caso B - Inventario.ipynb` (Optimización de Política $Q, R$)
Un simulador dinámico que optimiza una política de control de inventarios de revisión continua $(Q, R)$ en una comercializadora de tecnología.
* **El Problema:** Encontrar la combinación óptima de **Punto de Reorden ($R$)** y **Cantidad de Pedido ($Q$)** que minimice el costo promedio anual de operación del almacén.
* **Estructura de Costos:**
  * Costo fijo por emitir un pedido ($C_o$): **$100.00 USD**.
  * Costo diario de almacenamiento ($C_h$): **$0.20 USD** por unidad en stock al final del día.
  * Costo de escasez / venta perdida ($C_s$): **$5.00 USD** por unidad no entregada.
* **Modelado de Incertidumbre:**
  * Demanda diaria de productos: Distribución de **Poisson** ($\lambda = 15$ unidades/día).
  * Tiempo de entrega del proveedor (*Lead Time*): Variable aleatoria discreta (1, 2 o 3 días con probabilidades de 20%, 50% y 30% respectivamente).
* **Simulación y Optimización (500 réplicas anuales):**
  * Se evalúa una cuadrícula (*Grid Search*) de múltiples combinaciones de $Q$ y $R$.
  * **Punto de Reorden óptimo ($R^*$): 30 unidades**.
  * **Cantidad de Pedido óptima ($Q^*$): 130 unidades**.
  * Costo anual promedio mínimo obtenido: **$9,418.32 USD**.

---

## Tecnologías Utilizadas

* **Lenguaje:** Python 3
* **Entorno:** Jupyter Notebooks
* **Bibliotecas Clave:**
  * `NumPy`: Generación de variables aleatorias y cálculos matemáticos vectorizados.
  * `Pandas`: Estructuración y análisis de datos de simulación.
  * `Matplotlib` y `Seaborn`: Visualización gráfica de las curvas de demanda, distribuciones y optimización (mapas de calor de costos y ganancias).
