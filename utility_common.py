#!/usr/bin/python
# -*- coding: utf-8 -*-

from api_instapaper import send_instapaper
from lxml import html
import urllib2


def strip_unicode(text):
    return ''.join(i for i in text if ord(i)<128).strip()

def get_page(url):
  req = urllib2.Request(url , headers={'User-Agent': 'Magic Browser'})
  req = urllib2.urlopen(req)
  page = req.read()
  req.close()
  return page

def find_links(link_url, includes, excludes=[]):
  page = get_page(link_url)
  tree = html.fromstring(page)
  links = tree.xpath('//a/@href')
  for include in includes:
    links = filter(lambda link: include in link, links)
  for exclude in excludes:
    links = filter(lambda link: exclude not in link, links)
  links = list(set(links))
  return links

def send_links(links, service):
  if service['name'] == 'Instapaper':
    send_instapaper(links, service)