# 📘 Documentación de Taller MS Persitence

Encargado de la gestión y almacenamiento de usuarios, licitaciones y trazabilidad de procesos del sistema.


Este proyecto incluye un MS desarrollado con Django para gestionar:

- Clientes y sus intereses asociados.
- Licitaciones (tenders).

---

## 📌 Tabla resumen de endpoints

| Recurso    | Método | Endpoint               | Descripción                                       |
|------------|--------|------------------------|---------------------------------------------------|
| Clientes   | GET    | `/clients/`       | Obtener listado de clientes con sus intereses     |
| Clientes   | POST   | `/clients/create/`     | Crear un cliente y asociar intereses              |
| Clientes   | GET    | `/clients/interests/`  | Obtener listado de todos los intereses            |
| Licitaciones | GET  | `/tenders/`       | Obtener listado de licitaciones                   |

> ⚠️ La creación de licitaciones se realiza mediante Redis, publicando un mensaje en el canal `messages`.


## 🧑‍💼 Clientes (`/clients/`)

### `GET /clients/`

Obtiene una lista de todos los clientes registrados junto con sus intereses.

- **Método:** `GET`
- **Respuesta exitosa:** `200 OK`

#### Ejemplo de respuesta:

```json
[
  {
    "name": "Juan Pérez",
    "email": "juan@example.com",
    "interests": ["Python", "Django"]
  }
]
```

### `POST /clients/create/`

Crea un nuevo cliente junto con sus intereses.

- **Método:** `POST`
- **Content-Type:** `application/json`

Cuerpo requerido:

```json
{
  "name": "Ana Torres",
  "email": "ana@example.com",
  "interests": ["IA", "Ciencia de Datos"]
}
```

- Validaciones:

1- Todos los campos son obligatorios.

2- Los intereses serán creados si no existen.

- **Respuestas:** `201 Created: Cliente creado correctamente.`

```json

{
  "message": "Cliente creado correctamente",
  "client_id": 5
}
```
`400 Bad Request: Faltan campos obligatorios o formato inválido.`

`500 Internal Server Error: Otro error inesperado.`

### `GET /clients/interests/`
Obtiene la lista completa de intereses existentes en el sistema.

- **Método:** `GET`

- **Respuesta exitosa:** `200 OK`

Ejemplo de respuesta:
```json
[
  {
    "id": 1,
    "name": "Construcción"
  },
  {
    "id": 2,
    "name": "Tecnología"
  }
]
```

## 📦 Licitaciones (/tenders/)
### GET /tenders/
Obtiene una lista de todas las licitaciones registradas.

-**Método:** `GET`

-** Respuesta exitosa:** `200 OK`

#### Ejemplo de respuesta:
```json
[
  {
    "id": 1,
    "code": "LIC001",
    "title": "Compra de equipos",
    "description": "Licitación para la adquisición de equipos computacionales"
  }
]
```

### Create Tenders

Crea una nueva licitación.

- **Cuerpo requerido:**

```json
{
  "code": "LIC123",
  "title": "Servicio de Mantenimiento",
  "description": "Contratación de servicios de mantenimiento preventivo"
}
```
-  **Validaciones:** 

1- Todos los campos son obligatorios.

2- El code debe ser único.

- **Respuestas:** 

`201 Created: Licitación creada correctamente.`

```json
{
  "message": "Licitación creada correctamente",
  "tender_id": 10
}
```
`400 Bad Request:` Faltan campos obligatorios o formato JSON inválido.

`409 Conflict:` Ya existe una licitación con el mismo código.

`500 Internal Server Error:` Otro error inesperado.

## 🧪 Pruebas unitarias
Puedes ejecutar las pruebas unitarias con el siguiente comando:

`python manage.py test`

Incluye pruebas para:

- Creación y validación de clientes con intereses.
- Manejo de campos requeridos y errores en /clients/create/.
- Creación y validación de licitaciones.
- Prevención de duplicados en códigos de licitación.
- Manejo de JSON inválido y métodos no permitidos.

## ⚙️ Requisitos del sistema
- Python 3.11
- Django 5.2.x
- psycopg 3.2.x
- redis[hiredis] 6.2.x
- PostgreSQL
- Docker y Docker Compose (opcional para entorno de desarrollo)

