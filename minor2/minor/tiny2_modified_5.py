#!/usr/bin/python
from __future__ import division
from tiny_contentfilter import Blocker
from cacherep import replace
from datasize import cachesize
import BaseHTTPServer, select, socket, SocketServer, urlparse
import logging
import logging.handlers
import getopt
import sys
import os
from os import getenv
import signal
import threading
from types import FrameType, CodeType
from time import sleep
import ftplib

import pickle
import urllib2
import datetime
import email
import math

from StringIO import StringIO

log = logging.getLogger(__name__)





class CacheHandle(urllib2.BaseHandler,replace,cachesize):
       	"""
        Stores responses in a httplib2-style cache object.
        """



            

	###############################################################################
	total_http_requests=0
	found_in_cache=0
	not_found_in_cache=0
	hit=0
	miss=0
	###############################################################################

	
        def __init__(self, store):
                "construct a handler from a store"
                self.store = store

	#replace.__init__()

        def default_open(self, request):
		"""
                Open the url specified in the request. If it's an HTTP GET, and
                the result is a valid cached value, return the cached version.
                """

		####################################################################################
		CacheHandle.total_http_requests=CacheHandle.total_http_requests+1
		print "\ntotal HTTP requests"
		print CacheHandle.total_http_requests
		##################################################################################

		key = self._defrag_url(request.get_full_url())
                if request.get_method() not in ('GET', 'HEAD'):
                        # invalate this item if cached (RFC 2616 Section 13.10)

			##############################################################

			#CacheHandle.total_http_requests=CacheHandle.total_http_requests-1

			#############################################################



                        self.store.delete(str(hash(key)))
                if request.get_method() is not 'GET':
                        # defer to other handlers
                        return None


		
                
                self._convert_pragma(request.headers)

                # check the request cache-control header
                cc = self._parse_cache_control(request.headers)
                
                # check that the user-agent hasn't asked us to bypass the cache
                if 'no-cache' in cc:
                        return None
                                
                # get the cached response, or None if it's not found
                cached_resp = CachedResponse.load(self.store.get(str(hash(key))))
                if not cached_resp and 'only-if-cached' in cc:

##############################################################################################

			#CacheHandle.not_found_in_cache=CacheHandle.not_found_in_cache+1

################################################################################################

                        raise urllib2.HTTPError(request.get_full_url(), 504,
                                'content is not cached', hdrs=None, fp=None)


                
                if cached_resp and not cached_resp.fresh_for(request.headers):
                        log.debug('Request is stale')

#################################################################################################

			CacheHandle.not_found_in_cache=CacheHandle.not_found_in_cache+1
			#print "\nNot found in cache"
			#print CacheHandle.not_found_in_cache
##################################################################################################

                        self._add_stale_cache_request_headers(request, cached_resp)
                        cached_resp = None


###################################################################################################

		CacheHandle.found_in_cache=CacheHandle.found_in_cache+1
		#print "\nFound in cache"
		#print CacheHandle.found_in_cache
