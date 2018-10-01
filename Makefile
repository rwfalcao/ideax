PROCS=4

test:
	py.test -n $(PROCS) --reuse-db ${ARGS}

test_newdb:
	py.test -n $(PROCS) --create-db ${ARGS}

test_snapshot:
	py.test -n $(PROCS) --snapshot-update ${ARGS}

test_coverage:
	py.test -n $(PROCS) --reuse-db --cov-report term-missing --cov=apps

test_watch:
	ptw -c -- -n $(PROCS) --reuse-db ${ARGS}

test_ci:
	py.test --create-db
