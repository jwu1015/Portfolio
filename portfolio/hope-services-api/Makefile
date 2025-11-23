.PHONY: run seed test lint clean docker-build docker-run

run:
	python run.py

seed:
	python seed.py

test:
	pytest -q -v

lint:
	flake8 app/ tests/ || true
	pylint app/ || true

clean:
	find . -type d -name __pycache__ -exec rm -r {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	rm -f hope_services.db

docker-build:
	docker build -t hope-services-api .

docker-run:
	docker run -p 5000:5000 hope-services-api

install:
	pip install -r requirements.txt

dev-install:
	pip install -r requirements.txt
	pip install flake8 pylint pytest pytest-flask


