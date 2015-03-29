import urlparse
import BaseHTTPServer

import re
from string import find, replace, strip, lower, join

'''
def stripsite(url):
    "Take a URL and return (host, document)"
    url = urlparse.urlparse(url)
    return url[1], urlparse.urlunparse( (0,0,url[2],url[3],url[4],url[5]) )

def base_host(host):
    "Given HOST, return the top level domain: abc.XYZ or abc.def.XY"
    parts = split(host, '.')
    if len(parts[-1]) == 3: parts = parts[-2:]
    elif len(parts[-1]) == 2: parts = parts[-3:]
    return join(parts, '.')
        
def shorten_url(url, length):
    "Given a URL, shorten the middle portion of it so that it is LENGTH long"
    if url[:1] == '/': url = url[1:]
    site, doc = stripsite('http://'+url)
    if doc[:1]=='/': site, doc = site+'/', doc[1:]
    i = len(site)
    if i >= length: return site[:length]
    elif i+len(doc) < length: return site+doc
    else:
        # This is the complicated case, where we remove the middle
        j = find(doc, '?')+1 # note the +1, so failures are 0
        if j == 0: return site+'...'+doc[-(length-i-3):]
        elif i+j < length: return site+doc[:(length-i-3)]+'...'
        else: return site+'...'+doc[-(length-i-j-6):j]+'...'

'''

def glob_to_regex(a):
    "Given a glob EXPR (with *, like shell patterns), turn it into a regexp"
    a = replace(a, '.','[.]')
    a = replace(a, '$', '[$]')
    a = replace(a, '|','[|]')
    a = replace(a, '(?', '(#####') # re extension, save (?...)
    a = replace(a, '?','[?]')      # replace ?
    a = replace(a, '(#####', '(?') # put back in (?...)
    a = replace(a, '*','.*')
    a = '^' + a + '$'
    return re.compile(a)

def regex_to_glob(r):
    "Given a REGEXP, try to turn it into a glob expression"
    r = replace(r, '.*', '*')
    r = replace(r, '[.]', '.')
    r = replace(r, '[?]', '?')
    if r[0] == '^': r = r[1:]
    if r[-1] == '$': r = r[:-1]
    return r

'''

def html_output(file, data, code=200, moreheaders=[]):
    response = BaseHTTPServer.BaseHTTPRequestHandler.responses[code][0]
    file.write("HTTP/1.0 %s %s\r\n" % (code, response))
    file.write("Server: MURI Python Proxy\r\n")
    file.write("Content-type: text/html\r\n")
    file.write("Content-length: "+`len(data)`+'\r\n')
    for h in moreheaders:
        file.write(h)
        file.write("\r\n")
    file.write("\r\n")
    file.write(data+"\r\n")
    file.close()

def set_header(header, key, value):
    h = header.headers
    for i in range(len(h)):
        if lower(h[i][:len(key)]) == lower(key):
            h[i] = h[i][:len(key)] + ' ' + value + '\r\n'
            return
    raise KeyError

def header_rewrite(headers, name, value):
    "Rewrite name: X to name: value  or name: value(X) if value not a string"
    new_headers = []
    altered = 0
    for h in headers:
        i = find(h, ':')
        if i >= 0:
            n = h[:i]
            if lower(n) == lower(name): 
                if type(value)==type(''): v = value
                else: v = value(strip(h[i+1:]))
                if v: h = '%s: %s\r\n' % (n, v)
                else: h = ''
                altered = 1
        if h: new_headers.append(h)
    if not altered:
        if type(value)==type(''): v = value
        else: v = value('')
        if v: new_headers.append('%s: %s\r\n' % (name, v))
    return new_headers

def remove_pattern(text, start_pat, end_pat, replacement=''):
    # This does NOT remove regular expressions!  It is case sensitive.
    while 1:
        i = find(text, start_pat)
        if i < 0: return text
        j = find(text, end_pat, i)
        if j < 0: return text

        # Remove the section from i to j
        text = join([text[:i], replacement, text[j+len(end_pat):]], '')
'''
