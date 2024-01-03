[![python](https://img.shields.io/badge/Python-3.10-3776AB.svg?style=flat&logo=python&logoColor=ffd343)](https://docs.python.org/3.10/)
[![codecov](https://codecov.io/gh/sanger/janitor/branch/main/graph/badge.svg?token=326K6QWD3V)](https://codecov.io/gh/sanger/janitor)
<!-- omit from toc -->
# Janitor
A Python application which hosts task scripts for data management and clean up tasks, running them on a schedule.
The application uses [APScheduler](https://apscheduler.readthedocs.io/en/3.x/) to schedule and run these tasks.

<!-- omit from toc -->
## Table of Contents

- [Getting Started](#getting-started)
  - [Requirements for Development](#requirements-for-development)
  - [Installing Dependencies](#installing-dependencies)
  - [Configuring the Environment](#configuring-the-environment)
- [Running the Application](#running-the-application)
  - [Adding Tasks](#adding-tasks)
- [Testing](#testing)
- [Formatting, Type Checking and Linting](#formatting-type-checking-and-linting)
- [Deployment](#deployment)
- [Tasks](#tasks)
  - [Labware Location](#labware-location)
  - [Sequencing Publisher](#sequencing-publisher)
- [Updating the Table of Contents](#updating-the-table-of-contents)


## Getting Started

### Requirements for Development

The following tools are required for development:

- Python (use a tool like `pyenv` to install the required version specified in the `Pipfile`)
- Install dependencies using [pipenv](https://github.com/pypa/pipenv):

    brew install pipenv

### Installing Dependencies

Install the required dependencies:

    pipenv install
    pipenv install --dev

### Configuring the Environment

The app uses a `.env` file for configuration settings.
The `.env.example` file can be copied and renamed to `.env` to load in those environment variables.

    cp .env.example .env

## Running the Application

Enter the virtual environment with

    pipenv shell

The application can then be started by running

    python run.py

This will start the APScheduler and run the scheduled tasks.

### Adding Tasks

Tasks can be added by creating scripts in the `janitor/tasks` directory, wrapping your task in a function and importing that to `run.py`.
The task can then be scheduled to run by using `sched.add_job(...)` (see [documentation](https://apscheduler.readthedocs.io/en/3.x/userguide.html#adding-jobs)).

## Testing

This application uses Pytest for the unit tests.
To run the tests:

    pipenv run test

This will generate code coverage reports in `xml` and `html` formats.

## Formatting, Type Checking and Linting

Black is used as a code formatter:

    black .

Mypy is used as a type checker:

    mypy .

Flake8 is used for linting:

    flake8

isort is used for tidying up imports:

    isort .

All four tools can be run by executing:

    ./forlint.sh

**Note:** VSCode settings have been included in the repository and are consistent with the configurations in `pyproject.toml` and `setup.cfg` so that the code is formatted on save.

## Deployment

This application gets deployed as a Docker image.
The `.release-version` uses SemVer (major/minor/patch).
Merging a pull request into *develop* or *main* creates a release with an associated Docker image.

The [deployment](https://github.com/sanger/deployment) repository is used to deploy the application.
The instructions for doing so can be found in `deploy_janitor.yml`.

## Tasks

### Labware Location

This task retrieves data from various tables in the LabWhere database and compiles it into a single table `labware_location` in the MLWH database.
This table stores the latest known locations of labwares which is a more convenient way of tracking labwares.
The task checks for changes every 5 minutes and will update all entries which have been changed since the latest entry in the table.

**Note:** The SQL query for retrieving the latest updates from the LabWhere database checks all entries with a timestamp greater than or equal to the latest entry in the `labware_location` table (i.e. the entry with the latest `stored_at` timestamp).
This means that even if there are no updates since the last time the task ran, it will still update the latest entry in the table and thus the logs will always report 1 entry being updated. (`Updating 1 rows...`)

### Sequencing Publisher

This task queries the MLWH and MLWH Events databases for sample sequencing run status changes and publishes these changes to RabbitMQ.
These messages are published to a fanout exchange using the message schema found in `janitor/tasks/sequencing_publisher/message_schemas/sample_sequence_status.avsc`.
Users can consume from this queue to retrieve sequencing run status changes without needing to poll the MLWH database.

The messages are sent in groups where each individual message corresponds to a row returned from the SQL query to retrieve sequencing run status changes.

**Note:** If an error occurs when messages are being published to RabbitMQ, the earliest timestamp from the group of messages which failed to publish is saved.
This timestamp is used to retrieve changes when the job is ran next which means that there may be duplicate messages published to consumers but using the timestamp this way minimises the number of duplicate messages.

## Updating the Table of Contents

Node is required to run npx:

    npx markdown-toc -i README.md
