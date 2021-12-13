install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements_dev.txt
	pip freeze >> requirements.txt

commit:
	git add *
	git commit -m '${m}'
	git push origin main

deploy:
	git push heroku main
	heroku run "alembic upgrade head"

start:
	uvicorn app.main:app --reload

black: 
	black .

migrate:
	alembic upgrade head

makemigrations:
	alembic revision --autogenerate -m "'${m}'"

test:
	pytest -v -s