#################################################################################################		

		#CacheHandle.hit=float(CacheHandle.found_in_cache)/CacheHandle.total_http_requests
		CacheHandle.miss=float(CacheHandle.not_found_in_cache)/CacheHandle.total_http_requests
		CacheHandle.hit=1-CacheHandle.miss
		print "\n"
		print "\nhit ratio "
		print CacheHandle.hit
		print "\nmiss ratio "
		print CacheHandle.miss
		print "\n"

		with open("ratio.txt","a") as fp1:
			fp1.write(str(CacheHandle.hit)+'\t\t'+str(CacheHandle.miss)+'\n')
			fp1.close  




                return cached_resp

        @staticmethod
        def _add_stale_cache_request_headers(request, cached_resp):
                """
                The cached response is stale, so we need to re-validate it with
                the server. Add the `if-modified-since` and `if-none-match`
                headers to the request as appropriate.
                """

                if (
                        'last-modified' in cached_resp.headers and
                        not 'if-modified-since' in request.headers
                        ):
                        lm = cached_resp.headers['last-modified']
                        request.headers['if-modified-since'] = lm

                if (
                        'etag' in cached_resp.headers
                        #and not self.ignore_etag
                        and not 'if-none-match' in request.headers
                        ):
                        et = cached_resp.headers['etag']
                        request.headers['if-none-match'] = et

        def http_response(self, request, response):
                """
                Handle a HTTP response.
                """
                return self._update_cache(request, response)

        @staticmethod
        def _convert_pragma(headers):
                """
                convert "pragma: no-cache" to "cache-control: no-cache" in the
                request.
                """
                if (
                        'pragma' in headers
                        and 'no-cache' in headers['pragma'].lower()
                        and 'cache-control' not in headers
                        ):
                        headers['cache-control'] = 'no-cache'

        def _update_cache(self, request, response):
                """
                If it was a normal response (200 level) to
                a GET request, store it in the cache.
                """
                is_get = request.get_method() == 'GET'
                key = self._defrag_url(request.get_full_url())
                if is_get and response.code == 304:
                        # 304 - Not Modified, update the cached version
                        log.debug('304 received - updating headers')
                        new_headers = response.headers
                        response = CachedResponse.load(self.store.get(str(hash(key))))
                        response.update_headers(new_headers)
			self.updatedict()
			if(self.get_size())>429228:
##############		   
			   a=self.get_size()
				
			   while a>429228: 
				min1=min(self.userdata,key=self.userdata.get)
	 			del self.userdata[min1]
	 			#print '\n'
         			os.remove("home/kshama/Desktop/CD/minor/cache4/"+min1)
	 			print "min1 removed"
	 			#print '\n'
         
         			#print userdata
	 			#print len(userdata)

	 			a=self.get_size()
			 
######
                        self.store.set(str(hash(key)), response.save())
                        return response
                cached_response_codes = [200, 203]
                cacheable_response = response.code in cached_response_codes
                if not is_get or not cacheable_response: return response

                if self.should_cache(response):
                        response = CachedResponse(response)
			if(self.get_size())>429228:
##############		    
		            self.updatedict()
			    a=self.get_size()	
			    while a>429228: 
				min1=min(self.userdata,key=self.userdata.get)
	 			del self.userdata[min1]
	 			#print '\n'
				
         			os.remove("home/kshama/Desktop/CD/minor/cache4/"+min1)
	 			print "min1 removed"
	 			print '\n'
         
         			#print userdata
	 			#print len(userdata)

	 			a=self.get_size()
			 

######
                        self.store.set(str(hash(key)), response.save())
                return response

        def should_cache(self, response):
                if 'vary' in response.headers:
                        # for now, don't store requests that vary based on headers
                        return False
                already_cached = getattr(response, 'cached', False)
                if already_cached:
                        return False
                if 'range' in response.headers:
                        # we don't support caching ranged requests
                        return False
                return True

        @staticmethod
        def _defrag_url(url):
                main, sep, frag = url.partition('#')
                return main

        @staticmethod
        def _parse_cache_control(headers):
                
                def parse_part(part):
                        
                        name, sep, val = map(str.lower, map(str.strip,
                                part.partition('=')))
                        return name, (val or None)
                        
                cc_header = headers.get('cache-control', '')
                return dict(map(parse_part, cc_header.split(',')))


