test:build
	python -m unittest -f
	python test_dmtaclasses/*_test.py

build:
	python -m pip install -U build
	python -m build
	python -m pip install dist/*.whl
