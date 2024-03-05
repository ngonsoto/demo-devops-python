# dockerfile

# using pyhton 3.11.3 as required on the python app documentation
FROM python:3.11.3

# install dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# copy the application to the container
COPY . /home/docker
WORKDIR /home/docker

# Create a non-root user
RUN addgroup --system djangogrp && adduser --system --ingroup djangogrp djangousr

# Set ownership and permissions
RUN chown -R djangousr:djangogrp /home/docker

# Switch to non-root user
USER djangousr

# open port 8000
EXPOSE 8000

# run the application
CMD ["bash", "entrypoint.sh"]

# verify application health
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD curl --fail http://localhost:8000/api/ || exit 1