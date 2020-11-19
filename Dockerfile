FROM python:3.6-jessie

RUN apt-get update
RUN apt-get install libpcap-dev -y
RUN apt install tree

ENV INSTALL_PATH /app/
RUN mkdir -p $INSTALL_PATH

WORKDIR $INSTALL_PATH

RUN wget https://lcamtuf.coredump.cx/p0f3/releases/p0f-3.09b.tgz
RUN tar -xzvf p0f-3.09b.tgz
WORKDIR p0f-3.09b
RUN ./build.sh

WORKDIR $INSTALL_PATH

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 80

COPY . .
CMD ["python", "driver.py"]
