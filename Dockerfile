FROM python:3.10.10

# Setup working directory
WORKDIR /app
COPY . /app

# Runners
RUN pip install --no-cache-dir -r requirements.txt
ENV TZ=Asia/Seoul

EXPOSE 8000

ENTRYPOINT uvicorn main:app --host=0.0.0.0 --port=8000 --reload