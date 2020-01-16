#encoding: utf-8

def create_url(url, name=None):
    if name is None:
        name = url
    return '<a href="' + url + '">' + name + '</a>'
