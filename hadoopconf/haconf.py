#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
import commands
from optparse import OptionParser


def main(argv):
    parser = OptionParser(
    usage="usage haconf.py %prog -h hostname | -f hostfile [-u |-d |-t ]",
    description="""Make hadoop configure file to remote hosts
    """
    )
    parser.add_option("-n", "--host", dest="host", help="The remote hostname string")
    parser.add_option("-f", "--file", dest="file", help="The remote hostname file",metavar="FILE")
    parser.add_option("-d", "--dest-path", dest="destpath", help="The remote path to send file",default="/data/ljw/hadoop-1.0.2/conf/hdfs-site.xml")
    parser.add_option("-u", "--user", dest="user", help="The remote username",default="bigdata")
    parser.add_option("-t", "--template", dest="temp", help="The template file default is locale file <hdfs-site-template.xml>",default="./hdfs-site-template.xml")

    (options, args) = parser.parse_args(argv)
    destpath = options.destpath
    user = options.user
    temp = options.temp
    if options.host:
        filetosend = changefile(temp,options.host)
        sendfile(filetosend,user,options.host,destpath)
    elif options.file:
        f = open(options.file,"r")
        hosts = f.readlines()
        for host in hosts:
            host = host.replace("\n","")
            filetosend = changefile(temp,host)
            sendfile(filetosend,user,host,destpath)
    else:
        print "host must be input,string or file"

def sendfile(filename,user,host,dest):
    cmd = "scp %s %s@%s:%s" %(filename,user,host,dest)
    #print cmd
    res = commands.getstatusoutput(cmd)
    if res[0] != 0:
        print "send %s to %s error" % (filename,host)
    else:
        print "send %s to %s successs" % (filename,host)

def changefile(path,hostname):
    f = open(path,"r")
    old = f.read()
    f.close()
    num = re.findall(r"\d+", hostname)
    if not num:
        num = "_" + hostname
    new = old.replace(r"mnt","mnt"+num[0])
    p = "./hdfs-site.xml"
    f = open(p,"w")
    f.write(new)
    return p
    


if __name__ == "__main__":
    import sys
    args = sys.argv[1:]
    res = main(args)
