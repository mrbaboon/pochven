#!/usr/bin/env bash
set -ex

coverage erase
coverage run manage.py test --noinput
coverage report
