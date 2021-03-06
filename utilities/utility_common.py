#!/usr/bin/python
# -*- coding: utf-8 -*-


def ask_for_index(string, end, start=1):
    selection = -1
    while selection < start or selection > end:
        selection = raw_input(string)
        if len(selection) == 0:
            return None
        selection = int(selection)
    return selection - 1

def strip_unicode(text):
    return ''.join(i for i in text if ord(i) < 128).strip()

def get_page(url, mercury_api=None, backoff=0):
    import urllib2

    headers = {'User-Agent': 'Magic Browser'}
    if mercury_api:
        headers['Content-Type'] = 'application/json'
        headers['x-api-key'] = mercury_api
    req = urllib2.Request(url, headers=headers)
    try:
        req = urllib2.urlopen(req)
        page = req.read()
        req.close()
        return page
    except urllib2.HTTPError as err:
        if err.code == 500:
            print_colour('urllib2', 'Failed', "Getting the webpage failed", 'error')
            if backoff == 3:
                raise
            print_colour('urllib2', 'Failed', "Retry number " + str(backoff), 'error')
            import time
            time.sleep(60 * pow(2, backoff))
            return get_page(url, mercury_api, backoff + 1)
    except:
        raise

def find_links(link_url, includes, excludes=[]):
    from lxml import html

    page = get_page(link_url)
    tree = html.fromstring(page)
    links = tree.xpath('//a/@href')
    for include in includes:
        links = [link for link in links if include in link]
    for exclude in excludes:
        links = [link for link in links if exclude not in link]
    links = list(set(links))
    return links

def send_link(reader, service, link, folder_id, mercury_api):
    if reader == 'Instapaper':
        from readers.instapaper import send_instapaper
        return send_instapaper(service, link, folder_id, mercury_api)

def print_colour(service, status, message, level=''):
    import datetime
    import time

    background = 43
    if level == 'success':
        background = 42
    elif level == 'error':
        background = 41
    elif level == 'info':
        background = 44

    totaltime = int(time.time() - time.mktime(time.localtime(0)))
    timestamp = str(datetime.datetime.fromtimestamp(totaltime))

    format_timestamp = ';'.join([str(5), str(30), str(45)])
    format_service = ';'.join([str(5), str(30), str(background)])

    text_timestamp = '{:19}'.format(timestamp)
    text_service = '{:10}'.format(service) + ': ' + '{:11}'.format(status)

    text_timestamp = '\x1b[%sm %s \x1b[0m' % (format_timestamp, text_timestamp)
    text_service = '\x1b[%sm %s \x1b[0m' % (format_service, text_service)
    print text_timestamp, text_service, message

def bulk_print(links):
    from backports.shutil_get_terminal_size import get_terminal_size

    (col, row) = get_terminal_size()
    row -= 1

    lines = []
    for i in xrange(row):
        lines.append('')

    zeroes = len(str(len(links)))

    longest = 0
    for link in links:
        if len(link) > longest:
            longest = len(link)

    size = longest + zeroes + 6 # four for spacer between links, 1 for the : and one for a space

    for i, link in enumerate(links):
        which = i % row
        line = ''
        if len(lines[which]) != 0:
            line += '    '
        line += '0' * (zeroes - len(str(i + 1)))
        line += str(i + 1)
        line += ': '
        line += link
        line += ' ' * (longest - len(link))
        lines[which] += line

    for line in lines:
        print line

def get_common_prefix_len(links):
    if len(links) == 0:
        return 0

    prefix = ''
    index = 0
    while True:
        index += 1
        prefix = links[0][:index]
        for link in links:
            if prefix not in link:
                if index > 0:
                    index -= 1
                return index
    return 0

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False

def check_if_all_number(nums):
    for n in nums:
        if not is_number(n):
            return False
    return True

def stringify_chapter_numbers(nums):
    l = 0
    for n in nums:
        if len(n) > l:
            l = len(n)
    new_nums = []
    for n in nums:
        new_num = ''
        new_num += '0' * (l - len(n))
        new_num += str(n)
        new_nums.append(new_num)
    return new_nums

def sort_links(links):
    import re

    new_links = []
    count = 0
    for link in links:
        slink = re.split('-|/', link)
        chapter = [int(str(s)) for s in slink if s.isdigit()]
        if len(chapter) < count:
            count = len(chapter)
        new_links.append([chapter, link])

    for i in xrange(count):
        new_links.sort(key=lambda x: x[0][count - 1 - i])

    new_links = [link[1] for link in new_links]
    return new_links
