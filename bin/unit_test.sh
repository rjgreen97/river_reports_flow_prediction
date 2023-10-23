#!/usr/bin/env bash

# Run unit tests

# python3 -m pytest tests/ "$@"
python3 -m pytest -W ignore::DeprecationWarning -W ignore::UserWarning -vv -s tests/ "$@"
