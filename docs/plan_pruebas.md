# Plan de Pruebas - Sistema de Gestión Deportiva Academia Tuzos

**Desarrollado por:** Equipo 4 - Integradora UTD  
**Universidad:** Universidad Tecnológica de Durango  
**Fecha:** Diciembre 2024

## 1. Introducción

### 1.1 Propósito
Este documento describe el plan de pruebas para el Sistema de Gestión Deportiva de la Academia Tuzos, con el objetivo de garantizar la calidad, funcionalidad y confiabilidad del sistema.

### 1.2 Alcance
Las pruebas cubrirán:
- Funcionalidad CRUD completa
- Autenticación y autorización
- Validación de datos
- Exportación de información
- Interfaz de usuario

## 2. Estrategia de Pruebas

### 2.1 Niveles de Prueba

#### Pruebas Unitarias
- **Objetivo:** Verificar el funcionamiento individual de funciones y métodos
- **Herramientas:** pytest
- **Cobertura esperada:** 80%

#### Pruebas de Integración
- **Objetivo:** Verificar la interacción entre componentes
- **Áreas clave:**
  - Conexión con base de datos
  - Flujo entre vistas
  - Validación de datos

#### Pruebas de Sistema
- **Objetivo:** Verificar el sistema completo
- **Escenarios:**
  - Flujos de usuario end-to-end
  - Casos de uso principales

#### Pruebas de Aceptación
- **Objetivo:** Validar requisitos del usuario
- **Método:** Pruebas manuales con usuarios finales

## 3. Casos de Prueba

### 3.1 Autenticación

#### TC-AUTH-001: Login Exitoso
- **Precondición:** Usuario existe en BD
- **Pasos:**
  1. Abrir aplicación
  2. Ingresar usuario: "admin"
  3. Ingresar contraseña: "admin123"
  4. Click en "Aceptar"
- **Resultado esperado:** Acceso al menú principal
- **Prioridad:** Alta

#### TC-AUTH-002: Login Fallido
- **Precondición:** Aplicación abierta
- **Pasos:**
  1. Ingresar usuario: "admin"
  2. Ingresar contraseña incorrecta
  3. Click en "Aceptar"
- **Resultado esperado:** Mensaje de error
- **Prioridad:** Alta

### 3.2 Gestión de Jugadores

#### TC-JUG-001: Registrar Jugador
- **Precondición:** Usuario autenticado
- **Pasos:**
  1. Ir a Registrar → Jugadores
  2. Llenar formulario con datos válidos
  3. Click en "Registrar"
- **Resultado esperado:** Jugador creado exitosamente
- **Prioridad:** Alta

#### TC-JUG-002: Consultar Jugadores
- **Precondición:** Existen jugadores en BD
- **Pasos:**
  1. Ir a Consultar → Jugadores
  2. Observar tabla
- **Resultado esperado:** Lista de jugadores mostrada
- **Prioridad:** Media

#### TC-JUG-003: Modificar Jugador
- **Precondición:** Jugador existe
- **Pasos:**
  1. Ir a Modificar → Jugadores
  2. Seleccionar jugador
  3. Modificar datos
  4. Click en "Actualizar"
- **Resultado esperado:** Datos actualizados
- **Prioridad:** Alta

#### TC-JUG-004: Eliminar Jugador
- **Precondición:** Jugador existe
- **Pasos:**
  1. Ir a Eliminar → Jugadores
  2. Seleccionar jugador
  3. Confirmar eliminación
- **Resultado esperado:** Jugador eliminado
- **Prioridad:** Alta

### 3.3 Validación de Datos

#### TC-VAL-001: CURP Único
- **Precondición:** Jugador con CURP existe
- **Pasos:**
  1. Intentar registrar jugador con mismo CURP
- **Resultado esperado:** Error de duplicado
- **Prioridad:** Alta

#### TC-VAL-002: Campos Obligatorios
- **Precondición:** Formulario de registro abierto
- **Pasos:**
  1. Dejar campos vacíos
  2. Intentar registrar
- **Resultado esperado:** Mensaje de error
- **Prioridad:** Media

### 3.4 Exportación de Datos

#### TC-EXP-001: Exportar a CSV
- **Precondición:** Datos en tabla
- **Pasos:**
  1. Ir a Consultar
  2. Click en "Exportar"
  3. Seleccionar CSV
- **Resultado esperado:** Archivo CSV generado
- **Prioridad:** Baja

#### TC-EXP-002: Exportar a Excel
- **Precondición:** Datos en tabla, pandas instalado
- **Pasos:**
  1. Ir a Consultar
  2. Click en "Exportar"
  3. Seleccionar Excel
- **Resultado esperado:** Archivo XLSX generado
- **Prioridad:** Baja

## 4. Criterios de Aceptación

### 4.1 Criterios de Entrada
- Código completo y compilable
- Base de datos configurada
- Dependencias instaladas

### 4.2 Criterios de Salida
- 100% de casos de prueba críticos pasados
- 90% de casos de prueba de alta prioridad pasados
- 80% de cobertura de código
- Cero defectos críticos abiertos

### 4.3 Criterios de Suspensión
- Más de 5 defectos críticos
- Imposibilidad de conectar a BD
- Fallo en autenticación

## 5. Recursos

### 5.1 Recursos Humanos
- 1 Tester QA
- 1 Desarrollador (soporte)

### 5.2 Recursos Técnicos
- Computadora con Windows
- Python 3.8+
- MySQL Server
- Herramientas de prueba (pytest)

### 5.3 Ambiente de Pruebas
- **Sistema Operativo:** Windows 10/11
- **Base de Datos:** MySQL 8.0
- **Python:** 3.8+

## 6. Cronograma

| Fase | Duración | Responsable |
|------|----------|-------------|
| Pruebas Unitarias | 2 días | Desarrollador |
| Pruebas de Integración | 2 días | QA |
| Pruebas de Sistema | 3 días | QA |
| Pruebas de Aceptación | 2 días | Usuario + QA |
| **Total** | **9 días** | |

## 7. Riesgos

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|--------------|---------|------------|
| BD no disponible | Media | Alto | Tener backup de BD |
| Dependencias faltantes | Baja | Medio | Documentar requirements |
| Datos de prueba insuficientes | Media | Medio | Crear script de datos |

## 8. Entregables

- Casos de prueba documentados
- Reporte de ejecución de pruebas
- Reporte de defectos
- Métricas de cobertura
- Recomendaciones de mejora

## 9. Aprobaciones

| Rol | Nombre | Firma | Fecha |
|-----|--------|-------|-------|
| Líder de Proyecto | | | |
| QA Lead | | | |
| Desarrollador | | | |
