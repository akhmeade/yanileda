#encoding: utf-8
from urllib.parse import urlparse

def create_url(url, name=None):
    if name is None:
        name = url
    return '<a href="' + url + '">' + name + '</a>'

def is_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False