import pycurl
import cStringIO


def download(url, start, end, ip, filename):
    curl = pycurl.Curl()
    fp = open(filename, "ab")
    curl.setopt(pycurl.URL, url)
    curl.setopt(pycurl.NOSIGNAL, 1)
    curl.setopt(pycurl.NOPROGRESS, 1)
    curl.setopt(pycurl.WRITEDATA, fp)
    curl.setopt(pycurl.INTERFACE, ip)
    curl.setopt(pycurl.RANGE, str(start) + '-' + str(end))
    # curl.setopt(pycurl.TIMEOUT, 20)
    curl.setopt(pycurl.LOW_SPEED_LIMIT, 1)
    curl.setopt(pycurl.LOW_SPEED_TIME, 15)
    curl.setopt(pycurl.SSL_VERIFYPEER, 0)
    curl.setopt(pycurl.SSL_VERIFYHOST, 0)
    try:
        curl.perform()
    except:
        pass


def login(user, passw, ip):
    buf = cStringIO.StringIO()
    USER_AGENT = 'Mozilla/5.0 (X11; U; Linux i686; en-GB; rv:1.9.0.5) Gecko/2008121622 Ubuntu/8.10 (intrepid) Firefox/3.0.5'
    c = pycurl.Curl()
    c.setopt(c.URL, 'https://10.1.0.10:8090/httpclient.html')
    c.setopt(c.WRITEFUNCTION, buf.write)
    c.setopt(c.CONNECTTIMEOUT, 3)
    c.setopt(c.INTERFACE, ip)
    c.setopt(c.TIMEOUT, 5)
    c.setopt(c.MAXREDIRS, 5)
    c.setopt(c.POSTFIELDS, 'username=' + user + '&password=' + passw + '&mode=191')
    c.setopt(c.COOKIEFILE, 'cookie.txt')
    c.setopt(c.USERAGENT, USER_AGENT)
    c.setopt(c.COOKIEJAR, 'cookies.txt')
    c.setopt(c.ENCODING, 'gzip, deflate')
    c.setopt(c.SSL_VERIFYPEER, 0)
    c.setopt(c.SSL_VERIFYHOST, 0)
    c.setopt(c.FAILONERROR, True)
    c.setopt(c.HTTPHEADER, ['Accept: text/html', 'Accept-Charset: UTF-8'])
    # c.setopt(c.VERBOSE, True)
    try:
        c.perform()
    except:
        return 0
    # print buf.getvalue()
    if "You have successfully logged in" in buf.getvalue():
        print "Successful at login with %s and %s at ip %s" % (user, passw, ip)
        buf.close()
        return 1
    else:
        buf.close()
        print "The id - %s is not working please give a new one." % (user)
        return 0


def logout(ip):
    buf = cStringIO.StringIO()
    USER_AGENT = 'Mozilla/5.0 (X11; U; Linux i686; en-GB; rv:1.9.0.5) Gecko/2008121622 Ubuntu/8.10 (intrepid) Firefox/3.0.5'
    c = pycurl.Curl()
    c.setopt(c.URL, 'https://10.1.0.10:8090/httpclient.html')
    c.setopt(c.WRITEFUNCTION, buf.write)
    c.setopt(c.CONNECTTIMEOUT, 3)
    c.setopt(c.INTERFACE, ip)
    c.setopt(c.TIMEOUT, 5)
    c.setopt(c.MAXREDIRS, 5)
    c.setopt(c.POSTFIELDS, 'username=aaa&password=bbb&mode=193')
    c.setopt(c.COOKIEFILE, 'cookie.txt')
    c.setopt(c.USERAGENT, USER_AGENT)
    c.setopt(c.COOKIEJAR, 'cookies.txt')
    c.setopt(c.ENCODING, 'gzip, deflate')
    c.setopt(c.SSL_VERIFYPEER, 0)
    c.setopt(c.SSL_VERIFYHOST, 0)
    c.setopt(c.FAILONERROR, True)
    c.setopt(c.HTTPHEADER, ['Accept: text/html', 'Accept-Charset: UTF-8'])
    # c.setopt(c.VERBOSE, True)
    c.perform()
    # print buf.getvalue()
    buf.close()
    print "Logout successful in %s." % (ip)


def ipcheck(ip):
    buf = cStringIO.StringIO()
    USER_AGENT = 'Mozilla/5.0 (X11; U; Linux i686; en-GB; rv:1.9.0.5) Gecko/2008121622 Ubuntu/8.10 (intrepid) Firefox/3.0.5'
    c = pycurl.Curl()
    c.setopt(c.URL, 'google.com')
    c.setopt(c.WRITEFUNCTION, buf.write)
    c.setopt(c.CONNECTTIMEOUT, 2)
    c.setopt(c.INTERFACE, ip)
    c.setopt(c.TIMEOUT, 3)
    c.setopt(c.MAXREDIRS, 5)
    c.setopt(c.COOKIEFILE, 'cookie.txt')
    c.setopt(c.USERAGENT, USER_AGENT)
    c.setopt(c.COOKIEJAR, 'cookies.txt')
    c.setopt(c.ENCODING, 'gzip, deflate')
    c.setopt(c.SSL_VERIFYPEER, 0)
    c.setopt(c.SSL_VERIFYHOST, 0)
    c.setopt(c.FAILONERROR, True)
    c.setopt(c.HTTPHEADER, ['Accept: text/html', 'Accept-Charset: UTF-8'])
    # c.setopt(c.VERBOSE, True)
    try:
        c.perform()
    except:
        buf.close()
        return 0
    a = buf.getvalue()
    buf.close()
    if "10.1.0.10" in a:
        return 1
    elif "moved" in a:
        return 2
    else:
        return 0


def getsize(url):
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.NOBODY, 1)
    c.setopt(pycurl.SSL_VERIFYPEER, 0)
    c.setopt(pycurl.SSL_VERIFYHOST, 0)
    c.perform()
    size = c.getinfo(c.CONTENT_LENGTH_DOWNLOAD)
    return size