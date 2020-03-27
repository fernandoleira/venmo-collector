FROM ubuntu:18.04

# Install ubuntu dependencies
RUN apt-get update -y
RUN export DEBIAN_FRONTEND=noninteractive && ln -fs /usr/share/zoneinfo/America/New_York /etc/localtime
RUN apt-get install python3-dev python3-pip postgresql libpq-dev -y
RUN dpkg-reconfigure --frontend noninteractive tzdata

# Move to the home folder
WORKDIR /home

# Install dependencies using pip
COPY requirements.txt /
RUN  pip3 install -r /requirements.txt

# Copy all project files and open folder
COPY venmo-collector /venmo-collector

# Run command
CMD ["python3", "venmo-collector/main.py"]
