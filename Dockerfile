ARG PYTHON_VERSION=3.8.10
ARG APP_PORT=8000

# Pull base image
FROM python:${PYTHON_VERSION}-buster

# Set environment varibles
ARG DEBIAN_FRONTEND=noninteractive
ENV ACCEPT_EULA=Y
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set main working dir
WORKDIR /app

# Update
RUN apt-get -y update --fix-missing && \
    apt-get upgrade -y && \
    apt-get --no-install-recommends install -y apt-utils && \
    rm -rf /var/lib/apt/lists/*


# Install useful tools and install important libaries
RUN apt-get -y update && \
    apt-get -y --no-install-recommends install nano wget dialog libsqlite3-dev libsqlite3-0 unzip && \
    apt-get -y --no-install-recommends install mariadb-client zlib1g-dev libzip-dev libicu-dev && \
    apt-get -y --no-install-recommends install --fix-missing apt-utils build-essential git curl && \
    apt-get -y --no-install-recommends install --fix-missing libcurl4 libcurl4-openssl-dev zip openssl libssl-dev && \
    apt-get -y --no-install-recommends install --fix-missing libonig-dev openssh-client && \
    apt-get -y install net-tools && \
    rm -rf /var/lib/apt/lists/*

# Languages
RUN apt-get -y update && \
    apt-get install -y locales locales-all
ENV LC_ALL es_ES.UTF-8
ENV LANG es_ES.UTF-8
ENV LANGUAGE es_ES.UTF-8

# Add bash aliases
COPY /.docker/shoes/shoes_api/.bash_aliases /root/.bash_aliases
RUN echo '\n\
        \n# Alias\
        \nif [ -f ~/.bash_aliases ]; then\
        \n    . ~/.bash_aliases\
        \nfi\
    ' >> /root/.bashrc

# Install bash completion
RUN apt-get -y update && \
    apt-get install -y bash-completion

# Add Autocompletions
ENV SHELL bash
RUN echo '\n\
        \n# Add General Autocompletions\
        \nsource "/etc/profile.d/bash_completion.sh"\
    ' >> /root/.bashrc

# Cleanup
RUN rm -rf /usr/src/*

# Copy pipenv deps version control files
COPY /apps/shoes/Pipfile /apps/shoes/Pipfile.lock /app/apps/shoes/

# Install pipenv
RUN pip install pipenv

# Go to service entry point folder
WORKDIR /app/apps/shoes

# Install dependencies throught pipenv
RUN pipenv install --deploy --dev
RUN pipenv --venv >> /app/.pipenv-details

# Back to root folder
WORKDIR /app

# Expose listen ports
EXPOSE ${APP_PORT}

# Run app
CMD ["pipenv", "run", "uvicorn", "apps.shoes.main:app", "--reload", "--host", "0.0.0.0"]