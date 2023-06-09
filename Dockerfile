FROM python:3.11.3-slim-buster
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app/

RUN flask --app config db upgrade

RUN apt-get update && apt-get install -y tzdata && \
    ln -fs /usr/share/zoneinfo/Europe/Kiev /etc/localtime && \
    dpkg-reconfigure --frontend noninteractive tzdata

CMD sh -c "python daily_script.py >> daily_script.log 2>&1 & python main.py"
