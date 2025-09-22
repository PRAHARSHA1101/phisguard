# features.py
import re
import math
from urllib.parse import urlparse
from collections import Counter

SUSPICIOUS_TOKENS = {"login","secure","account","update","verify","webscr","bank","confirm","signin","password"}

def has_ip(host):
    return bool(re.match(r"^\d{1,3}(\.\d{1,3}){3}$", host))

def hostname_entropy(s):
    if not s: return 0.0
    counts = Counter(s)
    prob = [v/len(s) for v in counts.values()]
    return -sum(p * math.log2(p) for p in prob)

def extract_basic_features(url: str):
    parsed = urlparse(url if "://" in url else "http://" + url)
    host = parsed.hostname or ""
    path = parsed.path or ""
    query = parsed.query or ""
    url_full = url

    return {
        "url_len": len(url_full),
        "host_len": len(host),
        "path_len": len(path),
        "num_dots": host.count('.') + path.count('.'),
        "num_hyphens": url_full.count('-'),
        "num_digits": sum(c.isdigit() for c in url_full),
        "has_at": int('@' in url_full),
        "has_ip": int(has_ip(host)),
        "suspicious_tokens": sum((host+path+query).lower().count(tok) for tok in SUSPICIOUS_TOKENS),
        "host_entropy": hostname_entropy(host),
        "subdomain_count": max(0, host.count('.') - 1)
    }

