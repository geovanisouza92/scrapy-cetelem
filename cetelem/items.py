#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=F0401,C0301

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class CetelemItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    limite = scrapy.Field()
    super_limite = scrapy.Field()
    parcelamento = scrapy.Field()
    mes_atual = scrapy.Field()
    subtotal_atual = scrapy.Field()
    mes_proximo = scrapy.Field()
    subtotal_proximo = scrapy.Field()

    def __setitem__(self, key, value):  # pylint: disable=E1002
        value = ''.join(item.strip() for item in value.extract())
        super(CetelemItem, self).__setitem__(key, value)
