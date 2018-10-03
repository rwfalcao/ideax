PROCS=4

test:
	py.test -n $(PROCS) --reuse-db ${ARGS}

test_newdb:
	py.test -n $(PROCS) --create-db ${ARGS}

test_snapshot:
	py.test -n $(PROCS) --snapshot-update ${ARGS}

test_coverage:
	py.test -n $(PROCS) --reuse-db --cov-report term-missing --cov=ideax

test_watch:
	ptw -c -- -n $(PROCS) --reuse-db ${ARGS}

test_ci:
	py.test --create-db

pip_outdated:
	pip list --outdated --format=columns

lint:
	flake8 ideax

pylint:
	pylint ideax

ci: lint test_ci
	@echo "done"