class CachedResponse(StringIO):
        """
        A response object compatible with urllib2.response objects but for
        cached responses.
        """
        cached = True
        def __init__(self, response):
                #super(CachedResponse, self).__init__(response.read())
                StringIO.__init__(self, response.read())
                self.seek(0)
                self.headers = response.info()
                self.url = response.url
                self.code = response.code
                self.msg = response.msg

        def save(self):
                self.headers['x-urllib2-cache'] = 'Stored'
                return pickle.dumps(self)

        @classmethod
        def load(cls, payload):
                if payload is None:
                        return None
                result = pickle.loads(payload)
                result.headers['x-urllib2-cache'] = 'Cached'
                return result

        def info(self):
                return self.headers

        def geturl(self):
                return self.url

        def reload(self, store):
                opener = urllib2.build_opener()
                self.__init__(opener.open(self.url))
                store.set(self.url, self.save())

        @property
        def age(self):
                "Return the age of this response, guaranteed >= 0"
                date = datetime_from_email(self.headers['date'])
                now = datetime.datetime.utcnow()
                zero = datetime.timedelta()
                return max(zero, now - date)

        def fresh(self):
                """
                Check the max-age and expires headers on this response. Return
                True if this response has not expired.
                """
                cc = CacheHandle._parse_cache_control(self.headers)
                if 'no-cache' in cc:
                        return False
                if not self.within_max_age(cc):
                        return False
                if 'expires' in cc:
                        try:
                                expires = datetime_from_email(self.headers['expires'])
                                now = datetime.datetime.utcnow()
                                if expires < now:
                                        return False
                        except ValueError:
                                pass
                return True

        def fresh_for(self, req_headers):
                """
                Check if this response is fresh in its own right and with
                respect to the request headers.
                """
                cc = CacheHandle._parse_cache_control(req_headers)
                return self.fresh() and self.within_max_age(cc)

        def within_max_age(self, cache_control):
                if not 'date' in self.headers:
                        return False
                if 'max-age' not in cache_control:
                        return False
                # user-agent might have a 'min-fresh' directive indicating the
                #  client will only accept a cached request if it will still be
                #  fresh min-fresh seconds from now.
                try:
                        min_fresh = datetime.timedelta(
                                seconds = int(cache_control['min-fresh']))
                except (KeyError, ValueError):
                        min_fresh = datetime.timedelta()
                try:
                        max_age = datetime.timedelta(
                                seconds=int(cache_control['max-age']))
                        if self.age + min_fresh > max_age:
                                return False
                except ValueError:
                        pass
                return True

        def update_headers(self, new_headers):
                for header in get_endpoint_headers(new_headers):
                        self.headers[header] = new_headers[header]

def get_endpoint_headers(headers):
        """
        Given a dictionary-like headers object, return the names of all
        headers in that set which represent end-to-end (and not intermediate
        or connection headers).
        """
        intermediate_headers = ['connection', 'keep-alive',
                'proxy-authenticate', 'proxy-authorization', 'te', 'trailers',
                'transfer-encoding', 'upgrade']
        intermediate_headers.extend(header.strip()
                for header in headers.get('connection', ''))
        return set(headers.keys()) - set(intermediate_headers)

def datetime_from_email(str):
        parsed = email.Utils.parsedate_tz(str)
        if not parsed:
                raise ValueError("Unrecognized date %s" % str)
        offset = datetime.timedelta(seconds=parsed[-1] or 0)
        naive_date = datetime.datetime(*parsed[:6])
        return naive_date - offset







###############

class ProxyHandler (BaseHTTPServer.BaseHTTPRequestHandler,replace,Blocker):
    __base = BaseHTTPServer.BaseHTTPRequestHandler
    __base_handle = __base.handle

    
    rbufsize = 0                        

    def handle(self):
        ###
	#self.updatedict()	
	(ip, port) =  self.client_address
	chk=ip+'\n'
	with open("client.txt","r+a") as fp:
		if chk not in fp.readlines():
			fp.write(ip+'\n') 
	#fp.write(ip+"\n")
	#fp.close
	
	#lines_seen = set() # holds lines already seen
	#outfile = open("client1.txt", "w")
	#for line in open("client.txt", "r"):
    	#	if line not in lines_seen: # not a duplicate
        #		outfile.write(line)
        #		lines_seen.add(line)
	#outfile.close()



	####nat
	#self.client_address=(200.200.200.1,port)
	###
        self.server.logger.log (logging.INFO, "Request from '%s'", ip)
        if hasattr(self, 'allowed_clients') and ip not in self.allowed_clients:
            self.raw_requestline = self.rfile.readline()
            if self.parse_request(): self.send_error(403)
        else:
            self.__base_handle()

    def _connect_to(self, netloc, soc):
        
