# dockerfile

# using pyhton 3.11.3 as required on the python app documentation
FROM python:3.11.3

# install dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# copy the application to the container
COPY . /home/docker
WORKDIR /home/docker

# open port 8000
EXPOSE 8000

# run the application
CMD ["bash", "entrypoint.sh"]