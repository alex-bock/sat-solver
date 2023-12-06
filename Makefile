clean:
	find . -path "*/__pycache__/*" -delete
	find . -type d -name "__pycache__" -empty -delete
	rm -rf .pytest_cache
	rm .coverage

lint:
	flake8 ./sat/ ./tests/ run.py

test:
	coverage run --source ./sat/ -m --omit="*/tests/*" pytest ./tests/ && coverage report -m