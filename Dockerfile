FROM ubuntu:18.04

RUN apt-get -qq update && apt-get -q install -y \
    git curl \
    libffi-dev libldap2-dev libsasl2-dev libssl-dev \
    python3-dev python3-pip python-virtualenv

ADD . /st2docs
WORKDIR /st2docs
RUN make .cleandocs && make docs

EXPOSE 8000

CMD make .livedocs

#CMD  . ./virtualenv/bin/activate; \
#    sphinx-autobuild -H 0.0.0.0 -b html ./docs/source/ ./docs/build/html
