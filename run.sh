#!/usr/bin/env bash
gunicorn -c gunicorn.conf.py index:app