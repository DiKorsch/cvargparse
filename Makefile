install:
	python setup.py install

build:
	python setup.py build

deploy:
	python setup.py sdist upload -r pypi

get_version:
	@python -c "import cvargparse; print('v{}'.format(cvargparse.__version__))"
