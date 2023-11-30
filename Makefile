lint:
	flake8 ./sat/

test:
	coverage run -m --omit="*/tests/*" pytest ./tests/ && coverage report -m