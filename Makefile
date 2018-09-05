.PHONY: test

help:
	@echo "  env            create a development environment using virtualenv"
	@echo "  upgrade        upgrade dependencies to latest version"
	@echo "  clean          remove unwanted stuff"

env:
	python3 -m venv .env && \
	. .env/bin/activate && \
	pip install --upgrade pip && \
	make deps && \
	pre-commit install


deps:
	pip3 install -r requirements.txt

upgrade:
	pur -r requirements.txt

clean:
	find . -name '*.pyc' -exec rm -f {} \; && \
  	rm -rf temp && \
  	rm -rf dist && \
  	rm -fr .env
