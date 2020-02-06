FROM python:3-alpine
RUN pip install --upgrade pip
LABEL maintainer="ankit256@gmail.com"
RUN ["mkdir", "/docker_practice_directory"]
WORKDIR /docker_practice_directory
COPY ./ /docker_practice_directory
RUN pip install -r requirements.txt
EXPOSE 4000
CMD ["python", "./dockerp.py"]
