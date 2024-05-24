FROM python:3.10.10

# Setup working directory
COPY . .
WORKDIR /src

# Runners
WORKDIR ..
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

ENV TZ=Asia/Seoul
EXPOSE 8000

ENTRYPOINT uvicorn main:app --host=0.0.0.0 --port=8000 --reload