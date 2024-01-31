#!/usr/bin/env bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# move to the root of the project
cd "${SCRIPT_DIR}/../"

time python3.10 -m src.forecasting_session
