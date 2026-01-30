# Administrador de Pedidos para Restaurante

Aplicación de escritorio desarrollada en **Python con Tkinter**, orientada a la gestión de mesas y pedidos en un restaurante.
El proyecto fue diseñado siguiendo el patrón **Modelo–Vista–Controlador (MVC)**, con persistencia en base de datos y comunicación por sockets.

---

## Descripción general

El sistema permite:
- Dar de alta y administrar mesas
- Registrar comensales
- Cargar y eliminar pedidos
- Calcular totales
- Consultar consumos por cliente

No incluye control de stock; el foco está puesto en la **gestión de pedidos y clientes**.

---

## Arquitectura

El proyecto implementa una arquitectura **MVC**:

### Controlador
**`controlador.py`**
- Orquesta la ejecución del programa
- Inicializa la vista y la conexión con el servidor
- Vincula observadores y eventos

### Modelo
**`modelo.py`**
- Contiene la lógica de negocio
- Administración de clientes y consumos
- Acceso a base de datos (SQLite)
- Validaciones con expresiones regulares
- Manejo de excepciones personalizadas
- Implementación del patrón **Observer**
- Comunicación con servidor vía **sockets + threading**

### Vista
**`vista.py`**
- Implementa la interfaz gráfica con Tkinter
- Manejo de widgets, TreeViews y eventos
- No contiene lógica de negocio

---

## Comunicación por Sockets

El sistema incluye un módulo de comunicación cliente-servidor que:
- Envía información de pedidos en tiempo real
- Utiliza hilos (`threading`) para evitar bloquear la interfaz gráfica

---

## Tecnologías utilizadas

- Python
- Tkinter
- SQLite
- Sockets
- Threading
- Programación Orientada a Objetos
- Patrón Observer
- MVC

---

## Objetivos del proyecto

Este proyecto fue desarrollado con fines de aprendizaje para:
- Aplicar arquitectura MVC en una aplicación real
- Integrar GUI con lógica y base de datos
- Practicar patrones de diseño
- Trabajar con concurrencia y comunicación en red

---

## Autor

**Dami Pica**  
Desarrollador en formación  
Python · Java · Kotlin · Bases de Datos
