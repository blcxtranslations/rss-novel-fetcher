#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib2
import re


def get_page(url):
  req = urllib2.Request(url , headers={'User-Agent': 'Magic Browser'})
  return urllib2.urlopen(req).read()

def find_links(link_url):
  soup = BeautifulSoup(get_page(link_url), "lxml")
  article = soup.find('article')
  links = [a['href'] for a in article.findAll('a')]
  links = filter(lambda link: 'www.wuxiaworld.com' in link and 'index' in link and 'chapter' in link, links)
  links = list(set(links))
  return links

def sort_links(links):
  new_links = []
  for link in links:
    slink = re.split('-|/', link)
    chapter = [int(str(s)) for s in slink if s.isdigit()]
    order = chapter[0]
    new_links.append([order, link])
  new_links.sort(key=lambda x: x[0])
  return new_links

def stripunicode(text):
    return ''.join(i for i in text if ord(i)<128).strip()

def find_novels():
  main_url = 'http://www.wuxiaworld.com/'
  main_page = get_page(main_url)
  soup = BeautifulSoup(main_page, 'lxml')
  items = soup.find('nav').findAll('a')
  items = filter(lambda item: 'index' in item['href'], items)
  links = []
  for item in items:
    title = str(stripunicode(item.text)).replace(' ()', '')
    link = item['href']
    links.append([title, link])
  links.sort(key=lambda x: x[0])
  return links

def get_length(url):
  return 100

def get_chapters(url, lower=None, upper=None):
  links = find_links(url)
  links = sort_links(links)
  if not lower is None:
    links = filter(lambda link: int(link[0]) >= lower, links)
  if not upper is None:
    links = filter(lambda link: int(link[0]) <= upper, links)
  links = [link[1] for link in links]
  return links

def ask_for_index(str, end, start=1):
  selection = -1
  while selection < start or selection > end:
    selection = raw_input(str)
    if len(selection) == 0:
      return None
    selection = int(selection)
  return selection - 1

def web_wuxiaworld():
  novels = find_novels()
  for i, novel in enumerate(novels):
    print i + 1, '\t:\t', novel[0]

  selection = -1
  while selection < 1 or selection > len(novels):
    selection = int(raw_input("Select a novel: "))
  selection -= 1

  chapters = get_chapters(novels[selection][1])
  print "There are %s chapters in %s" % (len(chapters), novels[selection][0])
  lower = ask_for_index("Start from chapter: ", len(chapters))
  upper = ask_for_index("End at chapter: ", len(chapters))
  chapters = chapters[lower:upper]
  return chapters
