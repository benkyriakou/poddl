import os
import re
import sys
import logging
import requests
from pathlib import Path
from unidecode import unidecode
from xml.etree import ElementTree

logger = logging.getLogger('poddl')


def get(url, destination, limit=-1, summary=False):
    destination = os.path.expanduser(destination)

    try:
        r = requests.get(url)
    except requests.exceptions.RequestException:
        sys.exit('Unable to retrieve content from RSS feed "{0}"'.format(url))

    try:
        rss_xml = ElementTree.fromstring(r.content)
    except ElementTree.ParseError:
        sys.exit('Unable to parse URL contents as XML')

    items = rss_xml.findall('channel/item')
    items.reverse()

    try:
        os.mkdir(destination)
    except (PermissionError, FileNotFoundError):
        logger.error('Could not create directory "{0}/"'.format(destination))
        sys.exit(1)
    except FileExistsError:
        pass

    if not summary:
        logger.info('Downloading files to "{0}"...'.format(destination))
    
    for idx, item in enumerate(items, start=1):
        if 0 < limit < idx:
            logger.info('Stopped at limit "{0}"'.format(limit))
            sys.exit(0)
    
        ascii_title = re.sub(r'[^a-z0-9._\- ]', '', unidecode(item.find('title').text), flags=re.IGNORECASE)
    
        try:
            episode_url = item.find('enclosure[@type="audio/mpeg"]').get('url')
        except AttributeError as e:
            logger.warning('Could not find a podcast URL for "{0}'.format(ascii_title))
            continue
    
        if summary:
            logger.info('{0} ({1} of {2})'.format(ascii_title, idx, len(items)))
        else:
            destination_path = os.path.join(destination, '{0}.mp3'.format(ascii_title))
    
            if os.path.exists(destination_path):
                logger.info('"{0}" already exists, skipping'.format(destination_path))
                continue
            else:
                try:
                    Path(destination_path).touch()
                except FileNotFoundError:
                    sys.exit('Unable to write to directory "{0}/"'.format(destination))
    
            logger.info('Downloading "{0}" ({1} of {2})...'.format(ascii_title, idx, len(items)))

            try:
                r = requests.get(episode_url)

                with open(destination_path, 'wb') as fh:
                    fh.write(r.content)
            except requests.exceptions.RequestException:
                sys.exit('Error retrieving episode from "{0}"'.format(episode_url))
