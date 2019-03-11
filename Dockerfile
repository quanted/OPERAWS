#ARG version=dev
#FROM quanted/qed_py3:$version
FROM python:3.7

# Install requirements
COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

# Install uWSGI
RUN pip install uwsgi

# Overwrite the uWSGI config
COPY uwsgi.ini /etc/uwsgi/

COPY . /src/
WORKDIR /src

EXPOSE 3344

RUN chmod 755 /src/start_flask.sh

CMD ["sh", "/src/start_flask.sh"]