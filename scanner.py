#!/usr/bin/env python
import netifaces
import commands
import sys
from scapy.all import *

from curl import ipcheck


def setter(freeips, diface, n, setips):
    print "The following ips are already set on this machine:"
    count = 0
    for iface, ip in setips.items():
        print iface, "  :  ", str(ip[0])
        count += 1
    opt = raw_input("Would you like to use the existing ones? y/n\n")
    if opt == 'y':
        return 1
    else:
        print "Removing the existing interfaces......."
        for iface, ip in setips.items():
            # print iface
            down = "ifconfig " + str(iface) + " down"
            # print str(down)
            if iface != diface:
                l = commands.getoutput(str(down))
                print "Interface", iface, "with ip", ip[0], "down."
        print "Starting to add interfaces......."
        y = 0
        ips = []
        for i in xrange(int(n)):
            if y > len(freeips):
                print "Ran out of proper responsive ips.\nExiting."
                return 0
            iface = str(str(diface) + ":" + str(i))
            x = 0
            while x == 0:
                if y >= len(freeips):
                    print "Ran out of proper responsive ips :/.\nExiting."
                    return 0
                val = str(freeips[y]).split('.')[3]
                # print val
                # if val<254 and val>200:
                up = "ifconfig " + iface + " " + str(freeips[y]) + "/24 up"
                a = commands.getoutput(str(up))
                x = ipcheck(iface)
                if x == 1 or x == 2:
                    print "Interface", iface, "with ip", freeips[y], "up."
                    ips.append(freeips[y])
                y += 1
        print "Successfully finished setting all ips."
    return ips


def scanner(n):
    default = "route | grep 'default' | awk '{print $8}'"
    diface = commands.getoutput(default)
    srcip = netifaces.ifaddresses(diface)[2][0]['addr']
    netmask = netifaces.ifaddresses(diface)[2][0]['netmask']
    octets = srcip.split('.')
    starttime = time.time()
    global gw
    gw = octets[0] + "." + octets[1] + "." + octets[2]
    dest = gw + ".0/24"
    # print dest
    answered, unanswered = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=str(dest)), timeout=2, verbose=0)
    endtime = time.time()
    ifaces = "ifconfig | grep -o " + str(diface) + " | wc -l"
    num = int(commands.getoutput(ifaces))
    setips = defaultdict(list)
    setips[diface].append(str(srcip))
    existing = [srcip]
    freeips = []
    totaltime = endtime - starttime
    print "Sent ARP requests in %f seconds..." % (totaltime)
    for i in range(0, num - 1):
        iface = diface + ":" + str(i)
        ip = netifaces.ifaddresses(iface)[2][0]['addr']
        setips[iface].append(str(ip))
        existing.append(str(ip))
    print existing
    print setips
    # for i in range(0,len(answered)):
    # print "Response from " + answered[i][1].psrc + " using " + answered[i][1].hwsrc
    print "Found %d ips that are already set to this computer." % (len(setips))
    for i in range(0, len(unanswered)):
        freeips.append(str(unanswered[i][1].pdst))
    freeips = set(freeips) - set(existing)
    freeips.remove(gw + '.0')
    freeips.remove(gw + '.255')
    # freeips.remove(gw+'.1')
    print "Found %d ips that are free." % (len(freeips))
    completedtime = time.time()
    totaltime = completedtime - starttime
    print "Completed scan in %f seconds..." % totaltime
    # unanswered = unanswered.remove(srcip)
    # return freeips
    print setips
    res = setter(list(freeips), diface, n, setips)
    if res == 1:
        existing.remove(srcip)
        return existing, diface
    elif res == 0:
        print "The program has encountered an error!\nExiting."
        sys.exit(1)
    else:
        return res, diface


if __name__ == '__main__':
    scanner(sys.argv[1])