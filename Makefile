init:
	python -m venv ./venv
	pip install --upgrade pip
	pip install -r requirement-dev.txt

format:
	yapf **/*.py -i

release:
	python setup.py sdist bdist_wheel
	twine upload --repository-url https://upload.pypi.org/legacy/ dist/* -u ${PYPI_USERNAME} -p ${PYPI_PASSWORD}
