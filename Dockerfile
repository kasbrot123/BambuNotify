FROM python:3.12-slim
WORKDIR /app
RUN pip install --no-cache-dir paho-mqtt
COPY bambu_notify.py .
CMD ["python", "-u", "bambu_notify.py"]
