import os
import re
import requests
import argparse
from pathlib import Path
from unidecode import unidecode
from xml.etree import ElementTree

BASEDIR = os.path.abspath(os.path.dirname(__file__))

parser = argparse.ArgumentParser(description='A basic RSS podcast downloading script')
parser.add_argument('--url', help='The RSS feed URL', required=True, type=str)
parser.add_argument('--summary', help='Show a summary of available episodes', action='store_true')
parser.add_argument('--destination', help='Directory to save podcast files to', default=os.path.join(BASEDIR, 'files'),
                    type=str)
parser.add_argument('--limit', help="Limit the number of items retrieved", type=int, default=-1)
args = parser.parse_args()

r = requests.get(args.url)
rss_xml = ElementTree.fromstring(r.content)
items = rss_xml.findall('channel/item')
items.reverse()

for idx, item in enumerate(items, start=1):
    if 0 < args.limit < idx:
        exit(0)

    ascii_title = re.sub(r'[^a-z0-9._\- ]', '', unidecode(item.find('title').text), flags=re.IGNORECASE)

    try:
        url = item.find('enclosure[@type="audio/mpeg"]').get('url')
    except AttributeError as e:
        print('Could not find a podcast URL for "{0}'.format(ascii_title))
        continue

    if args.summary:
        print('{0} ({1} of {2})'.format(ascii_title, idx, len(items)))
    else:
        destination = os.path.join(args.destination, '{0}.mp3'.format(ascii_title))

        if os.path.exists(destination):
            print('"{0}" already exists, skipping'.format(destination))
            continue
        else:
            try:
                Path(destination).touch()
            except FileNotFoundError as e:
                print('Unable to write to directory "{0}/"'.format(args.destination))
                exit(1)

        print('Downloading "{0}" ({1} of {2})...'.format(ascii_title, idx, len(items)))

        r = requests.get(url)

        with open(destination, 'wb') as fh:
            fh.write(r.content)
