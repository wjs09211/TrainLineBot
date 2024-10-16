FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /code

WORKDIR /code

COPY requirements.txt /tmp/requirements.txt
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN set -ex && \
    pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    rm -rf /root/.cache/

COPY . /code/

EXPOSE 8080

# replace demo.wsgi with <project_name>.wsgi
CMD ["gunicorn", "--bind", ":8080", "--workers", "2", "TrainLineBot.wsgi"]
