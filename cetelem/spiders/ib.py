#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=C0301,F0401,W0612,R0201,W0613

from __future__ import print_function

import urlparse
import scrapy

from cetelem import items as cetitems


class IbSpider(scrapy.Spider):
    name = 'ib'
    allowed_domains = ['cetelem.com.br']
    start_urls = (
        'http://www.cetelem.com.br/wps/portal/cetelem/normal/NL/login',
    )

    def parse(self, response):
        # Get the values of each button (mixed values, understood by server)
        buttons = {
            str(i): response.selector.xpath('//*[@name=%d]/@onclick' % i).re(r'(?:_preencheSenha\()(?P<val>\d+)')[0]
            for i in xrange(9)
        }

        # Get form name and build form data
        formname = response.selector.xpath("//*[re:test(@id, 'PC_.*_LoginForm')]/@name").extract()[0]
        formdata = {
            'userid': self.settings.get('USERID'),
            'password': ''.join(buttons[c] for c in self.settings.get('PASSWORD')),
        }
        item = cetitems.CetelemItem()

        # Build the next request body
        req = scrapy.FormRequest.from_response(
            response=response,
            formdata=formdata,
            formname=formname,
            dont_click=True,
            callback=self.parse_limits)
        req.meta['item'] = item

        yield req

    def parse_limits(self, response):
        item = response.meta['item']

        # Get limits
        item['limite'] = response.selector.xpath('//*[@id="dadosCartaoInternetBanking"]/span[5]/text()')
        item['super_limite'] = response.selector.xpath('//*[@id="dadosCartaoInternetBanking"]/span[7]/text()')
        item['parcelamento'] = response.selector.xpath('//*[@id="dadosCartaoInternetBanking"]/span[11]/text()')

        # Get bill link
        consulta = response.selector.xpath('//a[contains(text(), "Consulte sua fatura")]/@href').extract()[0]

        # Go to bill listing
        req = scrapy.Request(
            urlparse.urljoin(response.url, consulta),
            callback=self.parse_actual_bill)
        req.meta['item'] = item

        yield req

    def parse_actual_bill(self, response):
        item = response.meta['item']

        # Get actual bill
        item['mes_atual'] = response.selector.xpath('//*[@id="abasFatura"]/table/tr/td[2]/a/text()')
        item['subtotal_atual'] = response.selector.xpath('//*[@id="boxFatura"]/table/tr[2]/td/strong/text()')
        item['mes_proximo'] = response.selector.xpath('//*[@id="abasFatura"]/table/tr/td[3]/a/text()')

        # Get next bill form name and data
        formname = response.selector.xpath("//*[re:test(@id, '.*_frmFatura')]/@name").extract()[0]
        formdata = {'tipoFatura': '0'}

        # Go to next bill
        req = scrapy.FormRequest.from_response(
            response=response,
            formname=formname,
            formdata=formdata,
            dont_click=True,
            callback=self.parse_next_bill)
        req.meta['item'] = item

        yield req

    def parse_next_bill(self, response):
        item = response.meta['item']

        # Get next bill information
        # item['mes_proximo'] = response.selector.xpath('//*[@id="boxFatura"]/table/tr[3]/td/div/strong/text()')
        item['subtotal_proximo'] = response.selector.xpath('//*[@id="boxFatura"]/table/tr[3]/td/div/text()')

        # Return item
        yield item
