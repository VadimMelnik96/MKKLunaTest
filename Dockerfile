FROM ubuntu:latest
LABEL authors="Vadim"

ENTRYPOINT ["top", "-b"]