# .UN-Almuerzo: Sistema de Validación Rápida y Recarga de Almuerzos.

**Paula Victoria Rojas Jerez**


## Justificación del Problema Real
En los comedores universitarios de la Universidad Nacional de Colombia, el servicio de almuerzo enfrenta congestiones prolongadas durante el turno de 4 horas. El principal cuello de botella que ralentiza la fila es el tiempo dedicado a la transacción de cobro individual en caja (efectivo, tarjetas o transferencias).

**UN-Almuerzo** elimina el pago directo en el punto de entrega mediante un sistema de **recarga previa de tiquetes/almuerzos numéricos**. Cuando el estudiante llega a la fila, la cajera únicamente digita su documento de identidad, logrando una validación de paso en menos de 60 segundos.


## Justificación de Estructuras de Datos Lineales

### 1. Arreglo Dinámico (`list` en Python)
* **Uso:** Almacena la base de datos central en memoria con los registros de los estudiantes matriculados.
* **Justificación:** Proporciona una estructura contigua en memoria que escala según la matrícula de estudiantes y permite la búsqueda eficiente por número de documento al consultar saldo, recargar o validar en caja.

### 2. Pila (`Stack` - LIFO)
* **Uso:** Gestiona el historial individual de operaciones (recargas y consumos) de cada estudiante.
* **Justificación:** Sigue el principio *Last In, First Out* (Último en Entrar, Primero en Salir). Permite consultar primero los movimientos más recientes y habilita la función de **anular/deshacer** la última recarga en caso de error al digitar.

### 3. Cola (`Queue` - FIFO)
* **Uso:** Guarda el registro secuencial de atenciones en la caja durante el turno de almuerzo.
* **Justificación:** Mantiene un orden estrictamente cronológico (*First In, First Out*) de las autorizaciones concedidas por la cajera para auditoría al final del servicio.


## Declaración del Porcentaje de Uso de Inteligencia Artificial (Gemini)

* **Desarrollo y Lógica por parte del Estudiante (50%):** 
  * Concepción de la problemática real en los comedores de la Universidad Nacional de Colombia.
  * Desarrollo del código base inicial y lógica del negocio.
  * Corrección de errores lógicos y ajuste del flujo funcional (Módulo Estudiante y Módulo Cajera).
  * Pruebas de funcionamiento y validación mecánica de las estructuras de datos lineales.

* **Asistencia por Herramientas de IA (50%):** 
  * Asistencia para la integración de la librería gráfica `streamlit`.
  * Resolución de errores de entorno de ejecución en consola.
  * Formateo de documentación (`README.md`).


## Manual de Usuario

### Requisitos
* Tener instalado **Python 3.8** o superior.
* Librería `streamlit`.

### Instrucciones de Ejecución
1. Clonar o descargar este repositorio:
   ```bash
   git clone [https://github.com/TU_USUARIO/un-almuerzo.git](https://github.com/TU_USUARIO/un-almuerzo.git)
   cd un-almuerzo
