FROM python:3.9

WORKDIR /Hardwaresteuerung

# Copy project files
COPY ./requirements.txt /Hardwaresteuerung/requirements.txt
COPY ./src /Hardwaresteuerung/src


# Install python packages
RUN pip install --no-cache-dir -r requirements.txt

# Update
# RUN apt-get autoremove && apt-get -f install && apt-get update && apt-get upgrade -y

# Exposed port to access fastapi rest service
EXPOSE 8096

# Start fastapi on container start
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8096"]