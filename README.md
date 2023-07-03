<!-- omit from toc -->
# Janitor
A Python application which hosts task scripts for data management and clean up tasks, running them on a schedule.
The application uses APScheduler to schedule and run these tasks.

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

The app can be configured to run with development settings by adding

    SETTINGS_MODULE=janitor.config.development

to a `.env` file.

## Running the Application

Enter the virtual environment with

    pipenv shell

The application can then be started by running

    python run.py

This will start the APScheduler and run the scheduled tasks.

### Adding Tasks

Tasks can be added by creating scripts in the `janitor/tasks` directory, wrapping your task in a function and importing that to `run.py`.
The task can then be scheduled to run by using `sched.add_job(...)`.

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

All three tools can be run by executing:

    ./forlint.sh

## Deployment

This application gets deployed as a Docker image.
The `.release-version` uses SemVer (major/minor/patch).
Merging a pull request into *develop* or *main* creates a release with an associated Docker image.
