#!/usr/bin/env bash

echo "Running gunicorn..."
gunicorn app:app --bind 0.0.0.0 --access-logfile - --access-logformat '{"request": "%(r)s", "http_status_code": "%(s)s", "http_request_url": "%(U)s", "http_query_string": "%(q)s", "http_verb": "%(m)s", "http_version": "%(H)s"}'
