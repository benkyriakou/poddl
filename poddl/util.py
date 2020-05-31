import sys
import poddl
import argparse
import logging


def main():
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(message)s'))
    handler.setLevel(logging.INFO)
    logger = logging.getLogger('poddl')
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    parser = argparse.ArgumentParser(description='A basic RSS podcast downloading script')
    parser.add_argument('--url', help='The RSS feed URL', required=True, type=str)
    parser.add_argument('--summary', help='Show a summary of available episodes', action='store_true')
    parser.add_argument('--destination', help='Directory to save podcast files to', default='~/Downloads/poddl',
                        type=str)
    parser.add_argument('--limit', help="Limit the number of items retrieved", type=int, default=-1)
    args = parser.parse_args()

    try:
        poddl.get(args.url, args.destination, limit=args.limit, summary=args.summary)
    except poddl.exceptions.PoddlException as e:
        sys.exit(e)
    except Exception as e:
        sys.exit('Unexpected exception: {0}'.format(e))
