FROM python:2.7

WORKDIR /app

ADD requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

ADD scrapy.cfg /app/scrapy.cfg
ADD cetelem/ /app/cetelem

CMD ["scrapy", "crawl", "ib"]
