# Sistema de Gestión Deportiva - Academia Tuzos

Sistema completo de gestión para academias deportivas desarrollado en Python con Tkinter y MySQL.

## 📋 Descripción

Sistema CRUD completo para la gestión de:
- Jugadores
- Torneos
- Partidos
- Horarios
- Categorías
- Entrenamientos
- Profesores
- Usuarios

## 🚀 Instalación

### Requisitos Previos
- Python 3.8 o superior
- MySQL Server (XAMPP recomendado)
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Descargar el proyecto**
```bash
# Descarga el proyecto completo
cd PROYECTO_INTEGRADOR_TUZOS
```

2. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

3. **Configurar la base de datos**
   - Iniciar MySQL (XAMPP)
   - Importar el archivo `database/academia_tuzos.sql` en phpMyAdmin
   - Crear archivo `.env` basado en `.env.example`

4. **Configurar variables de entorno**
```bash
cp .env.example .env
# Editar .env con tus credenciales de base de datos
```

## ▶️ Uso

### Ejecutar la aplicación
```bash
python Main.py
```

### Credenciales por defecto
- **Usuario:** admin
- **Contraseña:** admin123

## 📁 Estructura del Proyecto

```
PROYECTO_INTEGRADOR_TUZOS/
├── src/
│   ├── controllers/      # Lógica de negocio
│   ├── models/          # Modelos de datos
│   ├── views/           # Interfaces gráficas
│   ├── components/      # Componentes UI reutilizables
│   └── core/            # Núcleo de la aplicación
├── tests/               # Pruebas unitarias
├── database/            # Scripts SQL
├── assets/              # Recursos estáticos
│   └── imagenes/        # Imágenes del sistema
├── docs/                # Documentación
├── Main.py              # Punto de entrada
└── requirements.txt     # Dependencias
```

## 🛠️ Tecnologías Utilizadas

- **Python 3.x**
- **Tkinter** - Interfaz gráfica
- **MySQL** - Base de datos
- **mysql-connector-python** - Conector de BD
- **Pillow** - Procesamiento de imágenes
- **tkcalendar** - Selectores de fecha
- **pywinstyles** - Estilos de ventana

## 📊 Funcionalidades

### CRUD Completo
- ✅ **Registrar** - Agregar nuevos registros
- ✅ **Consultar** - Visualizar y buscar datos
- ✅ **Modificar** - Editar registros existentes
- ✅ **Eliminar** - Borrar registros con confirmación

### Características Adicionales
- 🔐 Sistema de autenticación
- 📤 Exportación a CSV, Excel y PDF
- 🔍 Búsqueda en tiempo real
- 📋 Validación de datos
- 🎨 Interfaz gráfica moderna

## 🧪 Pruebas

```bash
# Ejecutar pruebas
python -m pytest tests/

# Con cobertura
python -m pytest --cov=src tests/
```

## 📝 Licencia

Este proyecto es de código abierto y está disponible bajo la Licencia MIT.

## 👥 Autores

**Equipo 4 - Integradora UTD**

Proyecto desarrollado por el Equipo 4 como parte del curso Integradora de la Universidad Tecnológica de Durango (UTD).

- Sistema de Gestión Deportiva - Academia Tuzos
- Desarrollo completo del sistema CRUD con Python, Tkinter y MySQL

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📞 Soporte

Para soporte, por favor abre un issue en el repositorio.

---

**Nota:** Este es un proyecto educativo desarrollado por el Equipo 4 - Integradora UTD para la gestión de academias deportivas.

© 2025 Equipo 4 - Universidad Tecnológica de Durango
