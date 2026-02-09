# VideoMind Backend

Hexagonal architecture based backend for Personal Video Search App.

## Architecture

```text
       +-----------------------------------------------------------+
       |                        API (FastAPI)                      |
       +-----------------------------------------------------------+
                                     |
       +-----------------------------------------------------------+
       |                       USE CASES                           |
       | (Ingest, Search, Detail, Transcribe)                      |
       +-----------------------------------------------------------+
               |                     |                     |
    +-------------------+   +-------------------+   +-------------------+
    |      DOMAIN       |   |      DOMAIN       |   |      DOMAIN       |
    |     ENTITIES      |---|      PORTS        |---|      LOGIC        |
    +-------------------+   +-------------------+   +-------------------+
               |                     |                     |
       +-----------------------------------------------------------+
       |                       ADAPTERS                            |
       | (DB, Telegram, AI, Queue, Storage)                        |
       +-----------------------------------------------------------+
```

## Project Status

- [x] **Task 1: Backend base + Domain + Database adapter** (Completed)
- [ ] **Task 2: Telegram Bot + Celery workers** (Pending)
- [ ] **Task 3: AI adapters (Whisper + Embeddings + Categorizer)** (Pending)
- [ ] **Task 4: API REST + Búsqueda + Import Instagram** (Pending)

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

## Verification

To run tests:
```bash
pytest
```

To check health:
```bash
curl http://localhost:8000/health
```
