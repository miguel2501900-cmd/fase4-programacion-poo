# Fase 4 - Componente Práctico: Prácticas Simuladas (Programación Orientada a Objetos)

Sistema de gestión desarrollado en Python bajo el patrón Modelo-Vista-Controlador (MVC), utilizando `tkinter` para la interfaz gráfica y un sistema de persistencia en memoria y manejo avanzado de excepciones con registro automático en archivos de log (`sistema_logs.txt`).

## Estructura del Proyecto
- **`main.py`**: Archivo principal que inicializa la interfaz gráfica en pestañas (`ttk.Notebook`).
- **`entidades.py`**: Clase abstracta `Entidad`, de la que heredan `Cliente` y `Servicio`.
- **`clientes.py`**: Módulo de gestión y validación de clientes mediante propiedades (`@property`).
- **`Servicios.py`**: Clase abstracta `Servicio` y sus tres servicios especializados (Salas, Equipos y Asesorías). Cada uno sobrescribe el cálculo de costos, la descripción y la validación de parámetros; `calcular_costo_total` admite impuesto y descuento opcionales.
- **`reserva.py`**: Lógica de negocio para procesar, confirmar y cambiar estados de reservas.
- **`excepciones.py`**: Jerarquía de excepciones personalizadas y escritura automática de errores y eventos en `sistema_logs.txt`.
- **`simulacion.py`**: Simulación de 16 operaciones completas, válidas e inválidas, que demuestra que el sistema sigue funcionando ante errores.

## Requisitos de Ejecución
No requiere bases de datos externas ni librerías de terceros. Solo tener instalado Python 3.

## Cómo Ejecutar
Solo necesitas abrir tu terminal o consola en la carpeta del proyecto y correr el programa con:

```bash
python main.py
```

Para correr la simulación de operaciones sin abrir la interfaz:

```bash
python simulacion.py
```

También se puede lanzar desde la pestaña **Auditoría y Logs** de la interfaz.

## Autores (Grupo 92)
* Enrique Elías Ortiz Cobo
* José Manuel Escorcia Charris
* Miguel Antonio Castro Camacho
* Wilinton Ascanio Toro
