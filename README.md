# Sistema de Inventario FA

Sistema de gestión de inventario desarrollado en Django para el control de activos tecnológicos.

## Características

- Gestión completa de activos tecnológicos
- Control de ubicaciones y movimientos
- Sistema de responsivas con imágenes
- Escaneo de red para detectar dispositivos
- API REST para integración con otros sistemas
- Panel de administración completo
- Exportación e importación de datos en Excel

## Requisitos

- Python 3.8+
- PostgreSQL
- Virtualenv (recomendado)

## Instalación

1. **Clonar el repositorio**
```bash
git clone <url-del-repositorio>
cd inventarySistemFA
```

2. **Crear entorno virtual**
```bash
python3 -m venv venv
source venv/bin/activate  # En Linux/Mac
# o
venv\Scripts\activate  # En Windows
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**
```bash
cp env_example .env
# Editar .env con tus configuraciones
```

5. **Configurar base de datos PostgreSQL**
```sql
CREATE DATABASE inventary;
CREATE USER fa01 WITH PASSWORD 'admin';
GRANT ALL PRIVILEGES ON DATABASE inventary TO fa01;
```

6. **Ejecutar migraciones**
```bash
python manage.py migrate
```

7. **Crear superusuario**
```bash
python manage.py createsuperuser
```

8. **Ejecutar el servidor**
```bash
python manage.py runserver
```

## Configuración de Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

```env
# Django Settings
SECRET_KEY=tu-clave-secreta-segura
DEBUG=True

# Database Settings
DB_NAME=inventary
DB_USER=fa01
DB_PASSWORD=admin
DB_HOST=localhost
DB_PORT=5432

# Email Settings
EMAIL_HOST=tu-servidor-smtp.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-contraseña-de-aplicación

# CSRF Settings
CSRF_TRUSTED_ORIGINS=https://tu-dominio.com,http://localhost:3000
```

## Uso

1. **Acceder al sistema**: http://localhost:8000
2. **Panel de administración**: http://localhost:8000/admin
3. **API REST**: http://localhost:8000/api/

## Estructura del Proyecto

```
inventarySistemFA/
├── FA01/                    # Aplicación principal
│   ├── models.py           # Modelos de datos
│   ├── views.py            # Vistas y lógica de negocio
│   ├── urls.py             # Configuración de URLs
│   ├── admin.py            # Configuración del admin
│   └── templates/          # Plantillas HTML
├── inventario/             # Configuración del proyecto
│   ├── settings.py         # Configuración de Django
│   └── urls.py             # URLs principales
├── static/                 # Archivos estáticos
├── media/                  # Archivos subidos por usuarios
└── requirements.txt        # Dependencias de Python
```

## Modelos Principales

- **Asset**: Activos tecnológicos
- **Location**: Ubicaciones físicas
- **Movement**: Movimientos de activos
- **Responsibility**: Responsivas de activos
- **AssetImage**: Imágenes de activos
- **UserProfile**: Perfiles de usuario extendidos

## API REST

El sistema incluye endpoints REST para:

- Registro de dispositivos de sucursales
- Consulta de dispositivos por sucursal
- Gestión de activos

## Seguridad

- Todas las credenciales sensibles están en variables de entorno
- Validación de archivos subidos
- Autenticación requerida para todas las vistas
- Protección CSRF habilitada

## Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles. 