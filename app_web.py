"""
========================================================================
UN-Almuerzo: Sistema de Validación Rápida y Recarga de Almuerzos UNAL
========================================================================
Estructuras de Datos Lineales Utilizadas:
1. Arreglo Dinámico: Base de Datos global de Estudiantes registrados.
2. Pila (Stack): Historial individual de Transacciones (LIFO) con opción de anular última recarga.
3. Cola (Queue): Registro secuencial de atenciones en caja (FIFO) durante el turno.
"""

import streamlit as st
from collections import deque

# ----------------------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA E IDENTIDAD
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="UN-Almuerzo - Universidad Nacional de Colombia",
    page_icon="🍲",
    layout="wide"
)

# ----------------------------------------------------------------------
# ESTRUCTURA 1: PILA (Stack) - Historial individual por Estudiante
# ----------------------------------------------------------------------
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


# ----------------------------------------------------------------------
# ESTRUCTURA 2: COLA (Queue) - Registro de Atenciones en Caja
# ----------------------------------------------------------------------
class ColaRegistrosCaja:
    def __init__(self):
        self._cola = deque()

    def encolar_atencion(self, registro):
        self._cola.append(registro)

    def obtener_atenciones(self):
        return list(self._cola)

    def total_atendidos(self):
        return len(self._cola)


# ----------------------------------------------------------------------
# MODELO DE DATOS Y ARREGLO DINÁMICO
# ----------------------------------------------------------------------
class Estudiante:
    def __init__(self, documento, nombre, almuerzos_disponibles=0):
        self.documento = documento
        self.nombre = nombre
        self.almuerzos_disponibles = almuerzos_disponibles
        self.historial = PilaTransacciones()


class SistemaComedor:
    def __init__(self):
        # ESTRUCTURA 3: Arreglo Dinámico (Lista en Python)
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
        self.estudiantes.append(nuevo_est)
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
        est = self.buscar_estudiante(documento)
        if not est:
            return False, "Estudiante NO registrado en el sistema.", None
        
        if est.almuerzos_disponibles > 0:
            est.almuerzos_disponibles -= 1
            est.historial.apilar(f"Consumo de almuerzo (Saldo restante: {est.almuerzos_disponibles})")
            
            registro = f"Estudiante: {est.nombre} (Doc: {est.documento}) - PASO AUTORIZADO"
            self.registros_caja.encolar_atencion(registro)
            
            return True, f"PASO AUTORIZADO | Estudiante: {est.nombre} | Almuerzos restantes: {est.almuerzos_disponibles}", est
        else:
            return False, f"SALDO INSUFICIENTE | Estudiante: {est.nombre} | Almuerzos disponibles: 0.", est

    def deshacer_ultima_recarga(self, documento):
        est = self.buscar_estudiante(documento)
        if not est:
            return False, "Estudiante no encontrado."
        
        ultima = est.historial.ver_ultimo()
        if ultima and "Recarga" in ultima:
            est.historial.desapilar()
            partes = ultima.split("+")
            cant = int(partes[1].split()[0])
            est.almuerzos_disponibles -= cant
            return True, f"Última recarga anulada. Saldo actualizado: {est.almuerzos_disponibles} almuerzos."
        return False, "No hay recargas recientes para anular."


# ----------------------------------------------------------------------
# GESTIÓN DEL ESTADO GLOBAL DE LA APLICACIÓN WEB
# ----------------------------------------------------------------------
if 'sistema' not in st.session_state:
    st.session_state.sistema = SistemaComedor()
    # Datos de prueba predeterminados (UNAL)
    st.session_state.sistema.registrar_estudiante("1001", "Ana Gómez", 3)
    st.session_state.sistema.registrar_estudiante("1002", "Carlos Pérez", 0)

sistema = st.session_state.sistema

# ----------------------------------------------------------------------
# INTERFAZ GRÁFICA WEB
# ----------------------------------------------------------------------
st.title("🍲 UN-Almuerzo")
st.caption("Sistema de Validación Rápida y Recarga de Almuerzos - Universidad Nacional de Colombia")
st.write("---")

# Menú lateral para cambiar de pestaña
opcion_menu = st.sidebar.radio(
    "Seleccione el Módulo:",
    ["👤 Módulo Estudiante", "💳 Módulo Cajera", "⚙️ Módulo Administración"]
)

