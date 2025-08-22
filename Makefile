run:
    uvicorn src.main:app --reload

migrate:
    alembic upgrade head