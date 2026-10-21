"""
SISTEMA DE RECARGA Y VALIDACIÓN RÁPIDA DE ALMUERZOS UNIVERSITARIOS
"""

from collections import deque


# ESTRUCTURA 1: PILA (Stack) - Historial individual por Estudiante

class PilaTransacciones:
    def __init__(self):
        self._elementos = []

    def apilar(self, transaccion):
        self._elementos.append(transaccion)

    def desapilar(self):
        if not self.esta_vacia():
            return self._elementos.pop()
        return None

    def ver_ultimo(self):
        if not self.esta_vacia():
            return self._elementos[-1]
        return None

    def esta_vacia(self):
        return len(self._elementos) == 0

    def obtener_historial(self):
        return list(reversed(self._elementos))


# ESTRUCTURA 2: COLA (Queue) - Registro de Atenciones en Caja

class ColaRegistrosCaja:
    def __init__(self):
        self._cola = deque()

    def encolar_atencion(self, registro):
        """Registra la validación de un almuerzo en orden FIFO."""
        self._cola.append(registro)

    def obtener_atenciones(self):
        return list(self._cola)

    def total_atendidos(self):
        return len(self._cola)


# MODELO DE DATOS Y ARREGLO DINÁMICO

class Estudiante:
    def __init__(self, documento, nombre, almuerzos_disponibles=0):
        self.documento = documento
        self.nombre = nombre
        self.almuerzos_disponibles = almuerzos_disponibles
        self.historial = PilaTransacciones()


class SistemaComedor:
    def __init__(self):
        # ESTRUCTURA 3: Arreglo Dinámico (Lista en Python) para guardar estudiantes
        self.estudiantes = [] 
        self.registros_caja = ColaRegistrosCaja()

    def buscar_estudiante(self, documento):
        for est in self.estudiantes:
            if est.documento == documento:
                return est
        return None

    def registrar_estudiante(self, documento, nombre, almuerzos_iniciales=0):
        if self.buscar_estudiante(documento):
            return False, "El estudiante ya se encuentra registrado."
        nuevo_est = Estudiante(documento, nombre, almuerzos_iniciales)
        self.estudiantes.append(nuevo_est) # Arreglo dinámico
        if almuerzos_iniciales > 0:
            nuevo_est.historial.apilar(f"Recarga inicial: +{almuerzos_iniciales} almuerzos")
        return True, "Estudiante registrado con éxito."

    def recargar_almuerzos(self, documento, cantidad):
        est = self.buscar_estudiante(documento)
        if not est:
            return False, "Estudiante no encontrado."
        if cantidad <= 0:
            return False, "La cantidad a recargar debe ser mayor a 0."
        
        est.almuerzos_disponibles += cantidad
        est.historial.apilar(f"Recarga realizada: +{cantidad} almuerzos (Saldo actual: {est.almuerzos_disponibles})")
        return True, f"Recarga exitosa. Almuerzos disponibles: {est.almuerzos_disponibles}"

    def validar_paso_cajera(self, documento):
        """Proceso rápido para la cajera: digita documento y valida saldo."""
        est = self.buscar_estudiante(documento)
        if not est:
            return False, " Estudiante NO encontrado en el sistema."
        
        if est.almuerzos_disponibles > 0:
            est.almuerzos_disponibles -= 1
            est.historial.apilar(f"Consumo de almuerzo (Saldo restante: {est.almuerzos_disponibles})")
            
            # Registrar en la Cola de la Caja (FIFO)
            registro = f"Estudiante: {est.nombre} (Doc: {est.documento}) - PASO AUTORIZADO"
            self.registros_caja.encolar_atencion(registro)
            
            return True, f" PASO AUTORIZADO | Estudiante: {est.nombre} | Almuerzos restantes: {est.almuerzos_disponibles}"
        else:
            return False, f" SALDO INSUFICIENTE | Estudiante: {est.nombre} | Almuerzos disponibles: 0. Debe recargar."

    def deshacer_ultima_recarga(self, documento):
        est = self.buscar_estudiante(documento)
        if not est:
            return False, "Estudiante no encontrado."
        
        ultima = est.historial.ver_ultimo()
        if ultima and "Recarga" in ultima:
            est.historial.desapilar() # Uso de la Pila
            partes = ultima.split("+")
            cant = int(partes[1].split()[0])
            est.almuerzos_disponibles -= cant
            return True, f"Última recarga anulada. Saldo actualizado: {est.almuerzos_disponibles} almuerzos."
        return False, "No hay recargas recientes para anular."

