# Repositorio de Simulación

Este repositorio contiene diversos recursos, prácticas y explicaciones relacionados con el estudio y la implementación de modelos de **Simulación de Sistemas**, cubriendo desde análisis matemáticos y métodos analíticos clásicos hasta técnicas avanzadas de simulación computacional en Python.

---

## Contenido del Repositorio

El contenido está estructurado en tres secciones principales:

### 1. Simulación de Eventos Discretos con la Librería SimPy

**SimPy** es un framework basado en procesos para la simulación de eventos discretos en Python. En esta sección se explica el funcionamiento de la librería y se proporcionan tres ejemplos prácticos listos para su ejecución:

- **[Introducción a la Librería SimPy](./SIMPY_INFO.md):** Explicación teórica sobre el funcionamiento del entorno (`Environment`), procesos (`Process`), recursos (`Resource`) y eventos de SimPy.
- **[Ejemplo 1: Banco Unicajero (Modelo de Cola M/M/1)](./SIMPY_EJEMPLO_1.md):** Simulación de un cajero automático simple atendiendo un flujo exponencial de clientes.
- **[Ejemplo 2: Estación de Servicio (Modelo de Cola M/M/c)](./SIMPY_EJEMPLO_2.md):** Simulación de una gasolinera con 3 surtidores paralelos que comparten una fila de autos.
- **[Ejemplo 3: Taller de Manufactura con Retrabajo](./SIMPY_EJEMPLO_3.md):** Simulación de un proceso secuencial en dos etapas (Ensamblado e Inspección) con una probabilidad del 15% de retrabajo para piezas defectuosas.

### 2. Métodos de Montecarlo

Modelos aplicados a la toma de decisiones bajo condiciones de incertidumbre y optimización de inventarios o producción. Puedes consultar el detalle en su respectivo archivo de documentación:
- **[Simulaciones de Montecarlo](./README_Montecarlo.md):** Contiene la teoría del método de Montecarlo, el caso práctico de la Panadería "El Retorno" (Optimización de producción con distribución de Poisson/empírica) y el caso práctico de control de inventarios de revisión continua (Política $Q, R$).

### 3. Explicaciones de Prácticas Académicas (Modelos Matemáticos Analíticos)

Reportes detallados con resoluciones de ejercicios matemáticos utilizando métodos analíticos y probabilísticos:
- **[Método de Composición (Práctica #4)](./Explicacion_Simulacion_U3_P4.md):** Generación de observaciones mediante composición para distribuciones hiperexponenciales, tramos constantes y mezclas de uniformes.
- **[Método de la Transformada Inversa (Práctica #5)](./Explicacion_Simulacion_U3_P5.md):** Aplicación analítica de la transformada inversa para distribuciones uniformes generales, exponenciales continuas y distribuciones discretas (dado cargado).

---

## Requisitos y Configuración

Los ejemplos de SimPy y Montecarlo están escritos en Python 3. Para ejecutar los códigos de simulación, instala las librerías necesarias con el siguiente comando:

```bash
pip install simpy numpy pandas matplotlib seaborn
```

Cada documento incluye instrucciones detalladas y autónomas para ejecutar los códigos de simulación correspondientes.
