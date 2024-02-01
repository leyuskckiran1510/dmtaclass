test:build
	python3.12 -m unittest -f
	python3.12 test_dmtaclasses/*_test.py

build:
	python3.12 -m pip install -U build
	python3.12 -m build
	python3.12 -m pip install dist/*.whl
