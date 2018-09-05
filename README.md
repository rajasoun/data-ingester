# Ingest Data From External Datasource

Data Ingestion Tool from External sources like Google Analytics,  Database or Log Files

# [Google Analytics Setup](https://developers.google.com/analytics/devguides/reporting/core/v4/quickstart/service-py)
Refer steps required to access the Analytics Reporting API v4.

# [pre-commit](https://pre-commit.com/) hook

```
python3 -m pip install pre-commit
pre-commit clean
pre-commit install
pre-commit install-hooks
```


# [venv](https://docs.python.org/3/library/venv.html)
The venv module provides support for creating lightweight “virtual environments” with their own site directories,
optionally isolated from system site directories. Each virtual environment has its own Python binary
(which matches the version of the binary that was used to create this environment) and can have its own independent set of
installed Python packages in its site directories.

Its assumed Python3 and  pip3 are already Installed.

```
python3 -m venv .env
source .env/bin/activate
```

# Running the Program

```
python3 get_ga_data.py
deactivate
```


# Safety
Safety checks  dependencies for known security vulnerabilities.

```
safety check -r requirements.txt
```