####	
	Blocker.__init__(self)
        host_port = netloc, 80
        self.server.logger.log (logging.INFO, "connect to %s:%d", host_port[0], host_port[1])
	####
	print self.path +'\they'
	chk=self.matches_blocked(self.path)
	#print netloc +'\tapoorva'
	if chk:
		print "\nBLOCKED A CONNECTION TO AN UNAUTHORISED DOMAIN:\n"
	
	elif chk==0:
		print "hello"		
		try: soc.connect(host_port)
            	except socket.error, arg:
                	try: msg = arg[1]
                	except: msg = arg
                	self.send_error(404, msg)
                	return 0
            	return 1
	###	
	"""
        try: soc.connect(host_port)
        except socket.error, arg:
            try: msg = arg[1]
            except: msg = arg
            self.send_error(404, msg)
            return 0
        return 1
	"""

    def do_CONNECT(self):
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            if self._connect_to(self.path, soc):
                self.log_request(200)
                self.wfile.write(self.protocol_version +
                                 " 200 Connection established\r\n")
                self.wfile.write("Proxy-agent: %s\r\n" % self.version_string())
                self.wfile.write("\r\n")
                self._read_write(soc, 300)
        finally:
            soc.close()
            self.connection.close()

    def do_GET(self):
        from httplib2 import FileCache
        logging.basicConfig(level=logging.DEBUG)
        store = FileCache("cache4")
        opener = urllib2.build_opener(CacheHandle(store))
        urllib2.install_opener(opener)
        response = opener.open(self.path)
	
	(scm, netloc, path, params, query, fragment) = urlparse.urlparse(
            self.path, 'http')
        if scm not in ('http', 'ftp') or fragment or not netloc:
            self.send_error(400, "bad url %s" % self.path)
            return
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
        try:
            if scm == 'http':
                if self._connect_to(netloc, soc):
                    self.log_request()
                    soc.send("%s %s %s\r\n" % (self.command,
                                               urlparse.urlunparse(('', '', path,
                                                                    params, query,
                                                                    '')),
                                               self.request_version))
                    self.headers['Connection'] = 'close'
                    del self.headers['Proxy-Connection']
                    for key_val in self.headers.items():
                        soc.send("%s: %s\r\n" % key_val)
                    soc.send("\r\n")
                    self._read_write(soc)
           
        finally:
            soc.close()
            self.connection.close()

    def _read_write(self, soc, max_idling=20, local=False):
        iw = [self.connection, soc]
        local_data = ""
        ow = []
        count = 0
        while 1:
            count += 1
            (ins, _, exs) = select.select(iw, ow, iw, 1)
            if exs: break
            if ins:
                for i in ins:
                    if i is soc: out = self.connection
                    else: out = soc
                    data = i.recv(8192)
                    if data:
                        if local: local_data += data
                        else: out.send(data)
                        count = 0
            if count == max_idling: break
        if local: return local_data
        return None

    do_HEAD = do_GET
    do_POST = do_GET
    do_PUT  = do_GET
    do_DELETE=do_GET

    def log_message (self, format, *args):
        self.server.logger.log (logging.INFO, "%s %s", self.address_string (),
                                format % args)
        
    def log_error (self, format, *args):
        self.server.logger.log (logging.ERROR, "%s %s", self.address_string (),
                                format % args)

class ThreadingHTTPServer (SocketServer.ThreadingMixIn,
                           BaseHTTPServer.HTTPServer):
    def __init__ (self, server_address, RequestHandlerClass, logger=None):
        BaseHTTPServer.HTTPServer.__init__ (self, server_address,
                                            RequestHandlerClass)
        self.logger = logger

