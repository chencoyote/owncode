#!/usr/bin/python
#!coding:utf-8


from optparse import OptionParser
import json
import Shconfig

data = {}
CLASS = '{$key:{$next}}'


def main(argv):
    parser = OptionParser(
        usage="usage clitool.py %prog -i file -o file.config...",
        description="""Make cli file to cmdconfig file , read example file
        """
    )
    parser.add_option("-i", "--input", dest="input_file", help="Input cli file", metavar="FILE")
    parser.add_option("-o", "--output", dest="output_file", help="Output file")
    
    (options, args) = parser.parse_args(argv)

    cli_dict = load_file(options.input_file)
    #print json.dumps(cli_dict, indent=4)
    root = cli_dict["root"]
    def_dict = mk_define(cli_dict)
    cmd_dict = {}
    for cmd in cli_dict.get("cmd"):
        d = cmd.split()
        dic = {d[0]:d[1]}
        cmd_dict.update(dic)
    print json.dumps(def_dict,indent=4)
    cli_list = []
    for cli in cli_dict["cli"]:
        cli_list.append(cli.split())
    render(cli_list, cmd_dict, def_dict)



def def2dict(def_dict):
    d = def_dict
    for i in d.keys():
        #print json.dumps(d[i], indent=4)
        tmp = {i:{}}
        if d[i].get("help"): 
                tmp[i]["help"] = d[i]["help"]
        cla = d[i].get("attr")
        if  cla == "class":
            d[i] = tmp
        elif cla == "token":
            tmp[i][i] = {"token":1}
            if d[i].get("help"):
                tmp[i][i]["help"] = d[i]["help"]
            d[i] = tmp
        elif cla == "method":
            tmp[i] = {"method":1}
            d[i] = tmp
    return d
    print json.dumps(d,indent=4)


def __clean_file(filepath):
    try:
        fp = open(filepath, 'w')
    except IOError:
        show_message(Code.ERROR, "Permission denied: %s" % filepath)
    #fp.truncate(0)
    fp.write("nac:{};")
    fp.close()
    return 0



def mk_define(cdict):
    define = cdict.get("define")
    define_dict = {}
    cmd_dict = {}
    help_dict = {}
    for c in cdict.get("cmd"):
        cmd_dict[c.split()[0]] = c.split()[1]
    for h in cdict.get("help"):
        help_dict[h.split()[0]] = h.split()[1]
    if define:
        for item in define:
            attribute = item.split(" ")[0]
            values = item.split(" ")[1].split(",")
            for val in values:
                t = {}
                t["attr"] = attribute
                define_dict[val] = t
                if val in cmd_dict.keys():
                    t["cmd"] = cmd_dict[val]
                if val in help_dict.keys():
                    t["help"] = help_dict[val]
    return define_dict


def load_file(path):
    try:
        ifile = open(path, "r").readlines()
    except IOError:
        print "Can't open file : %s " % (path)
    t = []
    for tmp in ifile:
        tmp = tmp.replace("\n", "")
        t.append(tmp)
    ROOT = t[0].split("=")[1]
    defin = _get_define("def", t)
    help = _get_define("help", t)
    cli = _get_define("cli", t)
    cmd = _get_define("cmd", t)
    return {"root": ROOT, "define": defin, "help": help, "cli": cli, "cmd": cmd}


def _get_define(pastr, lists):
    a = lists.index("@" + pastr)
    b = lists.index("@end" + pastr)
    return lists[a + 1:b]
        
if __name__ == "__main__":
    import sys
    args = sys.argv[1:]
    if args:
        res = main(args)
        #print res
    else:
        print "use -h to the help"
