# Crime Statistics API

This is a backend application developed with FastAPI to manage crime statistics in Argentina. The application uses SQLAlchemy as an ORM to interact with a PostgreSQL database, Alembic for managing migrations, and a simple frontend based on HTMX.

---

## Requirements

- **Python 3.11** (o superior)
- **PostgreSQL** (make sure it is installed and running)
- **Git** (to clone the repository)

---

## Installation

### 1. Clone the repository

```bash
git clonehttps://github.com/mmedela/Criministica.git
cd Criministica
```
### 2. Create and activate a virtual environment
#### Linux/Mac:

```bash
python3 -m venv venv
source venv/bin/activate
```
#### Windows (CMD):

```cmd
python -m venv venv
venv\Scripts\activate
```

#### Windows (PowerShell):

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

Update pip and then install the dependencies from the requirements.txt file:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Database Configuration

## 1. Install PostgreSQL

- linux: Linux: Use your distribution’s package manager. For example, on Ubuntu:

```bash
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
```
- Windows: Download and install PostgreSQL from https://www.postgresql.org/download/windows/

## 2. Configure the Database

Make sure to create a database and tables needed for the aplication for the application. For example, using psql:

```sql
CREATE DATABASE crimes_db;
CREATE USER postgres WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE crimes_db TO postgres;

CREATE TABLE provinces (
    province_id INTEGER PRIMARY KEY,
    province_name VARCHAR,
    population INTEGER
);

CREATE TABLE crimes (
    crime_code_snic_id INTEGER PRIMARY KEY,
    crime_code_snic_name VARCHAR
);

CREATE TABLE crime_statistics (
    id INTEGER PRIMARY KEY,
    province_id INTEGER REFERENCES provinces(province_id),
    crime_code_snic_id INTEGER REFERENCES crimes(crime_code_snic_id),
    year INTEGER,
    act_quantity INTEGER,
    victim_quantity INTEGER,
    male_victims_quantity INTEGER,
    female_victims_quantity INTEGER,
    victim_quantity_sd INTEGER,
    act_rate NUMERIC,
    victim_rate NUMERIC,
    male_victims_rate NUMERIC,
    female_victims_rate NUMERIC,
    CONSTRAINT uq_statistics UNIQUE (province_id, crime_code_snic_id, year)
);
```

In the application's configuration file `(e.g., DB/config.py)`, make sure the connection string is set up, for example:


```python
DATABASE_URL = "postgresql://postgres:password@localhost/crimes_db"
```

## 2. Migrations

### 1. Initialize Alembic (if you haven’t done it yet)
If this is your first time, initialize Alembic:

```bash
alembic init migrations
```

### 2. Generate a migration
To generate a new migration based on changes in your models, run:
```bash
alembic revision --autogenerate -m "Descripción de los cambios"
```

### 3. Run migrations
To apply the migrations to the database, use:
```bash
alembic upgrade head
```

### ⚠️ Note on Migrations
Following the database translation process, existing Alembic migrations have become obsolete and are no longer in active use. However, their implementation and evolution can still be reviewed in the project's commit history, should you need to reference or understand past changes.

### 4. Populate DB
To populate the database, run the `populate_db` script. Before doing so, ensure that the `CSV_ROUTE` variable in the application's configuration file `(e.g., DB/config.py)` points to a valid CSV file containing the necessary data. A properly formatted CSV file has already been provided.

```bash
python DB\populate_db.py
```

Additionally, to demonstrate specific system features, a separate CSV file is available to populate the population data for provinces. You can upload this file by navigating to the `/provinces/upload_population`
 route. 

## Running the application


### 1. Run in development
You can run the application with Uvicorn:
```bash
uvicorn criministica.main:app --reload
```
Note: If your project's root directory is not named criministica, make sure to reference it correctly.


## Frontend
The application includes a simple frontend based on HTMX which is served through Jinja2 templates.

- The main page is located in templates/index.html.

- There are also pages for loading partial content, such as statistics, in templates/partial_statistics.html.

## Diagrams (Mermaid)

Here are some diagrams to better understand the application's architecture, flow and how to integrate it with other services.

## 🗂️ Database Schema Diagram (Mermaid)

The following ER diagram shows the relationship between provinces, crimes, and crime statistics stored in the system.

### ER Diagram: Crime Statistics Schema

```mermaid
erDiagram
    PROVINCE {
        INT province_id PK
        STRING province_name
        INT population
    }

    CRIME {
        INT crime_code_snic_id PK
        STRING crime_code_snic_name
    }

    CRIME_STATISTICS {
        INT id PK
        INT province_id FK
        INT crime_code_snic_id FK
        INT year
        INT act_quantity
        INT victim_quantity
        INT male_victims_quantity
        INT female_victims_quantity
        INT victim_quantity_sd
        FLOAT act_rate
        FLOAT victim_rate
        FLOAT male_victims_rate
        FLOAT female_victims_rate
    }

    PROVINCE ||--o{ CRIME_STATISTICS : has
    CRIME ||--o{ CRIME_STATISTICS : registers
```

## 📊 Flow Diagrams (Mermaid)

Below is a sequence diagram illustrating how the application handles a request for crime statistics by province.

### Sequence: Crime Statistics Request

```mermaid
sequenceDiagram
    participant Cliente
    participant API as FastAPI
    participant Sistema_Externo

    Cliente->>API: Solicita estadísticas de delitos por provincia
    API->>Sistema_Externo: Verifica datos adicionales (si aplica)
    Sistema_Externo-->>API: Responde con información complementaria
    API-->>Cliente: Retorna estadísticas en JSON
```