def logSetup (filename, log_size, daemon):
    logger = logging.getLogger ("Proxy")
    logger.setLevel (logging.INFO)
    if not filename:
        if not daemon:
            # display to the screen
            handler = logging.StreamHandler ()
        else:
            handler = logging.handlers.RotatingFileHandler (DEFAULT_LOG_FILENAME,
                                                            maxBytes=(log_size*(1<<20)),
                                                            backupCount=5)
    else:
        handler = logging.handlers.RotatingFileHandler (filename,
                                                        maxBytes=(log_size*(1<<20)),
                                                        backupCount=5)
    fmt = logging.Formatter ("[%(asctime)-12s.%(msecs)03d] "
                             "%(levelname)-8s {%(name)s %(threadName)s}"
                             " %(message)s",
                             "%Y-%m-%d %H:%M:%S")
    handler.setFormatter (fmt)
        
    logger.addHandler (handler)
    return logger


def handler (signo, frame):
    while frame and isinstance (frame, FrameType):
        if frame.f_code and isinstance (frame.f_code, CodeType):
            if "run_event" in frame.f_code.co_varnames:
                frame.f_locals["run_event"].set ()
                return
        frame = frame.f_back
    
def daemonize (logger):
    class DevNull (object):
        def __init__ (self): self.fd = os.open ("/dev/null", os.O_WRONLY)
        def write (self, *args, **kwargs): return 0
        def read (self, *args, **kwargs): return 0
        def fileno (self): return self.fd
        def close (self): os.close (self.fd)
    class ErrorLog:
        def __init__ (self, obj): self.obj = obj
        def write (self, string): self.obj.log (logging.ERROR, string)
        def read (self, *args, **kwargs): return 0
        def close (self): pass
        
    if os.fork () != 0:
        ## allow the child pid to instanciate the server
        ## class
        sleep (1)
        sys.exit (0)
    os.setsid ()
    fd = os.open ('/dev/null', os.O_RDONLY)
    if fd != 0:
        os.dup2 (fd, 0)
        os.close (fd)
    null = DevNull ()
    log = ErrorLog (logger)
    sys.stdout = null
    sys.stderr = log
    sys.stdin = null
    fd = os.open ('/dev/null', os.O_WRONLY)
    #if fd != 1: os.dup2 (fd, 1)
    os.dup2 (sys.stdout.fileno (), 1)
    if fd != 2: os.dup2 (fd, 2)
    if fd not in (1, 2): os.close (fd)
    
def main (ipadd,port,log):
    logfile=log
    daemon  = False
    max_log_size = 100
#   port = 8000
    allowed = []
    run_event = threading.Event ()
#    local_hostname = socket.gethostname ()

 

    opts, args = getopt.getopt (sys.argv[1:], "l:dhp:", [])

    for opt, value in opts:
       
        #if opt == "-l": logfile = value
        if opt == "-d": daemon = not daemon
        
          
        
    # setup the log file
    logger = logSetup (logfile, max_log_size, daemon)
    
    if daemon:
        daemonize (logger)
    signal.signal (signal.SIGINT, handler)
       
    
    logger.log (logging.INFO, "Any clients will be served...")




   # ipadd=raw_input("\nEnter ip address : ")
   # port=input("\nEnter port : ")    
    server_address = (ipadd, port)

    #server_address = (socket.gethostbyname (local_hostname), port)
    ProxyHandler.protocol = "HTTP/1.0"
    

    httpd = ThreadingHTTPServer (server_address, ProxyHandler, logger)
    sa = httpd.socket.getsockname ()
    print "\nServering HTTP on", sa[0], "port", sa[1]
    req_count = 0
    while not run_event.isSet ():
        try:
            httpd.handle_request ()
            req_count += 1
            if req_count == 1000:
                logger.log (logging.INFO, "Number of active threads: %s",
                            threading.activeCount ())
                req_count = 0
        except select.error, e:
            if e[0] == 4 and run_event.isSet (): pass
            else:
                logger.log (logging.CRITICAL, "Errno: %d - %s", e[0], e[1])
    logger.log (logging.INFO, "Server shutdown")
    return 0

if __name__ == '__main__':
    sys.exit (main (ipadd,port,log))
