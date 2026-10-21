# UN-Almuerzo | Sistema de Validación Rápida y Recarga de Almuerzos

Paula Victoria Rojas Jerez

## Problema Real

En los comedores universitarios de la Universidad Nacional de Colombia, el servicio de almuerzo enfrenta congestiones prolongadas durante el turno de 4 horas. El principal cuello de botella que ralentiza la fila es el tiempo dedicado a la transacción de cobro individual en caja (efectivo, tarjetas o transferencias).

UN-Almuerzo elimina el pago directo en el punto de entrega mediante un sistema de recarga previa de tiquetes/almuerzos numéricos. Cuando el estudiante llega a la fila, la cajera únicamente digita su documento de identidad, logrando una validación de paso en menos de 60 segundos.

## Estructuras de Datos 

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

## Documentación y Código 

La arquitectura del sistema está dividida en las siguientes clases clave en el código fuente (`app_web.py` / `sistema_almuerzos.py`):

```python
# 1. PILA (Stack) - Manejo de historial LIFO por estudiante
class PilaTransacciones:
    def __init__(self):
        self._elementos = []  # Lista base para la pila

    def apilar(self, transaccion):
        self._elementos.append(transaccion)

    def desapilar(self):
        return self._elementos.pop() if not self.esta_vacia() else None

    def ver_ultimo(self):
        return self._elementos[-1] if not self.esta_vacia() else None

# 2. COLA (Queue) - Registro FIFO de atenciones en caja
class ColaRegistrosCaja:
    def __init__(self):
        self._cola = deque()  # Cola doblemente enlazada

    def encolar_atencion(self, registro):
        self._cola.append(registro)

# 3. ARREGLO DINÁMICO Y MODELO DE DATOS
class Estudiante:
    def __init__(self, documento, nombre, almuerzos_disponibles=0):
        self.documento = documento
        self.nombre = nombre
        self.almuerzos_disponibles = almuerzos_disponibles
        self.historial = PilaTransacciones()  # Pila individual

class SistemaComedor:
    def __init__(self):
        self.estudiantes = []  # Arreglo Dinámico central
        self.registros_caja = ColaRegistrosCaja()  # Cola central