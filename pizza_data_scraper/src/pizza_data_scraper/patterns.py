"""Regex patterns for pizza data scraping."""

import re


# Pattern A: JavaScript style  →  lat: 40.8283749
PAT_JS = re.compile(
    r'\blat\s*:\s*(?P<lat>-?\d+\.\d+).*?'   # lat: ...
    r'\blng\s*:\s*(?P<lng>-?\d+\.\d+)',      # lng: ...
    re.DOTALL
)

# Pattern B: JSON style  →  "lat":40.831131,"lng":14.2258326
PAT_JSON = re.compile(
    r'"lat"\s*:\s*(?P<lat>-?\d+\.\d+).*?'
    r'"lng"\s*:\s*(?P<lng>-?\d+\.\d+)',
    re.DOTALL
)

# The generic fallback: bare  lat=40.8  or  latitude:40.8  etc.
PAT_FALLBACK = re.compile(
    r'lat(?:itude)?\s*[=:]\s*(?P<lat>-?\d+\.\d+).*?'
    r'l(?:ng|on)(?:gitude)?\s*[=:]\s*(?P<lng>-?\d+\.\d+)',
    re.DOTALL | re.IGNORECASE
)