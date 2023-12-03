lint:
	flake8 ./sat/ ./tests/

test:
	coverage run -m --omit="*/tests/*" pytest ./tests/ && coverage report -m