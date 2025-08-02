precommit:
	
	black . --config pyproject.toml
	ruff check . --fix

runserver:
	python manage.py runserver

test:
	python manage.py test
	