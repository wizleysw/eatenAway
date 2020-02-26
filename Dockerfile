FROM python:3

MAINTAINER Wizley <wizley@kakao.com>

WORKDIR /code
COPY ./requirements.txt /code

RUN pip3 install -r ./requirements.txt

ENTRYPOINT \
	django-admin startproject eatenAway && \
	python3 $(pwd)/eatenAway/manage.py makemigrations && \
	python3 $(pwd)/eatenAway/manage.py migrate && \
	echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('root', 'wizley@github.com', 'alpine')" | python3 $(pwd)/eatenAway/manage.py shell && \
	python3 $(pwd)/eatenAway/manage.py runserver 0.0.0.0:8000

