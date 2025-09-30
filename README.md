## Greystone FastAPI Boilerplate

A structured FastAPI boilerplate using SQLAlchemy, organized routers, and a simple service layer for a loan amortization API.

### Quickstart

1. Create and activate a virtual environment
```bash
python3 -m venv .venv && source .venv/bin/activate
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Run the app
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`. Interactive docs: `http://localhost:8000/docs`.

### Docker

This project is containerized with separate containers for the API and the database.

- Build and run:
```bash
docker compose up --build
```

- API: `http://localhost:8000`
- Postgres: exposed on `localhost:5432` (db/user/pass: greystone)

The app uses `DATABASE_URL` from the container environment and connects to the `db` service automatically.

### Migrations (Alembic)

- Configure DB url:
  - Locally (SQLite default): nothing to do.
  - With Postgres (e.g., Docker or local): set `DATABASE_URL`, e.g.
```bash
export DATABASE_URL=postgresql+psycopg://greystone:greystone@localhost:5432/greystone
```

- Create a new empty revision:
```bash
make migrate-new NAME="add_users_table"
```

- Autogenerate a revision from models:
```bash
make migrate-autogen NAME="init_models"
```

- Apply migrations:
```bash
make migrate-upgrade            # to head
make migrate-upgrade TARGET=+1  # or to a specific target
```

- Rollback:
```bash
make migrate-downgrade          # one step
make migrate-downgrade TARGET=base
```

- Inspect:
```bash
make migrate-history
make migrate-current
```

Alembic files live under `alembic/`. Models are discovered via `app.db.base:Base.metadata`.

### Configuration

- `DATABASE_URL` environment variable is supported. Defaults to a local SQLite file: `sqlite:///./data/app.db` when running outside Docker.
- In Docker, `docker-compose.yml` sets:
  - `DATABASE_URL=postgresql+psycopg://greystone:greystone@db:5432/greystone`
- To change credentials, edit `docker-compose.yml` in both services accordingly.

### Project Layout

```
app/
  api/
    v1/
      routers/
        users.py
        loans.py
  core/
    config.py
  db/
    base.py
    session.py
  models/
    user.py
    loan.py
  schemas/
    user.py
    loan.py
  services/
    base.py
    users.py
    loans.py
alembic/
  env.py
  versions/
```

### Endpoints (v1)

- Users: `/api/v1/users`
  - POST `/` create user
  - GET `/` list users
  - GET `/{user_id}` get user
  - PUT `/{user_id}` update user
  - DELETE `/{user_id}` delete user

- Loans: `/api/v1/loans`
  - POST `/` create loan
  - GET `/` list loans
  - GET `/{loan_id}` get loan
  - PUT `/{loan_id}` update loan
  - DELETE `/{loan_id}` delete loan
  - GET `/{loan_id}/amortization` amortization schedule for existing loan
  - POST `/amortization` amortization schedule from request body

### Adding New Models

- Create a SQLAlchemy model in `app/models/` and import it in `app/db/base.py`.
- Create matching Pydantic schemas in `app/schemas/`.
- Add a service in `app/services/` (optional, recommended for complex logic).
- Expose endpoints via a router in `app/api/v1/routers/`.

### Notes

- For demo/dev, tables are auto-created on startup. Use Alembic for production migrations.
- Passwords are hashed using `passlib[bcrypt]`.
