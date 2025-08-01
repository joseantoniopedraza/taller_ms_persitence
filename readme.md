# Taller MS Persistence

Microservicio Django para persistencia de datos de licitaciones.

## Docker

### Construir la imagen

```bash
docker build -t taller_ms_persistence .
```

### Ejecutar el contenedor

```bash
docker run --rm -p 8000:8000 \
  -e DB_HOST=postgres \
  -e DB_PORT=5432 \
  -e DB_NAME=persistence_db \
  -e DB_USER=persistence_user \
  -e DB_PASSWORD=A123456 \
  taller_ms_persistence
```

### Usar con Docker Compose

El servicio ya está configurado en el `docker-compose.yml` principal. Para ejecutarlo:

```bash
# Ejecutar solo el servicio de persistencia
docker-compose up taller_ms_persistence

# Ejecutar todo el stack
docker-compose up
```

## Variables de entorno

- `DB_NAME`: Nombre de la base de datos (por defecto: persistence_db)
- `DB_USER`: Usuario de la base de datos (por defecto: persistence_user)
- `DB_PASSWORD`: Contraseña de la base de datos (por defecto: A123456)
- `DB_HOST`: Host de la base de datos (por defecto: localhost)
- `DB_PORT`: Puerto de la base de datos (por defecto: 5432)

## Dependencias

- Python 3.11
- Django 5.2.4
- psycopg 3.2.9 (PostgreSQL adapter)
- PostgreSQL 15

## Acceso

- **Django Admin**: http://localhost:8000/admin/
- **API**: http://localhost:8000/

## Comandos útiles

```bash
# Crear superusuario
docker-compose exec taller_ms_persistence python manage.py createsuperuser

# Ejecutar migraciones manualmente
docker-compose exec taller_ms_persistence python manage.py migrate

# Crear migraciones
docker-compose exec taller_ms_persistence python manage.py makemigrations
```