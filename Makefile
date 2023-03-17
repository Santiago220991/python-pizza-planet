VENV_NAME=.venv

create-venv:
	python3.9 -m venv $(VENV_NAME)
	. $(VENV_NAME)/bin/activate && pip install -r requirements.txt

db-start:
	. $(VENV_NAME)/bin/activate && python3 manage.py db init
	. $(VENV_NAME)/bin/activate && python3 manage.py db migrate
	. $(VENV_NAME)/bin/activate && python3 manage.py db upgrade

db-seed:
	. $(VENV_NAME)/bin/activate && flask seed run

db-delete:
	rm -r migrations
	rm -r pizza.sqlite

start-app:
	. $(VENV_NAME)/bin/activate && python3 manage.py run

run-tests:
	. $(VENV_NAME)/bin/activate && python3 manage.py test 

