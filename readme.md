# Crime Statistics API

Esta es una aplicación backend desarrollada con FastAPI para gestionar estadísticas de delitos en Argentina. La aplicación utiliza SQLAlchemy como ORM para interactuar con una base de datos PostgreSQL, Alembic para gestionar migraciones y un frontend sencillo basado en HTMX.

---

## Requisitos

- **Python 3.11** (o superior)
- **PostgreSQL** (asegúrate de tenerlo instalado y en ejecución)
- **Git** (para clonar el repositorio)
- Opcional: **Docker** y **docker-compose** para correr la aplicación en contenedores

---

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu_usuario/tu_repositorio.git
cd tu_repositorio
```
### 2. Crear y activar un ambiente virtual
#### En Linux/Mac:

```bash
python3 -m venv venv
source venv/bin/activate
```
#### En Windows (CMD):

```cmd
python -m venv venv
venv\Scripts\activate
```

#### En Windows (PowerShell):

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3.  Instalar las dependencias

Actualiza pip y luego instala las dependencias desde el archivo requirements.txt:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Configuración de la Base de Datos

## 1. Instalar PostgreSQL

- linux: Usa el gestor de paquetes de tu distribución. Por ejemplo, en Ubuntu:

```bash
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
```
- Windows: Descarga e instala PostgreSQL desde https://www.postgresql.org/download/windows/

## 2. Configurar la Base de Datos

Asegúrate de crear una base de datos para la aplicación. Por ejemplo, usando psql:

```sql
CREATE DATABASE delitos_db;
CREATE USER postgres WITH PASSWORD 'tu_contraseña';
GRANT ALL PRIVILEGES ON DATABASE delitos_db TO postgres;
```

En el archivo de configuración de la aplicación (DB/config.py o similar), asegúrate de que la cadena de conexión esté configurada, por ejemplo:


```python
DATABASE_URL = "postgresql://postgres:tu_contraseña@localhost/delitos_db"
```

## 2. Migraciones

### 1. Inicializar Alembic (si aún no lo has hecho)
Si es la primera vez, inicializa Alembic:

```bash
alembic init migrations
```

### 2. Generar una migración
Para generar una nueva migración basada en los cambios en tus modelos, ejecuta:
```bash
alembic revision --autogenerate -m "Descripción de los cambios"
```

### 3. Aplicar las migraciones
Para aplicar las migraciones a la base de datos, usa:
```bash
alembic upgrade head
```

## Ejecución de la aplicación


### 1. Ejecutar en desarrollo
Puedes correr la aplicación con Uvicorn:
```bash
uvicorn criministica.main:app --reload
```
Nota: Si el directorio raíz de tu proyecto no se llama criministica, asegúrate de referenciarlo correctamente.


## Frontend
La aplicación incluye un frontend sencillo basado en HTMX que se sirve a través de plantillas Jinja2.

- La página principal se encuentra en templates/index.html.

- También hay páginas para cargar contenido parcial, por ejemplo, para estadísticas, en templates/estadisticas_partial.html.