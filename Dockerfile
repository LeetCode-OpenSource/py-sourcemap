FROM ubuntu:18.04

ARG PYTHON_VERSION=3.6

ENV RUSTUP_HOME=/usr/local/rustup \
    CARGO_HOME=/usr/local/cargo \
    PATH=/usr/local/cargo/bin:$PATH \
    RUST_VERSION=nightly

RUN apt-get update && \
    echo $PYTHON_VERSION && \
    apt-get install software-properties-common -y --no-install-recommends && \
    add-apt-repository ppa:deadsnakes/ppa -y && \
    apt-get install python${PYTHON_VERSION} wget build-essential git curl -y --no-install-recommends && \
    apt-get upgrade -y && \
    apt-get autoremove -y && \
    ln -sf /usr/bin/python${PYTHON_VERSION} /usr/bin/python && \
    if [ $PYTHON_VERSION = '3.6' ]; \
    then \
      apt-get install python3-pip -y --no-install-recommends && \
      ln -sf /usr/bin/pip3 /usr/bin/pip; \
    else \
      curl https://bootstrap.pypa.io/get-pip.py | python${PYTHON_VERSION}; \
    fi && \
    pip install --upgrade pip

RUN set -eux; \
    dpkgArch="$(dpkg --print-architecture)"; \
    case "${dpkgArch##*-}" in \
        amd64) rustArch='x86_64-unknown-linux-gnu'; rustupSha256='f69dafcca62fe70d7882113e21bb96a2cbdf4fc4636d25337d6de9191bdec8da' ;; \
        armhf) rustArch='armv7-unknown-linux-gnueabihf'; rustupSha256='eee969b9fd128e8dc9b4ec44acde46735cf8e612d06495e9d022517849aba2d6' ;; \
        arm64) rustArch='aarch64-unknown-linux-gnu'; rustupSha256='cdc48b7882582fd8475107a406dd86df85c7d72e5deea99ff8940c8e11531285' ;; \
        i386) rustArch='i686-unknown-linux-gnu'; rustupSha256='3bad3945452509ac28ba4113e198323daab57488d6885bb31ac30c9eecd88825' ;; \
        *) echo >&2 "unsupported architecture: ${dpkgArch}"; exit 1 ;; \
    esac; \
    url="https://static.rust-lang.org/rustup/archive/1.13.0/${rustArch}/rustup-init"; \
    wget "$url"; \
    echo "${rustupSha256} *rustup-init" | sha256sum -c -; \
    chmod +x rustup-init; \
    ./rustup-init -y --no-modify-path --default-toolchain $RUST_VERSION; \
    rm rustup-init; \
    chmod -R a+w $RUSTUP_HOME $CARGO_HOME; \
    rustup default nightly && \
    rustup --version; \
    cargo --version; \
    rustc --version; \
    python -V; \
    pip -V;
