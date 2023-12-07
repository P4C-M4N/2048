#Alpine based image for python 3.11.5
FROM python:3.11.5-alpine
COPY ./Game /Game
WORKDIR /Game
#Tail for infinite loop
CMD tail -f /dev/null