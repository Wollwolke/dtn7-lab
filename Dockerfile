ARG ARCH=

FROM ${ARCH}rust:1.62.1 as builder
WORKDIR /root
RUN rustup component add rustfmt
RUN git clone https://github.com/dtn7/dtn7-rs  && cd dtn7-rs && \
    cargo install --locked --bins --examples --root /usr/local --path examples && \
    cargo install --locked --bins --examples --root /usr/local --path core/dtn7


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


FROM ${ARCH}gh0st42/coreemu-lab

COPY --from=builder /usr/local/bin/* /usr/local/bin/

COPY --from=gobuilder /usr/local/bin/* /usr/local/bin/

# unnecessary?
RUN touch /root/.Xresources
RUN touch /root/.Xauthority

WORKDIR /root
COPY scripts/dtn7-* /usr/local/bin/

RUN mkdir -p /root/.core/myservices && mkdir -p /root/.coregui/custom_services && mkdir -p /root/.coregui/icons
COPY core_services/* /root/.core/myservices/
COPY coregui/config.yaml /root/.coregui/
COPY coregui/icons/* /root/.coregui/icons/
COPY configs/dtn7.yml /root/


COPY scripts/entrypoint.sh /entrypoint.sh

EXPOSE 22
EXPOSE 50051

WORKDIR /shared

ENTRYPOINT [ "/entrypoint.sh" ]
