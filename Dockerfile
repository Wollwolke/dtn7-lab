ARG ARCH=

FROM ${ARCH}rust:1.62.1 as builder
WORKDIR /root
RUN rustup component add rustfmt
RUN git clone https://github.com/dtn7/dtn7-rs  && cd dtn7-rs && \
    # git checkout 0bb1fa3 && \
    cargo install --locked --bins --examples --root /usr/local --path examples && \
    cargo install --locked --bins --examples --root /usr/local --path core/dtn7
# RUN cargo install --locked --bins --examples --root /usr/local dtn7-plus --git https://github.com/dtn7/dtn7-plus-rs  --rev 010202e56 dtn7-plus
RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    apt-get install -y libpango1.0-dev libatk1.0-dev libsoup2.4-dev libwebkit2gtk-4.0-dev cmake && \
    rm -rf /var/lib/apt/lists/*
RUN cargo install --bins --examples --root /usr/local --git https://github.com/gh0st42/coreemu-rs --rev 326a6f7
# RUN git clone https://github.com/stg-tud/dtn-dwd && cd dtn-dwd && \
#     git checkout b78e241 && \
#     cargo install --root /usr/local --path backend/ && \
#     cargo install --root /usr/local --path client/
# RUN git clone https://github.com/gh0st42/dtnchat && cd dtnchat && \
#     git checkout 93f1450 && \
#     cargo install --bins --examples --root /usr/local --path .


FROM ${ARCH}golang:1.19 as gobuilder

ARG wtfversion=v0.41.0

RUN git clone https://github.com/wtfutil/wtf.git $GOPATH/src/github.com/wtfutil/wtf && \
    cd $GOPATH/src/github.com/wtfutil/wtf && \
    git checkout $wtfversion

ENV GOPROXY=https://proxy.golang.org,direct
ENV GO111MODULE=on
ENV GOSUMDB=off

WORKDIR $GOPATH/src/github.com/wtfutil/wtf

ENV PATH=$PATH:./bin

RUN make build && \
    cp bin/wtfutil /usr/local/bin/


FROM ${ARCH}gh0st42/coreemu-lab:1.0.0

# install stuff for vnc session

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && \
    apt-get install -y lxde-core lxterminal \
    tightvncserver autocutsel wmctrl xterm \
    gstreamer1.0-plugins-bad gstreamer1.0-libav gstreamer1.0-gl \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/local/bin/* /usr/local/bin/

COPY --from=gobuilder /usr/local/bin/* /usr/local/bin/

RUN touch /root/.Xresources
RUN touch /root/.Xauthority
WORKDIR /root
RUN mkdir .vnc Desktop
COPY configs/Xdefaults /root/.Xdefaults
COPY scripts/dtn7-* /usr/local/bin/

RUN mkdir -p /root/.core/myservices && mkdir -p /root/.coregui/custom_services && mkdir -p /root/.coregui/icons
COPY core_services/* /root/.core/myservices/
COPY coregui/config.yaml /root/.coregui/
COPY coregui/icons/* /root/.coregui/icons/
COPY configs/dtn7.yml /root/


# COPY xstartup with start for lxde
COPY configs/xstartup /root/.vnc/
COPY scripts/coreemu.sh /root/Desktop
COPY scripts/entrypoint.sh /entrypoint.sh

RUN echo "export USER=root" >> /root/.bashrc
ENV USER root
RUN printf "sneakers\nsneakers\nn\n" | vncpasswd

EXPOSE 22
EXPOSE 5901
EXPOSE 50051
ENTRYPOINT [ "/entrypoint.sh" ]
WORKDIR /root
