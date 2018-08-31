FROM golang:alpine as build

RUN apk update && apk add curl git

RUN go get golang.org/x/sys/unix \
    && go get golang.org/x/crypto/ssh \
    && go get gopkg.in/ini.v1 \
    && go get github.com/julienschmidt/httprouter

WORKDIR /go/src/github.com

COPY ./iox-go ./iox-go

WORKDIR /go/src/github.com/iox-go

RUN go build -o gw_server gw_server.go

FROM alpine

COPY --from=build /go/src/github.com/iox-go/gw_server .
COPY ./iox-go/package_config.ini .

EXPOSE 8080

CMD ["./gw_server"]



