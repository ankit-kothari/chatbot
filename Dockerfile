FROM python:3.7.3
LABEL maintainer="ankit256@gmail.com"
RUN ["mkdir", "/docker_practice_directory"]
WORKDIR /docker_practice_directory
COPY ./ /docker_practice_directory
RUN pip install -r requirements.txt
CMD ["python", "./dockerp.py"]