# Introducción a la Librería SimPy

**SimPy** es un framework de simulación de eventos discretos (DES - *Discrete Event Simulation*) para Python basado en procesos. Es una herramienta poderosa, flexible y ligera, ampliamente utilizada en la industria y la academia para modelar sistemas complejos de colas, cadenas de suministro, logística y procesos industriales.

---

## 1. El Paradigma de Simulación de Eventos Discretos (DES)

En la simulación de eventos discretos, el estado del sistema cambia únicamente en puntos específicos del tiempo (llamados **eventos**), en contraste con las simulaciones continuas donde las variables cambian constantemente.

SimPy implementa esto utilizando **procesos** representados por funciones generadoras de Python (`yield`). Esto permite que los procesos se detengan y reanuden en puntos de tiempo definidos por el desarrollador, dando la sensación de que las actividades ocurren de manera concurrente en el tiempo de simulación.

---

## 2. Conceptos y Componentes Clave de SimPy

SimPy se estructura principalmente en torno a cuatro componentes fundamentales:

### A. El Entorno (`Environment`)
El entorno (`simpy.Environment`) es el núcleo de la simulación. Se encarga de:
- Mantener la línea de tiempo de la simulación.
- Programar y ejecutar los eventos en orden cronológico.
- Controlar la ejecución del programa mediante `env.run(until=...)`.

### B. Los Procesos (`Process`)
Los procesos representan el comportamiento dinámico de las entidades del sistema (por ejemplo, clientes, vehículos, piezas en una línea de montaje).
- Se definen mediante funciones generadoras que contienen la palabra clave `yield`.
- Un proceso se registra en el entorno con `env.process(mi_proceso(env))`.
- La instrucción `yield env.timeout(duracion)` suspende el proceso durante una cantidad dada de tiempo de simulación para modelar una actividad (como esperar en una fila o realizar un trabajo).

### C. Los Recursos (`Resource`)
Los recursos modelan los puntos de congestión o cuellos de botella del sistema. Son compartidos por múltiples procesos que compiten por ellos. SimPy ofrece varios tipos de recursos:

1. **`Resource` (Recursos Estándar):**
   Modelan servidores con capacidad limitada (p. ej., cajeros, ventanillas, rampas). Los procesos solicitan acceso con `with recurso.request() as peticion:` y liberan automáticamente el recurso al salir del bloque `with`.
   
2. **`PriorityResource` / `PreemptiveResource` (Recursos con Prioridad):**
   Permiten que procesos con mayor prioridad sean atendidos antes en la cola. Si es de tipo *preemptive*, un proceso prioritario puede interrumpir a uno de menor prioridad que esté siendo atendido.
   
3. **`Container` (Contenedores):**
   Modelan el almacenamiento de recursos homogéneos no diferenciados (p. ej., un tanque de agua, un silo de granos, combustible). Tienen límites de capacidad y admiten operaciones de producción (`put`) y consumo (`get`).
   
4. **`Store` (Almacenes):**
   Modelan inventarios o colas de objetos Python individuales y diferenciados (p. ej., piezas numeradas, paquetes con atributos específicos). Admiten transacciones tipo productor-consumidor.

### D. Eventos (`Events`)
Cualquier interacción entre un proceso y el entorno es un evento.
- El más común es `env.timeout(t)`, que genera un evento de espera temporal.
- Los procesos también pueden esperar a que otros procesos terminen o a que se cumplan condiciones lógicas utilizando operadores como `&` (AND) o `|` (OR) sobre múltiples eventos.

---

## 3. Ventajas de Utilizar SimPy

- **Python Estándar:** No requiere lenguajes propietarios de simulación. Se puede integrar directamente con librerías científicas como NumPy, Pandas, SciPy, Matplotlib y algoritmos de Machine Learning.
- **Ligero y Rápido:** Tiene una huella de memoria sumamente baja y su rendimiento de ejecución es excelente gracias al uso de generadores nativos de Python.
- **Claridad de Código:** Al modelar los procesos secuencialmente mediante generadores, el flujo lógico de las entidades es fácil de leer y mantener, evitando la complejidad del manejo de hilos tradicionales.
- **Fácil Extensibilidad:** Permite la construcción rápida de interfaces visuales, análisis estadístico avanzado y optimizaciones mediante bucles de búsqueda en Python.
