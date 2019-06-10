import queue
import threading
import urllib.request
import urllib.parse
import urllib.error
import urllib
from optparse import OptionParser
from fake_useragent import UserAgent

print()
print("  _____  _      ____             _            ")
print(" |  __ \(_)    |  _ \           | |           ")
print(" | |  | |_ _ __| |_) |_ __ _   _| |_ ___ _ __ ")
print(" | |  | | | '__|  _ <| '__| | | | __/ _ \ '__|")
print(" | |__| | | |  | |_) | |  | |_| | ||  __/ |   ")
print(" |_____/|_|_|  |____/|_|   \__,_|\__\___|_|   ")
print("          ______                              ")
print("         |______|                             ")
print("\nAuthor: Vaibhav Kush\nTested By: Priyam Harsh")

parser = OptionParser(usage="Usage: %prog -u [URL] -w [Wordlist]",version="%prog 1.0")
parser.add_option("-u", "--url",dest="target_url", default='', help="Target URL", type="str")
parser.add_option("-w", "--wfile",dest="wordlist_file", default='', help="Path to Wordlist File", type="str")
(options, args) = parser.parse_args()

ch = input("Do you want to use extensions as well? (y/N): ")
if ch=='Y' or ch=='y':
    extensions=['.php','.py','html','.bak','.jsp','.psp','.js','.orig','.inc','.cgi','.asp','.aspx']
else:
    extensions=[]

ua = UserAgent()
threads=20
resume=None
user_agent=ua.random

if not options.target_url or not options.wordlist_file:
    parser.error("[-] Invalid Syntax")

def build_wordlist(wordlist_file):

    fd=open(wordlist_file,'rb')
    raw_words=fd.readlines()
    fd.close()
    
    found_resume=False
    words=queue.Queue()

    for word in raw_words:

        word=word.rstrip()
        words.put(word)

    return words


def dir_bruter(word_queue,extensions=None):

    while not word_queue.empty():
        attempt=word_queue.get().decode('utf-8')
        
        attempt_list=[]

        #check to see if there is a file extension;
        #if not,it's a directory path we're bruting

        if '.' not in attempt:
            
            #if we want to bruteforce extensions
            if extensions:
                for extension in extensions:
                    attempt_list.append('/%s%s' %(attempt,extension))
            attempt_list.append('/%s/'%attempt)
                
        else:
            attempt_list.append('/%s/'%attempt)
        
        #iterate over our list of attempts
        for brute in attempt_list:
            url='%s%s' %(options.target_url,urllib.parse.quote(brute))
            try:
                headers={}
                headers['User-Agent']=user_agent
                
                r=urllib.request.Request(url,headers=headers)
                
                response=urllib.request.urlopen(r)
                #html,header=urllib.request.urlretrieve(url)

                if response:
                    print('[%d] >> %s' %(response.code,url))
                                        
            except urllib.error.URLError as e:
                
                if hasattr(e,'code') and e.code!=404:
                    print('[%d]!! >> %s' %(e.code,url))
                    
                pass
        
            
word_queue=build_wordlist(options.wordlist_file)

for i in range(threads):
    t=threading.Thread(target=dir_bruter,args=(word_queue,))
    t.start()

'''
responses = {
    100: ('Continue', 'Request received, please continue'),
    101: ('Switching Protocols',
          'Switching to new protocol; obey Upgrade header'),

    200: ('OK', 'Request fulfilled, document follows'),
    201: ('Created', 'Document created, URL follows'),
    202: ('Accepted',
          'Request accepted, processing continues off-line'),
    203: ('Non-Authoritative Information', 'Request fulfilled from cache'),
    204: ('No Content', 'Request fulfilled, nothing follows'),
    205: ('Reset Content', 'Clear input form for further input.'),
    206: ('Partial Content', 'Partial content follows.'),

    300: ('Multiple Choices',
          'Object has several resources -- see URI list'),
    301: ('Moved Permanently', 'Object moved permanently -- see URI list'),
    302: ('Found', 'Object moved temporarily -- see URI list'),
    303: ('See Other', 'Object moved -- see Method and URL list'),
    304: ('Not Modified',
          'Document has not changed since given time'),
    305: ('Use Proxy',
          'You must use proxy specified in Location to access this '
          'resource.'),
    307: ('Temporary Redirect',
          'Object moved temporarily -- see URI list'),

    400: ('Bad Request',
          'Bad request syntax or unsupported method'),
    401: ('Unauthorized',
          'No permission -- see authorization schemes'),
    402: ('Payment Required',
          'No payment -- see charging schemes'),
    403: ('Forbidden',
          'Request forbidden -- authorization will not help'),
    404: ('Not Found', 'Nothing matches the given URI'),
    405: ('Method Not Allowed',
          'Specified method is invalid for this server.'),
    406: ('Not Acceptable', 'URI not available in preferred format.'),
    407: ('Proxy Authentication Required', 'You must authenticate with '
          'this proxy before proceeding.'),
    408: ('Request Timeout', 'Request timed out; try again later.'),
    409: ('Conflict', 'Request conflict.'),
    410: ('Gone',
          'URI no longer exists and has been permanently removed.'),
    411: ('Length Required', 'Client must specify Content-Length.'),
    412: ('Precondition Failed', 'Precondition in headers is false.'),
    413: ('Request Entity Too Large', 'Entity is too large.'),
    414: ('Request-URI Too Long', 'URI is too long.'),
    415: ('Unsupported Media Type', 'Entity body in unsupported format.'),
    416: ('Requested Range Not Satisfiable',
          'Cannot satisfy request range.'),
    417: ('Expectation Failed',
          'Expect condition could not be satisfied.'),

    500: ('Internal Server Error', 'Server got itself in trouble'),
    501: ('Not Implemented',
          'Server does not support this operation'),
    502: ('Bad Gateway', 'Invalid responses from another server/proxy.'),
    503: ('Service Unavailable',
          'The server cannot process the request due to a high load'),
    504: ('Gateway Timeout',
          'The gateway server did not receive a timely response'),
    505: ('HTTP Version Not Supported', 'Cannot fulfill request.'),
    }
'''
