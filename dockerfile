#Alpine based image for python 3.11.5
FROM python:3.11.5-alpine

#Copy the requirements.txt file and all the files
COPY ./Game /Game
COPY ./requirements.txt /requirements.txt

#Working directory for installation
WORKDIR /

#Install the requirements
RUN pip install -r requirements.txt

#Set the working directory
WORKDIR /Game

#Tail for infinite loop
#CMD tail -f /dev/null

CMD [ "python", "Main.py", "200000"]