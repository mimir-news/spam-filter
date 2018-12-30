export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=spamfilter
export DB_USERNAME=spamfilter
export DB_PASSWORD=password
export CASHTAG_THRESHOLD=0.8
export TRAIN_MODEL=FALSE

NAME = $(shell appv name)
IMAGE = $(shell appv image)
VERSION = $(shell appv version)

run:
	sh start.sh

db-init:
	rm -rf migrations
	flask db init

db-migrate:
	flask db migrate

db-upgrade:
	flask db upgrade

db-downgrade:
	flask db downgrade

test:
	mypy --ignore-missing-imports run.py

install:
	pip install -r requirements.txt

build:
	docker build -t $(IMAGE) .

build-test:
	docker build -t "$(NAME)-test:$(VERSION)" -f Dockerfile.test .

run-container:
	docker run -d --name $(NAME) -p 8080:8080 --network=mimir-net \
		-e DB_HOST=mimir-db -e DB_PORT=5432 -e DB_NAME=spamfilter \
		-e DB_USERNAME=spamfilter -e DB_PASSWORD=password \
		-e SERVICE_NAME=$(NAME) -e SERVICE_VERSION=$(VERSION) \
		$(IMAGE)
