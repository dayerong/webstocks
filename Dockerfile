# pull official base image
FROM hub.cuanon.com/infra-app/python:3.10.11-slim-buster

# set work directory
WORKDIR /webstock

#TZ
ENV TZ Asia/Shanghai

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy requirements file
COPY ./src/requirements.txt /webstock/requirements.txt

# install dependencies
RUN set -eux \
    && pip install -r /webstock/requirements.txt -i https://mirrors.aliyun.com/pypi/simple/\
    && pip install akshare -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host=mirrors.aliyun.com  --upgrade \
    && rm -rf /root/.cache/pip

# copy project
COPY ./src /webstock

# RUN APP
CMD ["python", "./app/main.py"]
