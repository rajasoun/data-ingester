.PHONY: test

help:
	@echo "  env            create a development environment using virtualenv"
	@echo "  run            download the google analytics data"
	@echo "  upgrade        upgrade dependencies to latest version"
	@echo "  clean          remove unwanted stuff"

env:
	pipenv shell \
	make deps && \
	pre-commit clean
	pre-commit install
	pre-commit install-hooks

deps:
	pipenv update

run:
	python3 get_ga_data.py

upgrade:
	pipenv upgrade

clean:
	find . -name '*.pyc' -exec rm -f {} \; && \
  	rm -rf temp && \
  	rm -rf dist && \
  	pipenv --rm
