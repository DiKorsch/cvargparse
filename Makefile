install:
	pip install . --no-deps --upgrade

build:
	python setup.py build

deploy:
	python setup.py sdist upload -r pypi

test_deploy:
	python setup.py sdist upload -r pypitest

get_version:
	@python -c "import cvargparse; print('v{}'.format(cvargparse.__version__))"
