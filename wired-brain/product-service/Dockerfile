# Build image from Python 3.9.1 Official Image as base layer
FROM python:3.9.1

# Set the current working directory of the image to code/
WORKDIR /code

# Copy the requirements.txt file to the current working directory in the image
COPY requirements.txt .


# Run pip install to install depdencies
RUN pip install -r requirements.txt

# Copy our source code to /code/src in the image
COPY src/ .

# Run python ./app.py 
CMD ["python", "./app.py"]