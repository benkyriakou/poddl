# poddl

A basic podcast-downloading tool.

## Installation

Install via `pip`:

```
pip install poddl
```

## CLI

poddl makes itself available as a CLI utility. For options, see `poddl --help`:

```
usage: poddl [-h] --url URL [--summary] [--destination DESTINATION]
             [--limit LIMIT]

A basic RSS podcast downloading script

optional arguments:
  -h, --help            show this help message and exit
  --url URL             The RSS feed URL
  --summary             Show a summary of available episodes
  --destination DESTINATION
                        Directory to save podcast files to
  --limit LIMIT         Limit the number of items retrieved
```

By default, podcasts are downloaded to `~/Downloads/poddl`.

## Library

To use as a library, include `poddl.get`:

```python3
from poddl import get

get('https://example.com/rss')
```

By default episodes are downloaded to `~/Downloads/poddl`. To change this, set the destination:

```python3
from poddl import get

get('https://example.com/rss', destination='~/Documents/podcasts')
```

You can get a listing of the available podcasts without downloading them using `summary`:

```python3
from poddl import get

get('https://example.com/rss', summary=True)
```

And you can limit them number retrieved with `limit`:

```python3
from poddl import get

get('https://example.com/rss', summary=True, limit=20)
```