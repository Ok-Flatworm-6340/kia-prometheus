.PHONY: build down logs run up venv

CONTAINER_RUNTIME ?= podman

build:
	$(CONTAINER_RUNTIME) compose build

down:
	$(CONTAINER_RUNTIME) compose down

logs:
	$(CONTAINER_RUNTIME) compose logs -f

run: venv
	.venv/bin/python3 build/main.py

up:
	$(CONTAINER_RUNTIME) compose up -d

venv:
	python3 -m venv .venv
	.venv/bin/pip3 install -r build/requirements.txt
	