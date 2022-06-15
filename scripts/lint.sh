#!/usr/bin/env bash

set -xe
black --check .
isort --check-only .
flake8 --max-line-length 120
