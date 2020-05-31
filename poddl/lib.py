import os
import re
import requests
from pathlib import Path
from unidecode import unidecode
from xml.etree import ElementTree


def get(url, destination, limit=-1, summary=False):
    r = requests.get(url)
    rss_xml = ElementTree.fromstring(r.content)
    items = rss_xml.findall('channel/item')
    items.reverse()
    
    for idx, item in enumerate(items, start=1):
        if 0 < limit < idx:
            exit(0)
    
        ascii_title = re.sub(r'[^a-z0-9._\- ]', '', unidecode(item.find('title').text), flags=re.IGNORECASE)
    
        try:
            url = item.find('enclosure[@type="audio/mpeg"]').get('url')
        except AttributeError as e:
            print('Could not find a podcast URL for "{0}'.format(ascii_title))
            continue
    
        if summary:
            print('{0} ({1} of {2})'.format(ascii_title, idx, len(items)))
        else:
            destination = os.path.join(destination, '{0}.mp3'.format(ascii_title))
    
            if os.path.exists(destination):
                print('"{0}" already exists, skipping'.format(destination))
                continue
            else:
                try:
                    Path(destination).touch()
                except FileNotFoundError as e:
                    print('Unable to write to directory "{0}/"'.format(destination))
                    exit(1)
    
            print('Downloading "{0}" ({1} of {2})...'.format(ascii_title, idx, len(items)))
    
            r = requests.get(url)
    
            with open(destination, 'wb') as fh:
                fh.write(r.content)
