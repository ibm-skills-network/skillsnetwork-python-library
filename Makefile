.PHONY: install install-extras install-docs build local-pypi jupyterlite-dev jupyterlab-dev format test test-core clean

install:
				poetry install

install-extras:
				poetry install -E regular

install-docs:
				poetry install --no-root -E docs

update:
				poetry update

build:
				poetry run python -m build

local-pypi: build
				cp dist/* local-pypi/skillsnetwork/
				poetry run python local-pypi/pypi-server.py --directory local-pypi

jupyterlite-dev:
				poetry install
				poetry run jupyter lite serve

jupyterlab-dev:
				poetry install -E regular
				poetry run jupyter lab --ServerApp.password='' --ServerApp.token=''

format:
				poetry run black .

test:
				poetry run pytest -rP tests/

test-core:
				poetry run pytest tests/ -k 'test_skillsnetwork.py'

clean:
				rm *.ipynb || echo "no notebooks to clean up"
				rm dist/* || echo "no builds to clean up"
				rm local-pypi/skillsnetwork/skillsnetwork* || echo "no local pypi files to clean up"
				echo "done cleaning"
