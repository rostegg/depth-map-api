FROM python:3

WORKDIR /usr/src/depth-generator-api

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN ./get_models_monodepth.sh

EXPOSE 5000

CMD [ "python", "./run.py" ]