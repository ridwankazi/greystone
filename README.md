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
- Postgres: exposed on `localhost:5432` (db: `greystone`, user: `greystone`, password: `greystone`)

The app uses `DATABASE_URL` from the container environment and connects to the `db` service automatically.

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
