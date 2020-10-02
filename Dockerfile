FROM ubuntu:bionic

RUN apt-get -qq update && apt-get -q install -y \
    git \
    python3-dev python3-pip python-virtualenv \
    libffi-dev libssl-dev

ADD . /st2docs
WORKDIR /st2docs
RUN make .cleandocs && make docs

EXPOSE 8000

CMD make .livedocs

#CMD  . ./virtualenv/bin/activate; \
#    sphinx-autobuild -H 0.0.0.0 -b html ./docs/source/ ./docs/build/html
