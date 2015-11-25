.PHONY: clean test

clean:
	./clean.sh

test: clean
	flake8
	coverage run --source geotrie -m py.test tests/
	coverage report -m
