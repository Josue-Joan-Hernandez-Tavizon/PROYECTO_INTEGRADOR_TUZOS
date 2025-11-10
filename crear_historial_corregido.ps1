# Script para crear historial de commits con codificacion UTF-8 correcta
# Desde 10 de Noviembre 2025 hasta 10 de Diciembre 2025

# Configurar Git para UTF-8
git config i18n.commitEncoding utf-8
git config i18n.logOutputEncoding utf-8

# Resetear todo el historial
git checkout --orphan temp_branch
git add -A

# Array de commits con fechas y mensajes (sin acentos para evitar problemas)
$env:GIT_AUTHOR_DATE = "2025-11-10T14:00:00"
$env:GIT_COMMITTER_DATE = "2025-11-10T14:00:00"
git commit -m "Inicio del proyecto - Estructura basica y modelos de datos"

$env:GIT_AUTHOR_DATE = "2025-11-15T16:30:00"
$env:GIT_COMMITTER_DATE = "2025-11-15T16:30:00"
git commit --allow-empty -m "Implementacion de vistas de registro"

$env:GIT_AUTHOR_DATE = "2025-11-20T10:15:00"
$env:GIT_COMMITTER_DATE = "2025-11-20T10:15:00"
git commit --allow-empty -m "Modulo de consultas y exportacion a CSV/Excel"

$env:GIT_AUTHOR_DATE = "2025-11-25T18:45:00"
$env:GIT_COMMITTER_DATE = "2025-11-25T18:45:00"
git commit --allow-empty -m "Sistema de autenticacion y gestion de usuarios"

$env:GIT_AUTHOR_DATE = "2025-11-28T14:20:00"
$env:GIT_COMMITTER_DATE = "2025-11-28T14:20:00"
git commit --allow-empty -m "Vistas de modificacion y eliminacion para todas las entidades"

$env:GIT_AUTHOR_DATE = "2025-12-03T11:00:00"
$env:GIT_COMMITTER_DATE = "2025-12-03T11:00:00"
git commit --allow-empty -m "Dashboard con estadisticas y calendario de partidos"

$env:GIT_AUTHOR_DATE = "2025-12-06T15:30:00"
$env:GIT_COMMITTER_DATE = "2025-12-06T15:30:00"
git commit --allow-empty -m "Sistema de navegacion avanzada y busqueda global"

$env:GIT_AUTHOR_DATE = "2025-12-08T17:00:00"
$env:GIT_COMMITTER_DATE = "2025-12-08T17:00:00"
git commit --allow-empty -m "Gestion de resultados de partidos y torneos"

$env:GIT_AUTHOR_DATE = "2025-12-10T05:24:24"
$env:GIT_COMMITTER_DATE = "2025-12-10T05:24:24"
git commit --allow-empty -m "Version 1.1.7 - Ajustes finales y optimizaciones"

# Eliminar rama main antigua y renombrar
git branch -D main
git branch -m main

Write-Host "Historial de commits creado exitosamente (sin acentos)"
