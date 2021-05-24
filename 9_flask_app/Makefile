build:
	make build-pg \
	&& make build-nginx \

build-pg:
	python3 -m pip install -r ./main_page/requirements.txt \
	&& docker-compose build main_page \

build-nginx:
	docker-compose build nginx


dev:
	docker-compose up