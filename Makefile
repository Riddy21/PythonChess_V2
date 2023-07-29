all: clean test

test: unittest systemtest

unittest:
	python3 -m unittest utests/test_*.py

systemtest:
	python3 -m unittest systemtests/test_*.py

clean:
	rm -rf __pycache__
	rm -rf systemtests/__pycache__
	rm -rf utests/__pycache__

test_%: utests/test_%.py
	python3 -m unittest $<

test_%: systemtests/test_%.py
	python3 -m unittest $<
