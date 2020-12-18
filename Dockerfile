FROM python:3.8
WORKDIR /usr/src/app
COPY ./requirements.txt ./requirements.txt
COPY ./greek_cnn.py ./
COPY ./api.py ./
COPY ./dataset_hasy.py ./
COPY ./hasy.h5 ./
COPY ./dataset/HASYv2/symbols.csv ./dataset/HASYv2/
RUN ["pip", "install", "-r", "requirements.txt"]
RUN ["apt-get", "update"]
RUN ["apt-get", "install", "-y", "libgl1-mesa-dev"]
EXPOSE 5000
CMD ["python", "api.py"]
