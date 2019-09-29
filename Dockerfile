FROM python:3.6
RUN mkdir /app
ADD . /app
WORKDIR /app
EXPOSE 5000
RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
CMD flask run -h 0.0.0.0 -p 5000
