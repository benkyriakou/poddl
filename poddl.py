import os
import re
import requests
import argparse
from lxml import etree
from unidecode import unidecode

parser = argparse.ArgumentParser(description='A basic RSS podcast downloading script')
parser.add_argument('--url', help='The RSS feed URL', required=True)
args = parser.parse_args()

r = requests.get(args.url)
rss_xml = etree.fromstring(r.content)
items = rss_xml.xpath('/rss/channel/item')
items.reverse()

for idx, item in enumerate(items, start=1):
    title = item.find('title').text
    ascii_title = re.sub(r'[^a-z0-9._\- ]', '', unidecode(title), flags=re.IGNORECASE)
    url = item.find('enclosure').get('url')
    destination = 'files/{0}.mp3'.format(ascii_title)

    print('Downloading "{0}" ({1} of {2})...'.format(ascii_title, idx, len(items)))

    if os.path.exists(destination):
        print('"{0}" already exists, skipping'.format(destination))
        continue

    r = requests.get(url)

    with open(destination, 'wb') as fh:
        fh.write(r.content)
