_python_pkg = csfd_export

.PHONY: run
run:  ## Start the development server
	poetry run python manage.py runserver

.PHONY: worker
worker:  ## Start the Celery worker server
	DJANGO_SETTINGS_MODULE=csfd_export.settings \
	poetry run celery -A csfd_export.tasks worker --loglevel=INFO

.PHONY: redis
redis:  ## Start the Redis message broker
	redis-server --port 0 --unixsocket /run/user/1000/redis.sock

.PHONY: setup
setup:  ## Install Python dependencies
	poetry install

.PHONE: test
test:  ## Test Python code
	poetry run pytest $(_python_pkg)

.PHONE: lint
lint:  ## Lint Python code
	poetry run flake8 $(_python_pkg)
	poetry run mypy $(_python_pkg) --ignore-missing-imports
	poetry run isort -c $(_python_pkg)

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-16s\033[0m %s\n", $$1, $$2}'
