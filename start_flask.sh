#!/bin/bash

uwsgi --ini /etc/uwsgi/uwsgi.ini
# waitress-serve --port=3344 opera_flask:app