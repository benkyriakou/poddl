import os
import re
import requests
import argparse
from unidecode import unidecode
from xml.etree import ElementTree

parser = argparse.ArgumentParser(description='A basic RSS podcast downloading script')
parser.add_argument('--url', help='The RSS feed URL', required=True)
parser.add_argument('--summary', help='Show a summary of available episodes', action='store_true')
args = parser.parse_args()

r = requests.get(args.url)
rss_xml = ElementTree.fromstring(r.content)
items = rss_xml.findall('channel/item')
items.reverse()

for idx, item in enumerate(items, start=1):
    title = item.find('title').text
    ascii_title = re.sub(r'[^a-z0-9._\- ]', '', unidecode(title), flags=re.IGNORECASE)

    try:
        url = item.find('enclosure[@type="audio/mpeg"]').get('url')
    except AttributeError as e:
        print('Could not find a podcast URL for "{0}'.format(ascii_title))
        continue

    if args.summary:
        print('{0} ({1} of {2})'.format(ascii_title, idx, len(items)))
    else:
        destination = 'files/{0}.mp3'.format(ascii_title)
        print('Downloading "{0}" ({1} of {2})...'.format(ascii_title, idx, len(items)))

        if os.path.exists(destination):
            print('"{0}" already exists, skipping'.format(destination))
            continue

        r = requests.get(url)

        with open(destination, 'wb') as fh:
            fh.write(r.content)
