FROM ubuntu:16.04

ENV GHR_VERSION="0.9.0"

ARG PYTHON_VERSION=3.6

ENV RUSTUP_HOME=/usr/local/rustup \
    CARGO_HOME=/usr/local/cargo \
    PATH=/usr/local/cargo/bin:$PATH \
    RUST_VERSION=1.28.0

RUN apt-get update && \
    apt-get install software-properties-common python-software-properties -y && \
    add-apt-repository ppa:deadsnakes/ppa -y && \
    apt-get update && \
    apt-get install python${PYTHON_VERSION} python3-pip wget git curl -y && \
    apt-get upgrade -y && \
    apt-get autoremove -y && \
    ln -sf /usr/bin/python${PYTHON_VERSION} /usr/bin/python && \
    curl -fSL -o ghr.tar.gz "https://github.com/tcnksm/ghr/releases/download/v${GHR_VERSION}/ghr_v${GHR_VERSION}_linux_amd64.tar.gz" && \
    tar -xvzf ghr.tar.gz && \
    mv ghr_v0.9.0_linux_amd64/ghr /usr/local/bin && \
    chown root:root /usr/local/bin/ghr && \
    rm -r \
        ghr.tar.gz \
        ghr_v0.9.0_linux_amd64

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
    rustc --version;
