#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=W0613,R0201,F0401

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from __future__ import print_function

from pushbullet import Pushbullet
from scrapy import log
from scrapy.exceptions import DropItem


TEMPLATE = u'''
Limite: %(limite)s
Super limite: %(super_limite)s
Parcelamento: %(parcelamento)s
Fatura do mês %(mes_atual)s: %(subtotal_atual)s
Fatura do mês %(mes_proximo)s: %(subtotal_proximo)s
'''


class CetelemPipeline(object):

    def process_item(self, item, spider):
        return item


class PushbulletPipeline(object):

    @classmethod
    def from_crawler(cls, crawler):
        return cls(pb_key=crawler.settings.get('PUSHBULLET_APIKEY'))

    def __init__(self, pb_key):
        super(PushbulletPipeline, self).__init__()
        self.pb = Pushbullet(pb_key)  # pylint: disable=C0103

    def process_item(self, item, spider):
        content = TEMPLATE % item
        spider.log(content)

        try:
            self.pb.push_note('Resumo da fatura Submarino', content)
        except Exception as exc:
            print(exc)
            spider.log(exc, level=log.ERROR)
            raise DropItem()

        return item
