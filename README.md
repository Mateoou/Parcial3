
# Parcial - Corte 3

Este repositorio contiene los dos proyectos desarrollados para el parcial del Corte 3. El objetivo fue aplicar habilidades de programación y transformar ideas en soluciones funcionales, cumpliendo con los requisitos base y añadiendo características adicionales para mejorar cada proyecto. [cite: 3]

## Proyectos Desarrollados

Se entregan dos desarrollos: una Batalla Pokémon en C++ y un Sistema de Parqueadero en Python. [cite: 5]

### 1. Batalla Pokémon (C++)

Basado en el sistema de combate de los juegos Pokémon[cite: 9], este proyecto busca simular un enfrentamiento por turnos.

**Cumplimiento de Requisitos Mínimos:**
* **Lenguaje C++:** El proyecto está desarrollado en C++. [cite: 11]
* **Combate por Turnos:** Se implementó un sistema donde dos Pokémon, controlados por el usuario, se enfrentan y atacan alternadamente. [cite: 12]
* **Menú de Interacción Textual:** Se utiliza un menú basado en texto para la interacción del jugador. [cite: 13]
* **Sistema de Ataques (mínimo dos):** Cada Pokémon cuenta con cuatro ataques distintos. [cite: 14]
* **Sistema de Victoria:** El combate finaliza cuando un Pokémon se queda sin puntos de vida, y se anuncia al ganador. [cite: 14]

**Características Adicionales (Valor Agregado):**
* **Equipos de Múltiples Pokémon:** Cada jugador selecciona y gestiona un equipo de 3 Pokémon, con la posibilidad de cambiarlos durante la batalla.
* **Estadísticas Detalladas:** Los Pokémon poseen atributos como nombre, tipo, HP actual, HP máximo, ataque y defensa.
* **Cálculo de Daño Mejorado:** El daño de los ataques incluye una variación aleatoria y considera la defensa del Pokémon oponente.
* **Selección de Equipo:** Los jugadores eligen sus Pokémon de una lista predefinida al inicio.
* **Interfaz de Usuario Clara:** Se procuró una presentación ordenada de la información en consola.

### 2. Sistema de Parqueadero (Python)

Este proyecto tiene como objetivo desarrollar un sistema básico para la administración de un parqueadero. [cite: 17]

**Cumplimiento de Requisitos Mínimos:**
* **Lenguaje Python:** El proyecto está desarrollado en Python. [cite: 19]
* **Mapa Visual del Parqueadero (>7x7):** Se genera un mapa visual utilizando Tkinter que representa la distribución del parqueadero, excediendo las dimensiones mínimas. [cite: 20]
* **Vías, Entrada y Salida Accesibles:** El mapa incluye vías y los espacios son accesibles desde un punto de entrada simulado. [cite: 21]
* **Registro de Vehículos (Placa y Hora de Entrada):** Se registra la placa y la hora de ingreso de cada vehículo. [cite: 22]
* **Sistema de Cobro por Tiempo:** Se calcula el valor a pagar según el tiempo de permanencia del vehículo. [cite: 23]
* **Sistema de Disponibilidad (Visual y en Tiempo Real):** Se muestra la disponibilidad de espacios (ocupados/libres) y esto se refleja gráficamente en el mapa. [cite: 24, 25]

**Características Adicionales (Valor Agregado):**
* **Interfaz Gráfica de Usuario (GUI) con Tkinter:** Se desarrolló una interfaz gráfica completa para una mejor interacción y visualización.
* **Modo de Conducción Interactivo:** El usuario puede controlar el vehículo (WASD y Espacio) para estacionarlo en el mapa.
* **Múltiples Tipos de Vehículos:** Soporte para "carro", "deportivo" y "motocicleta", con tarifas y gestión de imágenes (con fallback) diferenciadas.
* **Sistema de Facturación Detallado:** Incluye opción de seguro adicional, descuento por larga estadía y una factura detallada al retirar el vehículo.
* **Gestión de Casilleros para Motocicletas.**
* **Persistencia de Datos:** El estado del parqueadero (vehículos, espacios, historial) se guarda y carga desde un archivo JSON, permitiendo continuar la simulación.
* **Historial de Salidas Completo:** Se mantiene un registro de salidas, visualizable en la aplicación y exportable a JSON.
* **Diseño Personalizado:** Se aplicó un esquema de colores para la interfaz.
* **Funcionalidades Adicionales en UI:** Reloj en tiempo real, información de vehículos al hacer clic sobre ellos (en modo vista general) y opción de reseteo completo del sistema.

Estos desarrollos adicionales buscan ofrecer una solución más completa y con mayor valor diferencial. [cite: 28, 29]

*(Agregar aquí nombre completo del integrante)*
