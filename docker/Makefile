USER := tunalagoona
NAME := apache_log_manager
IMG := ${USER}/${NAME}:latest

build:
	@docker build -t ${IMG} -f docker/Dockerfile .

shell:
	@sudo docker run -it ${IMG} bash -c "/bin/bash"

load:
	@sudo docker run -it ${IMG} bash -c "python3 apache_log_manager/manage.py process_log $(link)"

app:
	@sudo docker run -it -p 8000:8000 ${IMG} bash -c "python3 apache_log_manager/manage.py runserver 0.0.0.0:8000"

push:
	@sudo docker push ${IMG}

pull:
	@sudo docker pull ${IMG}
