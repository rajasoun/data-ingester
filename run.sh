#!/usr/bin/env sh

# To Run the Forecast in headless Mode
make env && \
. .env/bin/activate && \
python3 get_ga_data.py
