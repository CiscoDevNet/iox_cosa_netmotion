FROM golang:alpine

RUN apk update && apk add curl git

RUN go get golang.org/x/sys/unix && go get golang.org/x/crypto/ssh && go get gopkg.in/ini.v1

