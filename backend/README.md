# VideoMind Backend

Hexagonal architecture based backend for Personal Video Search App.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Start infrastructure:
   ```bash
   docker-compose up -d
   ```

3. Run migrations:
   ```bash
   alembic upgrade head
   ```

4. Run the app:
   ```bash
   uvicorn src.api.main:app --reload
   ```

## Structure

- `src/domain`: Core business logic and entities.
- `src/adapters`: Implementations of external services (DB, AI, etc.).
- `src/api`: FastAPI routes and application setup.
- `alembic`: Database migrations.
