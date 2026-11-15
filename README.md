# Fase 4 - Componente Práctico: Prácticas Simuladas (Programación Orientada a Objetos)

Sistema de gestión desarrollado en Python bajo el patrón Modelo-Vista-Controlador (MVC), utilizando `tkinter` para la interfaz gráfica y un sistema de persistencia en memoria y manejo avanzado de excepciones con registro automático en archivos de log (`sistema_logs.txt`).

## Estructura del Proyecto
- **`main.py`**: Archivo principal que inicializa la interfaz gráfica en pestañas (`ttk.Notebook`).
- **`clientes.py`**: Módulo de gestión y validación de clientes mediante propiedades (`@property`).
- **`Servicios.py`**: Catálogo de servicios (Salas, Equipos y Asesorías) con códigos automáticos.
- **`reserva.py`**: Lógica de negocio para procesar, confirmar y cambiar estados de reservas.
- **`excepciones.py`**: Jerarquía de excepciones personalizadas y escritura automática de trazas en `sistema_logs.txt`.

## Requisitos de Ejecución
No requiere bases de datos externas ni librerías de terceros. Solo tener instalado Python 3.

## Cómo Ejecutar
Solo necesitas abrir tu terminal o consola en la carpeta del proyecto y correr el programa con:

```bash
python main.py
```

## Autores (Grupo 92)
* Enrique Elías Ortiz Cobo
* José Manuel Escorcia Charris
* Miguel Antonio Castro Camacho
