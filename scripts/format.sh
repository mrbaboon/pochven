#!/usr/bin/env bash

set -ex

# trim whitespace
find . -name '*.py' | xargs sed -i '' -e :a -e '/^\n*$/{$d;N;};/\n$/ba'

black .

autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place . --exclude=__init__.py,venv
isort .
