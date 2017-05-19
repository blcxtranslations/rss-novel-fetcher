#!/usr/bin/python
# -*- coding: utf-8 -*-

from bulk.web_wuxiaworld import web_wuxiaworld
from bulk.web_fanfiction import web_fanfiction


def ask_for_index(str, end, start=1):
  selection = -1
  while selection < start or selection > end:
    selection = raw_input(str)
    if len(selection) == 0:
      return None
    selection = int(selection)
  return selection - 1

def fetch():
  selection = ask_for_index('1 for wuxiaworld, 2 for fanfictionnet : ', 2)
  if selection == 0:
    return web_wuxiaworld()
  else:
    return web_fanfiction()
