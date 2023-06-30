# Use bullseye for a smaller image size and install only the required packages.
# Bookworm is available but at the time of writing is 5 days old.
FROM python:3.10-slim-bullseye

# > Setting PYTHONUNBUFFERED to a non empty value ensures that the python output is sent straight to
# > terminal (e.g. your container log) without being first buffered and that you can see the output
# > of your application (e.g. django logs) in real time.
# https://stackoverflow.com/a/59812588
ENV PYTHONUNBUFFERED 1

# Install required libs
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    git

# Install the package manager - pipenv
RUN pip install --upgrade pip && \
    pip install --no-cache-dir pipenv

# Change the working directory for all proceeding operations
#   https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#workdir
WORKDIR /code

# "items (files, directories) that do not require ADD’s tar auto-extraction capability, you should always use COPY."
#   https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#add-or-copy
COPY Pipfile .
COPY Pipfile.lock .

# Install both default and dev packages so that we can run the tests against this image
RUN pipenv sync --dev --system && \
    pipenv --clear

# Copy all the source to the image
COPY . .

RUN pipenv install --dev

# "The best use for ENTRYPOINT is to set the image’s main command, allowing that image to be run as though it was that
#   command (and then use CMD as the default flags)."
#   https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#entrypoint
ENTRYPOINT [ "python3" ]
CMD ["run.py"]
