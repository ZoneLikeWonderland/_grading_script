FROM ubuntu:16.04

# Proudly served by GeekPie Association and SIST @ ShanghaiTech
RUN sed -i 's/archive.ubuntu.com/mirrors.geekpie.club/' /etc/apt/sources.list

# install dependencies of sandbox and scripts
RUN apt-get update && apt-get install -y cmake python3 python3-pip libseccomp-dev gcc g++

# Install your custom dependency here
# Just prefix your install command with RUN
# For apt, you don't need to apt-get update as we have done it for you
# RUN apt-get install gcc-multilib

# Install sandbox
COPY qdujudger /tmp/qdujudger
RUN cd /tmp/qdujudger && \
	cmake . && \
	make && \
	make install && \
	rm -rf /tmp/qdujudger

# This is the user that student program will run under
RUN groupadd -g 1000 student && useradd -g 1000 -u 1000 -d /test student  

# you can add dependencies from other kind of repositories as well.
# Just prefix the installation command with RUN,
# and make sure the package manangement tool is installed
RUN pip3 install pip

# /test will hold test output, but it's not mandatory nor hardcoded
# /submission will hold student submission and this name is mandatory and hardcoded
RUN mkdir /test /submission && touch /test/output

# Copy the grading scripts
COPY setup build run grade *.sh *.awk *.py /judge/
COPY grading /judge/grading

# Copy the testcases
# Here we don't have any so it's commented out
#COPY input /test/input

# Fix permission
RUN chmod 500 -R /judge /submission && chown student:student -R /test

# Generate the reference output
# Here we use static ones
# RUN python3 /judge/grading/generate_output.py > /judge/grading/output
COPY tests /judge/tests
