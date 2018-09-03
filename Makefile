format:
	yapf **/*.py -i

release:
	python3 setup.py sdist bdist_wheel
	twine upload --repository-url https://upload.pypi.org/legacy/ dist/* -u $PYPI_USERNAME -p $PYPI_PASSWORD
