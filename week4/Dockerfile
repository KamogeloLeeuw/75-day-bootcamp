# Using python 3.12 slim image as a base
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

# installing dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY . . 

CMD ["python", "etl_pipeline.py"]