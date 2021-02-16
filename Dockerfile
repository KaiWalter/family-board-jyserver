FROM arm32v7/python as BASE

RUN apt-get update
RUN apt-get install -y libffi6 libffi-dev
RUN apt-get install -y build-essential libssl-dev libffi-dev python3-dev cargo
RUN apt-get install -y python3-dev python3-distutils python3-setuptools
RUN apt-get install -y locales locales-all

RUN pip install cryptography

FROM BASE

ADD ./src /app

WORKDIR /app

RUN pip install -r ./requirements.txt

EXPOSE 8080

CMD [ "python", "./server.py", "-a", "0.0.0.0", "-p", "8080" ]