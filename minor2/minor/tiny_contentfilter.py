#!/bin/sh -

#import BaseHTTPServer, select, socket, SocketServer, urlparse
#from string import *
from proxy3_util import glob_to_regex
import proxy3_config
#
#f = open('proxy.txt', 'r')
#i=0
#l=1
#t=0
#storage=0
#urlkey="key"
#allowedlist = []
#while i<10000:
#    cvalue=f.read(1)
#    t+=1
#    if(cvalue==";"):
#        storage+=t
#        f.seek(storage-t)
#        urlkey=f.read(t-1)
#        f.seek(storage)
#        allowedlist.append(urlkey)
#        print "ENTRY FOUND", urlkey
#        t=0
#        i+=1
#        l+=1
#    if(cvalue==""):
#        print "EOF"
#        i=10000
#    i+=1
#print "Proxy.txt file with", l-1, "entries"

#i=1
#f.seek(0)
#x=0


#f.close()

class Blocker:
    blocked = proxy3_config.get('block')
    nocookies = proxy3_config.get('nocookies')
    docookies = proxy3_config.get('docookies')
    
    def __init__(self):
	# Process the glob expressions, then compile into regexes
	# Store the regexes in the object, not the class
	# print Blocker.blocked
        self.blocked = map(glob_to_regex, Blocker.blocked)
        self.nocookies = map(glob_to_regex, Blocker.nocookies)
        self.docookies = map(glob_to_regex, Blocker.docookies)

	a=10;
        
    def matches_blocked(self, s):
	"""Returns 1 if the string matches one of the blocked sites"""
		
	for b in self.blocked:
	    if b.match(s) != None:
		print "found"
		return 1
	return 0

    def matches_nocookie(self, s):
	"""Returns 1 if the string matches one of the blocked sites"""
        if proxy3_options.options.get('accept-cookie-default', 1):
            for b in self.nocookies:
                if b.match(s) != None:
                    return 1
            return 0
        else:
            for b in self.docookies:
                if b.match(s) != None:
                    return 0
            return 1
        


"""
class ProxyHandler (BaseHTTPServer.BaseHTTPRequestHandler,Blocker):
    __base = BaseHTTPServer.BaseHTTPRequestHandler
    __base_handle = __base.handle

   # server_version = "TinyHTTPProxy/" + __version__
    rbufsize = 0 # self.rfile Be unbuffered

    def handle(self):
        (ip, port) = self.client_address
        if hasattr(self, 'allowed_clients') and ip not in self.allowed_clients:
            self.raw_requestline = self.rfile.readline()
            if self.parse_request(): self.send_error(403)
        else:
            self.__base_handle()

    def _connect_to(self, netloc, soc):
	
	Blocker.__init__(self)
	#print "jkggcgfc"  
	#print blocker.a 
	i = netloc.find(':')
        if i >= 0:
            host_port = netloc[:i], int(netloc[i+1:])
        else:
            host_port = netloc, 80

        print "CONNECTION TEST:\n"
	####
        #search = str(allowedlist[1])
	#index = netloc.find(search)
	#print "SEARCHED FOR", search, "in", netloc, "RESULT:", index
        #print "\t" "connect to %s:%d" % host_port
	###
	print self.path +'\they'
	chk=self.matches_blocked(self.path)
	#print netloc +'\tapoorva'
	if chk:
		print "BLOCKED A CONNECTION TO AN UNAUTHORISED DOMAIN:\n"
	
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
       #if index==-1:

            #try: soc.connect(host_port)
            #except socket.error, arg:
             #   try: msg = arg[1]
              #  except: msg = arg
               # self.send_error(404, msg)
                #return 0
            #return 1

        #else:
         #   print "BLOCKED A CONNECTION TO AN UNAUTHORISED DOMAIN:\n"

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
            print "\t" "bye"
            soc.close()
            self.connection.close()

    def do_GET(self):
        (scm, netloc, path, params, query, fragment) = urlparse.urlparse(
            self.path, 'http')
        if scm != 'http' or fragment or not netloc:
            self.send_error(400, "bad url %s" % self.path)
            return
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            if self._connect_to(netloc, soc):
                self.log_request()
                soc.send("%s %s %s\r\n" % (
                    self.command,
                    urlparse.urlunparse(('', '', path, params, query, '')),
                    self.request_version))
                self.headers['Connection'] = 'close'
                del self.headers['Proxy-Connection']
                for key_val in self.headers.items():
                    soc.send("%s: %s\r\n" % key_val)
                soc.send("\r\n")
                self._read_write(soc)
        finally:
            print "\t" "bye"
            soc.close()
            self.connection.close()

    def _read_write(self, soc, max_idling=20):
        iw = [self.connection, soc]
        ow = []
        count = 0
        while 1:
            count += 1
            (ins, _, exs) = select.select(iw, ow, iw, 3)
            if exs: break
            if ins:
                for i in ins:
                    if i is soc:
                        out = self.connection
                    else:
                        out = soc
                    data = i.recv(8192)
                    if data:
                        out.send(data)
                        count = 0
            else:
                print "\t" "idle", count
            if count == max_idling: break

    do_HEAD = do_GET
    do_POST = do_GET
    do_PUT = do_GET
    do_DELETE=do_GET

class ThreadingHTTPServer (SocketServer.ThreadingMixIn,
                           BaseHTTPServer.HTTPServer): pass

if __name__ == '__main__':
    """"""from sys import argv
    if argv[1:] and argv[1] in ('-h', '--help'):
        print argv[0], "[port [allowed_client_name ...]]"
    else:
        if argv[2:]:
            allowed = []
            for name in argv[2:]:
                client = socket.gethostbyname(name)
                allowed.append(client)
                print "Accept: %s (%s)" % (client, name)
            ProxyHandler.allowed_clients = allowed
            del argv[2:]
        else:"""
"""print "Any clients will be served..."
BaseHTTPServer.test(ProxyHandler, ThreadingHTTPServer)"""
