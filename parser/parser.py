#
# -*- coding: utf-8 -*-


import json
import sys
import codecs

UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)

def print_names(path):
    for l in open(path):
        item=json.loads(l)
        try:
            print item['name'][0]
        except:
            pass

if __name__ == '__main__':
    try:
        print_names(sys.argv[1])
    except Exception, e:
        print e
        print "usage: %s [path]" % sys.argv[0]

