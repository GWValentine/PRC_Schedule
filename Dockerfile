# Dockerfile to create the container image for PRC Schedule App
FROM python:3.10-slim
LABEL maintainer="Grant Valentine <gw.valentine11@gmail.com>"

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

# playing with the secret keys
ARG API_KEY
ENV API_KEY=$API_KEY

EXPOSE 8000
CMD ["streamlit", "run", "--server.port", "8000", "src/PRC_Schedule.py"]