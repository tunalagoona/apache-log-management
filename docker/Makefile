USER := tunalagoona
NAME := apache_log_manager
IMG := ${USER}/${NAME}:latest

build:
	@docker build -t ${IMG} -f docker/Dockerfile .

rebuild:
	@docker build --no-cache -t ${IMG} -f docker/Dockerfile .

init:
	@docker run -v $(shell pwd)/data:/package/data -it ${IMG} bash -c "apache_log_manager/init.sh"

shell:
	@docker run -v $(shell pwd)/data:/package/data -it ${IMG} bash -c "/bin/bash"

load:
	@docker run -v $(shell pwd)/data:/package/data -it ${IMG} bash -c "python3 apache_log_manager/manage.py process_log $(link)"

app:
	@docker run -v $(shell pwd)/data:/package/data -it -p 8000:8000 ${IMG} bash -c "python3 apache_log_manager/manage.py runserver 0.0.0.0:8000"

push:
	@docker push ${IMG}

pull:
	@docker pull ${IMG}
