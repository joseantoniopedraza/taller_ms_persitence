precommit:
	
	black . --config pyproject.toml
	ruff check . --fix
	ruff format .

runserver:
	python manage.py runserver

test:
	python manage.py test
	