# INTERFAZ DE USUARIO 

def menu_principal():
    sistema = SistemaComedor()
    # Datos de prueba para agilizar la revisión
    sistema.registrar_estudiante("1001", "Ana Gómez", 3)
    sistema.registrar_estudiante("1002", "Carlos Pérez", 0)

    while True:
        print("\n" + "="*55)
        print("   SISTEMA DE RECARGA Y VALIDACIÓN RÁPIDA DE ALMUERZOS")
        print("="*55)
        print("--- MÓDULO ESTUDIANTE ---")
        print("1. Consultar Almuerzos Disponibles e Historial")
        print("2. Recargar Almuerzos")
        print("\n--- MÓDULO CAJERA ---")
        print("3. Validar Ingreso por Documento ")
        print("\n--- MÓDULO ADMINISTRACIÓN ---")
        print("4. Registrar Nuevo Estudiante")
        print("5. Anular Última Recarga")
        print("6. Ver Reporte de Atenciones del Turno")
        print("7. Salir")
        print("="*55)
        
        opcion = input("Seleccione una opción (1-7): ").strip()

        if opcion == "1":
            doc = input("\nIngrese su número de documento: ").strip()
            est = sistema.buscar_estudiante(doc)
            if est:
                print(f"\n ESTUDIANTE: {est.nombre}")
                print(f" ALMUERZOS DISPONIBLES: {est.almuerzos_disponibles}")
                if est.almuerzos_disponibles == 0:
                    print(" ALERTA: No tiene almuerzos disponibles. Por favor recargue antes de hacer la fila.")
                
                print("\n Historial Reciente:")
                hist = est.historial.obtener_historial()
                if hist:
                    for item in hist:
                        print(f"   • {item}")
                else:
                    print("   • Sin movimientos registrados.")
            else:
                print("\n[!] El documento no está registrado.")

        elif opcion == "2":
            doc = input("\nIngrese su número de documento: ").strip()
            try:
                cant = int(input("Ingrese el número de almuerzos a recargar (ej. 3, 5, 10): "))
                exito, msg = sistema.recargar_almuerzos(doc, cant)
                print(f"\n[Resultado]: {msg}")
            except ValueError:
                print("\n[!] Error: Ingrese un número entero válido.")

        elif opcion == "3":
            print("\n [MODO CAJERA] Digite el documento del estudiante en la fila:")
            doc = input("Documento: ").strip()
            exito, msg = sistema.validar_paso_cajera(doc)
            print(f"\n>>> {msg}")

        elif opcion == "4":
            doc = input("\nIngrese el documento del nuevo estudiante: ").strip()
            nom = input("Ingrese el nombre completo: ").strip()
            try:
                cant = int(input("Almuerzos iniciales (0 si no recarga aún): "))
                exito, msg = sistema.registrar_estudiante(doc, nom, cant)
                print(f"\n[Resultado]: {msg}")
            except ValueError:
                print("\n[!] Error: Cantidad no válida.")

        elif opcion == "5":
            doc = input("\nIngrese el documento del estudiante: ").strip()
            exito, msg = sistema.deshacer_ultima_recarga(doc)
            print(f"\n[Resultado]: {msg}")

        elif opcion == "6":
            print("\n REPORTE DE PASOS ATENDIDOS EN CAJA:")
            atenciones = sistema.registros_caja.obtener_atenciones()
            if atenciones:
                for idx, elem in enumerate(atenciones, 1):
                    print(f"  {idx}. {elem}")
                print(f"\nTotal almuerzos servidos en el turno: {sistema.registros_caja.total_atendidos()}")
            else:
                print("  No se han registrado pasadas de estudiantes aún.")

        elif opcion == "7":
            print("\n¡Gracias por utilizar el Sistema de Validación Rápida de Almuerzos!")
            break
        else:
            print("\n[!] Opción inválida. Intente de nuevo.")

if __name__ == "__main__":
    menu_principal()