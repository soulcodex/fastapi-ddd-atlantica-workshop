FROM python:3.8-slim-buster

# ICU & Timezone
RUN apt update && apt install tzdata -y && echo "UTC" > /etc/timezone

# Add utils packages
RUN apt install -y figlet make curl wget
RUN wget -qO /usr/local/bin/yq https://github.com/mikefarah/yq/releases/latest/download/yq_linux_amd64
RUN chmod a+x /usr/local/bin/yq

# pip install via get-pip script
RUN curl -o get-pip.py -X GET https://bootstrap.pypa.io/get-pip.py
RUN python get-pip.py
RUN rm get-pip.py

# Set root working dir
WORKDIR /app

# Copy pipenv deps version control files
COPY Pipfile Pipfile.lock /app/apps/shoes/

# Set shoes api working dir
WORKDIR /app/apps/shoes/

# Install poetry
RUN pip install pipenv
RUN pipenv install --dev

# Copy entrypoint and superfluos things
COPY ./docker/.bash_profile /root/.profile
COPY ./docker/shoes-api/tools /root/tools
COPY ./docker/shoes-api/entrypoint.sh /root/entrypoint.sh
RUN chmod +x /root/entrypoint.sh /root/tools/*.sh

# Define entrypoint script
ENTRYPOINT ["/root/entrypoint.sh"]

# Back to the working root working directory
WORKDIR /app

# Expose ports
EXPOSE 8000