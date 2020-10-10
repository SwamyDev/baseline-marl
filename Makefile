.PHONY: help clean setup test

.DEFAULT: help
help:
	@echo "make clean"
	@echo "	clean all python build/compilation files and directories"
	@echo "make setup"
	@echo "	create virtual environment and install dependencies"
	@echo "make test"
	@echo " run all tests and coverage"

clean:
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +
	find . -name '*~' -exec rm --force {} +
	rm --force .coverage
	rm --force --recursive .pytest_cache
	rm --force --recursive build/
	rm --force --recursive dist/
	rm --force --recursive *.egg-info

baseline-marl/_version.py:
	python meta.py $(shell git describe --tags --abbrev=0 --always)


third_party/.install.done:
	pip install --upgrade pip setuptools
	cd third_party/stable-baseline3/; pip install -e .[extra]
	touch third_party/.install.done

.install.done: baseline-marl/_version.py third_party/.install.done
	pip install -e .
	touch .install.done

setup: .install.done

.install.test.done: baseline-marl/_version.py
	pip install -e .[test]
	touch .install.test.done

test: third_party/.install.done .install.test.done
	pytest --verbose --color=yes --cov=amarl --cov-report term-missing tests 


.try.done:
	echo "running try"
	touch .try.done

try: .try.done
