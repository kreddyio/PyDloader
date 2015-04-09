from curl import getsize, download, login, ipcheck, logout
from threading import Thread
import sys, shutil, os, time
from scanner import scanner


def join(filename, files):
    # print filename
    output = open(filename, 'ab')
    for x in files:
        shutil.copyfileobj(open(x, 'rb'), output)
        os.remove(x)
    print "Final file has been successfully saved."


def check(filename, files, sizes):
    # print "\nSizes\n",sizes
    for x in xrange(len(files)):
        if sizes[x] == os.path.getsize(files[x]):
            print files[x], "is alright."
        else:
            print "sizes gave", sizes[x], "and os gave", os.path.getsize(files[x])
            print "There has been a problem with", files[x], "!\n Would you like to restart it? (y/n)"
            opt = raw_input("")
            if opt == 'y':
                main_args = [sys.argv[0], url, filename, len(files), "-p", x + 1]
                main(main_args)
            else:
                print "Exiting.."
                sys.exit(1)
    # print files
    print "Joining the part files to form the final %s file..." % filename
    join(filename, files)


def progressbar(files, size):
    sizes = 0
    limit = 1
    prev = 0
    t = 1
    kb = 1024
    mb = 1024 * kb
    gb = 1024 * mb
    totspeed = 0
    while (True):
        time.sleep(limit)
        sizes = 0
        for x in files:
            sizes += os.path.getsize(x)
        percent = (sizes / float(size)) * 100
        dloaded = float(sizes - prev)
        if t % 10 == 0 and prev == sizes:
            break
        if dloaded <= kb:
            speed = str(dloaded)
            val = 'bps'
        elif kb < dloaded <= mb:
            speed = str(dloaded / kb)
            val = 'kbps'
        elif mb < dloaded <= gb:
            speed = str(dloaded / mb)
            val = 'mbps'
        print '\r',
        sys.stdout.flush()
        print sizes, 'bytes done', "%2.2f" % (percent), '%', 'done.', "%3.2f" % (float(speed)), "%s" % (val),
        print '\r',
        sys.stdout.flush()
        t += limit
        if sizes == size:
            print '\n'
            avspeed = size / float(t)
            if avspeed <= kb:
                avspeed = avspeed
                val = 'bps'
            elif kb < avspeed <= mb:
                avspeed = avspeed / kb
                val = 'kbps'
            elif mb < avspeed <= gb:
                avspeed = avspeed / mb
                val = 'mbps';
            print 'Download completed in %d seconds at %0.2f %s ' % (t, avspeed, val)
            break
        prev = sizes


def main(argv):
    try:
        global url
        url = argv[1]
        filename = argv[2]
        chunks = int(argv[3])

    except IndexError:
        print "Error in the syntax!\n"
        print "\tUsage:\n", sys.argv[0], "<url> <filename> <numofchunks>"
        sys.exit(1)
    files = []
    sizes = []
    print "Connecting to the site for getting file size..."
    size = int(getsize(url))
    print "Size: ", size, "bytes"
    print "Starting to set the required ips."
    ips, diface = scanner(chunks)
    print ips, diface
    chunksize = int(size / chunks)
    partsize = int(size / chunks)
    newstart = 0
    if len(argv) > 4:
        if argv[4] == '-p':
            try:
                part = int(argv[5])
                filename = filename + str(part) + '.dat'
                newstart = int((part - 1) * partsize)
                # print newstart
                # sys.exit(1)
                # newend = partsize+newstart
                partsize = int(size / (chunks * chunks))
            except Exception, e:
                print "Error! expected the required chunk number to re-download with \"-p\" option."
                sys.exit(1)
        else:
            print "Error! Expected only three arguments!\n\tUsage:\n"
            print sys.argv[0], "<url> <filename> <numofchunks> [-p <chunknumber to re-download>"
            print "(Be sure that num of chunks is same as the previous failed download.)]"
            sys.exit(1)
    for x in xrange(chunks):
        ret = 0
        while ret == 0:
            log = ipcheck(ips[x])
            if log == 1:
                user = raw_input("username:")
                password = raw_input("password:")
                ret = login(user, password, ips[x])
            elif log == 2:
                print "%s is already logged in." % (ips[x])
                ret = 1
    threads = []
    for x in xrange(0, chunks):
        fl = filename + str(x + 1) + '.dat'
        files.append(fl)
        existing = 0
        if os.path.exists(fl):
            existing = os.path.getsize(fl)
            print "existing-", existing
        start = int((x * partsize) + newstart) + existing
        if x != chunks - 1:
            end = int((((x + 1) * partsize) - 1) + newstart)
            sizes.append(partsize)
        else:
            if len(argv) == 6:
                end = int((part) * chunksize) - 1
                if part == chunks:
                    end = size
                sizes.append(end - start + 1)
            else:
                end = size
                sizes.append(end - ((x) * partsize))
        print start, "-", end
        thread = Thread(target=download, args=[url, start, end, ips[x], fl])
        thread.setDaemon(True)
        if start != (end + 1) and x != chunks - 1:
            threads.append(thread)
        if start != (end) and x == chunks - 1:
            threads.append(thread)
    # sys.exit(1)
    print "Starting threads...."
    for x in threads:
        x.start()
    print "Size:", size
    progress = Thread(target=progressbar, args=[files, size])
    progress.setDaemon(True)
    progress.start()
    progress.join()
    for x in threads:
        x.join()
    print "\nCompleted downloading all the part files."
    # print "Starting time.."
    # time.sleep(10)
    print "Checking the downloaded part files."
    check(filename, files, sizes)

    for x in xrange(chunks):
        logout(ips[x])
if __name__ == '__main__':
    if "--help" in sys.argv or len(sys.argv) == 1:
        print "Usage:\n", sys.argv[0], "<url> <filename> <numofchunks> [-p <chunknumber to re-download>"
        print "(Be sure that num of chunks is same as the previous failed download.)] [--help]"
        print "<url> - Final file link to Download."
        print "<filename> - Final file name to save the download."
        print "<numofchunks> - number of connections to download from."
        print "( This should be the same as previous failed download if used with \"-p\" option.)"
        print "-p - to be used when a part file failed to download and you quit restarting it."
        print "<chunknumber to re-download> - the part file number to re-download."
        print "--help - Displays this help dialog."
        sys.exit(1)
    main(sys.argv)