#!/bin/sh
source venv/bin/activate
gunicorn -w 3 -b 127.0.0.1:5000 server:app
