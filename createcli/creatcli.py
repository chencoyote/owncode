#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import sys
from optparse import OptionParser
import Shconfig
from dictdiffer import diff, patch


def main(argv):
    parser = OptionParser(
        usage="usage clitool.py %prog -i file -o file.config...",
        description="""Make cli file to cmdconfig file , read example file
        """
    )
    parser.add_option("-i", "--input", dest="input_file", help="Input cli file", metavar="FILE")
    parser.add_option("-o", "--output", dest="output_file", help="Output file")
    
    (options, args) = parser.parse_args(argv)

    cli_line = load_file(options.input_file)
    root = cli_line[0].split()[0]
    out_file = clean_file(root, options.output_file)
    conf = Shconfig.config(name="", conffile=out_file)
    print conf
    if conf is None:
        print "output file is not correct format"
        return
    d = conf.dict
    main_dict = {root: {}}
    for cli in cli_line:
        cmd = cli.split()
        res = list_to_deep_dict(cmd)
        result = diff(main_dict, res, nodel=True)
        patched = patch(result, main_dict, set_remove=False)
        main_dict = patched
    print json.dumps(main_dict, indent=2)
    cof = conf.dict
    print cof
    cof[root] = main_dict[root]
    print cof
    print conf.save()


def load_file(path):
    try:
        ifile = open(path, "r").readlines()
    except IOError:
        print "Can't open file : %s " % (path)
    t = []
    for tmp in ifile:
        tmp = tmp.replace("\n", "")
        t.append(tmp)
    return t


def clean_file(root, path):
    try:
        ofile = open(path, "w")
    except IOError:
        print "Can't open file : %s " % (path)
    ofile.write('%s :\n{\n};' % (root))
    ofile.close()
    return path

def list_to_deep_dict(s, d={}):
    if not s:
        return d
    item = s.pop()
    tmp = {}
    if item.startswith("<"):
        k = item.strip("<>")
        cmd = ""
        if ":" in k:
            cmd = k.split(":")[1]
            k = k.split(":")[0]
        tmp[k] = {}
        tmp[k]["token"] = True
        if cmd:
            tmp[k]["cmd"] = cmd
        for i in d:
            tmp[k][i] = d[i]
    elif item.startswith("#"):
        k = item.strip("#")
        tmp[k] = {}
        tmp[k]["method"] = True 
        for i in d:
            tmp[k][i] = d[i]
    elif item.startswith(":"):
        tmp = {"cmd": item.strip(":")}
        for i in d:
            tmp[i] = d[i]
    else:
        tmp[item] = d
    return list_to_deep_dict(s, tmp)

if __name__ == "__main__":
    import sys
    args = sys.argv[1:]
    if args:
        res = main(args)
    else:
        print "use -h to the help"

