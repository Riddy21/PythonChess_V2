all: clean test play


play: main.py
	python3 main.py

test: unittest systemtest

unittest:
	python3 -m coverage run -a -m unittest utests/test_*.py

systemtest:
	python3 -m coverage run -a -m unittest systemtests/test_*.py

clean:
	-rm -rf __pycache__
	-rm -rf systemtests/__pycache__
	-rm -rf utests/__pycache__
	-rm -rf htmlcov/
	-rm .coverage

test_%: utests/test_%.py
	python3 -m coverage run -a -m unittest $<

test_%: systemtests/test_%.py
	python3 -n coverage run -a -m unittest $<

coverage:
	coverage html
	open htmlcov/index.html