# ----------------------------------------------------------------------
# PESTAÑA 1: MÓDULO ESTUDIANTE
# ----------------------------------------------------------------------
if opcion_menu == "👤 Módulo Estudiante":
    st.header("👤 Panel de Consulta y Recarga de Estudiantes")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Consulta de Saldo")
        doc_consulta = st.text_input("Ingrese su número de documento:", key="doc_est")
        if st.button("Consultar"):
            est = sistema.buscar_estudiante(doc_consulta)
            if est:
                st.session_state.est_actual = est
            else:
                st.error("Estudiante no encontrado. Verifique el número de documento.")
                st.session_state.est_actual = None

    if 'est_actual' in st.session_state and st.session_state.est_actual:
        est = st.session_state.est_actual
        with col2:
            st.success(f"**Estudiante:** {est.nombre}")
            st.metric("Almuerzos Disponibles", f"{est.almuerzos_disponibles} 🍲")
            
            if est.almuerzos_disponibles == 0:
                st.warning("⚠️ Sin almuerzos disponibles. Recargue antes de dirigirse a la fila.")
            
            st.write("---")
            st.subheader("Recargar Almuerzos")
            cant_recarga = st.number_input("Cantidad de almuerzos a comprar:", min_value=1, max_value=50, value=5)
            if st.button("Confirmar Recarga"):
                exito, msg = sistema.recargar_almuerzos(est.documento, cant_recarga)
                st.success(msg)
                st.rerun()

            st.write("---")
            st.subheader("📜 Historial de Movimientos ")
            historial = est.historial.obtener_historial()
            if historial:
                for item in historial:
                    st.info(f"• {item}")
            else:
                st.write("Sin movimientos registrados.")

# ----------------------------------------------------------------------
# PESTAÑA 2: MÓDULO CAJERA (PASO RÁPIDO)
# ----------------------------------------------------------------------
elif opcion_menu == "💳 Módulo Cajera":
    st.header("💳 Punto de Validación Rápida en Caja")
    st.write("Digite el documento del estudiante que se encuentra al frente de la fila:")
    
    doc_caja = st.text_input("Número de Documento del Estudiante:", key="doc_caja")
    
    if st.button("✅ VALIDAR PASO", type="primary"):
        if doc_caja:
            exito, msg, est = sistema.validar_paso_cajera(doc_caja)
            if exito:
                st.success(f"### {msg}")
                st.balloons()
            else:
                st.error(f"### {msg}")
        else:
            st.warning("Por favor ingrese un número de documento.")

# ----------------------------------------------------------------------
# PESTAÑA 3: MÓDULO ADMINISTRACIÓN
# ----------------------------------------------------------------------
elif opcion_menu == "⚙️ Módulo Administración":
    st.header("⚙️ Panel Administrativo")
    
    tab1, tab2, tab3 = st.tabs(["Registrar Estudiante", "Anular Recarga", "Reporte de Atenciones"])
    
    with tab1:
        st.subheader("Registrar Nuevo Estudiante")
        new_doc = st.text_input("Documento:")
        new_nom = st.text_input("Nombre Completo:")
        new_cant = st.number_input("Almuerzos Iniciales:", min_value=0, value=0)
        if st.button("Registrar en Sistema"):
            if new_doc and new_nom:
                exito, msg = sistema.registrar_estudiante(new_doc, new_nom, new_cant)
                if exito:
                    st.success(msg)
                else:
                    st.error(msg)
            else:
                st.warning("Complete todos los campos.")

    with tab2:
        st.subheader("Anular Última Recarga")
        doc_anular = st.text_input("Documento del Estudiante a Anular:")
        if st.button("Anular Última Operación"):
            exito, msg = sistema.deshacer_ultima_recarga(doc_anular)
            if exito:
                st.warning(msg)
            else:
                st.error(msg)

    with tab3:
        st.subheader("📊 Reporte de Pasos en Caja")
        atenciones = sistema.registros_caja.obtener_atenciones()
        st.write(f"**Total de almuerzos servidos en el turno:** {sistema.registros_caja.total_atendidos()}")
        if atenciones:
            for i, atencion in enumerate(atenciones, 1):
                st.text(f"{i}. {atencion}")
        else:
            st.write("No se han registrado pasos en caja durante este turno.")