#!/usr/bin/env bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# move to the root of the project
cd "${SCRIPT_DIR}/../"

python3 -m src.forecasting_session
