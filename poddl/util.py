import poddl
import argparse


def main():
    parser = argparse.ArgumentParser(description='A basic RSS podcast downloading script')
    parser.add_argument('--url', help='The RSS feed URL', required=True, type=str)
    parser.add_argument('--summary', help='Show a summary of available episodes', action='store_true')
    parser.add_argument('--destination', help='Directory to save podcast files to', default='~/Downloads/poddl',
                        type=str)
    parser.add_argument('--limit', help="Limit the number of items retrieved", type=int, default=-1)
    args = parser.parse_args()

    poddl.get(args.url, args.destination, limit=args.limit, summary=args.summary)
