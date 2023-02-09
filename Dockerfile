FROM python:3.9 AS python

WORKDIR /Hardwaresteuerung

# Copy project files
COPY ./requirements.txt /Hardwaresteuerung/requirements.txt


# Install python packages
RUN pip install -r requirements.txt --upgrade-strategy only-if-needed

FROM python
COPY ./src /Hardwaresteuerung/src

# Update
# RUN apt-get autoremove && apt-get -f install && apt-get update && apt-get upgrade -y

# Exposed port to access fastapi rest service
EXPOSE 8096

# Start fastapi on container start
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8096"]
