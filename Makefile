install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements_dev.txt

start:
	uvicorn app.main:app --reload

black: 
	black .

migrate:
	alembic upgrade head

makemigrations:
	alembic revision --autogenerate -m "'${m}'"