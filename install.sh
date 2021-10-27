#!/bin/sh

python3 -m venv .
source ./bin/activate

python -m pip install pydantic
python -m pip install python-dateutil
