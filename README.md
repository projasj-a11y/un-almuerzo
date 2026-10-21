# .UN-Almuerzo: Sistema de Validación Rápida y Recarga de Almuerzos

Paula Vcitoria Rojas Jerez


## Problema Real
En los comedores universitarios de la Universidad Nacional de Colombia, el servicio de almuerzo enfrenta congestiones prolongadas durante el turno de 4 horas. El principal cuello de botella que ralentiza la fila es el tiempo dedicado a la transacción de cobro individual en caja (efectivo, tarjetas o transferencias).

UN-Almuerzo elimina el pago directo en el punto de entrega mediante un sistema de recarga previa de tiquetes/almuerzos numéricos. Cuando el estudiante llega a la fila, la cajera únicamente digita su documento de identidad, logrando una validación de paso en menos de 60 segundos.


## Estructuras Usadas

A continuación se detalla por qué y cómo se utilizó cada una de las 3 estructuras de datos lineales implementadas en el proyecto:

### 1. Arreglo Dinámico (`list` en Python)
* Por qué se usó: Se requiere una estructura de datos contigua en memoria de tamaño flexible que permita almacenar el registro global de estudiantes y escalar automáticamente a medida que se inscriben nuevos usuarios sin reorganizar la memoria manualmente.
* Cómo se usó: Se utiliza en la clase `SistemaComedor` para mantener la lista `self.estudiantes`. Permite iterar y buscar eficientemente a los estudiantes mediante su número de documento al momento de consultar saldo, efectuar recargas o validar su ingreso en caja.

### 2. Pila (`Stack` - LIFO)
* Por qué se usó: Sigue el principio Last In, First Out (Último en Entrar, Primero en Salir). Es la estructura ideal para modelar historiales de transacciones individuales, permitiendo acceder inmediatamente al movimiento más reciente y deshacer operaciones erróneas.
* Cómo se usó: Se implementó a través de la clase `PilaTransacciones` asociada a cada `Estudiante`. Cada recarga o consumo de almuerzo se apila (`apilar()`). Si el administrador o cajera comete un error al recargar, la función `desapilar()` anula la última operación y restaura el saldo previo.

### 3. Cola (`Queue` - FIFO)
* Por qué se usó: Sigue la filosofía First In, First Out (Primero en Entrar, Primero en Salir). Garantiza que las atenciones procesadas en caja se registren en un orden cronológico estricto para fines de auditoría del turno.
* Cómo se usó: Se implementó con la clase `ColaRegistrosCaja` (utilizando `collections.deque`). Cada vez que la cajera aprueba el paso de un estudiante, la validación se encola (`encolar_atencion()`), permitiendo al módulo de administración consultar la secuencia cronológica de almuerzos entregados.

## Manual de usuario
Requisitos Previos:
- Tener instalado Python 3.8 o superior.
- Libreria streamlit (pip install streamlit).

Instrucciones de Ejecucion:
1. Abrir la terminal en la carpeta del proyecto.
2. Ejecutar: streamlit run app_web.py

Guia de Uso por Modulo:

1. Modulo Estudiante:
   - Ingrese su numero de documento (ej. 1001 o 1002).
   - Presione Consultar para verificar su saldo y revisar su historial (Pila LIFO).
   - Ingrese la cantidad de almuerzos a recargar y confirme la operacion.

2. Modulo Cajera (Punto de Control):
   - Ingrese el documento del estudiante en la fila.
   - Presione VALIDAR PASO. En menos de 2 segundos el sistema autorizara
     el ingreso descontando 1 almuerzo o indicara saldo insuficiente.

3. Modulo Administracion:
   - Registrar Estudiante: Permite inscribir un usuario en el Arreglo Dinamico.
   - Anular Recarga: Utiliza desapilar() en la Pila para revertir un error.
   - Reporte de Atenciones: Muestra la secuencia cronologica (Cola FIFO)
     de almuerzos entregados en el turno.


## Declaración del uso de la IA

1. Desarrollo y Logica por personal (50%):
   - Concepción y planteamiento de la problemática real del comedor en la Universidad Nacional de Colombia (UNAL), desarrollo y alimentación del código lógico inicial (versión en consola), identificación y corrección de inconsistencias en la lógica de negocio, prueba mecánica de las estructuras de datos (Arreglo, Pila y Cola) y adaptación del diseño del software para el flujo real de la cajera y el estudiante.

2. Asistencia por Herramientas de IA (Gemini) (50%):
   -Estructuración sintáctica de la librería streamlit, soporte técnico para resolver errores de dependencias de entorno (pip/ensurepip), optimización de componentes visuales de la interfaz gráfica y maquetación de la documentación en formato Markdown.
