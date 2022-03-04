ENV = env
BIN = $(ENV)/bin
PYTHON_VERSION = 3
PYTHON = $(BIN)/python
CODE_LOCATIONS = django_anonymous test_project manage.py setup.py

clean:
	rm -rf env
	rm -rf build
	rm -rf dist
	rm -rf *.egg
	rm -rf *.egg-info
	find | grep -i ".*\.pyc$$" | xargs -r -L1 rm

venv: clean
	$(shell which python$(PYTHON_VERSION)) -m venv $(ENV)

setup: venv
	$(BIN)/pip install -r requirements.txt

fix-codestyle:
	$(BIN)/black $(CODE_LOCATIONS)
	$(BIN)/isort $(CODE_LOCATIONS)

lint:
	$(BIN)/black --check $(CODE_LOCATIONS)
	$(BIN)/isort --check-only $(CODE_LOCATIONS)
	$(BIN)/flake8 $(CODE_LOCATIONS)

test: lint
	$(PYTHON) -X dev -m pytest $(ARGS)