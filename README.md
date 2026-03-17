# IP Segment Manager

Aplicación web full stack para gestión de segmentos IPv4 orientada a ISP, telecomunicaciones y equipos NOC. Incluye inventario, detección de superposición, validación operativa por ping y SNMP, auditoría, dashboard y autenticación por roles.

## Arquitectura recomendada

- Backend: FastAPI + SQLAlchemy + PostgreSQL.
- Frontend: React + Vite + TypeScript.
- Autenticación: JWT con roles `admin`, `operator`, `viewer`.
- Scheduler: APScheduler integrado en el backend para validaciones periódicas.
- Validación técnica:
  - Ping vía comando del sistema ejecutado por backend.
  - SNMP v2c vía `pysnmp`.
- Persistencia:
  - `segments` como entidad principal.
  - `validations` para historial técnico.
  - `audit_logs` para trazabilidad operativa.

## Modelo de datos

### Tablas principales

- `users`: usuarios, rol, estado y credenciales.
- `segments`: inventario de redes, CIDR, tipo, ubicación, VLAN, nodo, pool, equipo, estado y última validación.
- `validations`: historial de validaciones por IP.
- `pools`: agrupación lógica de segmentos.
- `locations`: ubicaciones o sitios.
- `nodes`: nodos asociados a ubicaciones.
- `audit_logs`: historial de cambios por segmento.

### Reglas clave

- Solo IPv4 en esta versión.
- El CIDR se valida al crear o editar.
- Se bloquea duplicidad exacta.
- Se bloquea superposición con otros segmentos.
- La IP principal de validación debe pertenecer al segmento.

## Estructura de carpetas

```text
.
|-- backend
|   |-- app
|   |   |-- api/v1
|   |   |-- core
|   |   |-- db
|   |   |-- jobs
|   |   |-- models
|   |   |-- schemas
|   |   |-- services
|   |   `-- utils
|   |-- scripts
|   `-- requirements.txt
|-- frontend
|   |-- src
|   |   |-- api
|   |   |-- components
|   |   |-- context
|   |   |-- pages
|   |   `-- types
|   `-- package.json
|-- .env.example
`-- README.md
```

## Endpoints principales

- `POST /api/v1/auth/login`
- `GET /api/v1/auth/me`
- `GET|POST|PUT|DELETE /api/v1/segments`
- `POST /api/v1/segments/{id}/validate`
- `GET /api/v1/segments/{id}/validations`
- `GET /api/v1/segments/dashboard`
- `GET /api/v1/segments/export/csv`
- `POST /api/v1/segments/import/csv`
- `GET|POST|PUT|DELETE /api/v1/pools`
- `GET|POST|PUT|DELETE /api/v1/locations`
- `GET|POST|PUT|DELETE /api/v1/nodes`

Swagger queda disponible en `http://localhost:8000/docs`.

## Instalación

### 1. Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Editar `backend/.env` y ajustar `DATABASE_URL` y `SECRET_KEY`.

### 2. Base de datos

Crear una base PostgreSQL llamada `ip_segments` y verificar que el usuario configurado tenga permisos.

### 3. Seed inicial

```bash
cd backend
set PYTHONPATH=.
python scripts/seed.py
```

Usuarios iniciales:

- `admin / admin123`
- `operador / operador123`
- `viewer / viewer123`

### 4. Ejecutar backend

```bash
cd backend
set PYTHONPATH=.
uvicorn app.main:app --reload
```

### 5. Frontend

```bash
cd frontend
npm install
copy .env.example .env
npm run dev
```

Frontend por defecto en `http://localhost:5173`.

## Funcionalidades incluidas en esta primera versión

- Login con JWT y roles.
- Dashboard con métricas principales.
- CRUD de segmentos, pools, ubicaciones y nodos.
- Búsqueda general de segmentos.
- Detección de duplicidad y superposición CIDR.
- Validación manual por ping y SNMP.
- Scheduler para validaciones periódicas.
- Historial técnico por segmento.
- Auditoría de cambios.
- Importación y exportación CSV.
- API documentada con OpenAPI/Swagger.

## Consideraciones operativas

- El ping y SNMP dependen de la conectividad real del servidor backend hacia los dispositivos o gateways.
- En Windows se usa `ping -n 1`; en Linux se usa `ping -c 1`.
- SNMP usa el OID `1.3.6.1.2.1.1.1.0` para una prueba básica de conectividad.
- Esta versión crea tablas con `Base.metadata.create_all()`. Para producción conviene migrar luego a Alembic.
- IPv6 queda preparado como evolución futura, pero no implementado aún.

## Mejoras sugeridas para la siguiente iteración

- Alembic para migraciones.
- Refresh token y expiración configurable por rol.
- Vista jerárquica por sitio/pool/nodo.
- Importador CSV con mapeo flexible de columnas.
- Soporte IPv6.
- Jobs distribuidos con Celery o RQ si el volumen crece.
