#
# -*- coding: utf-8 -*-


import json
import sys
import codecs

UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)

def escape(f):
    def f_esc(*args):
        ret = f(*args)
        if ret == None:
            ret = ''
        ret = "%s" % ret
        return ret.replace('\t','').replace('\r', '').replace('\n', '')
    return f_esc

def none2empty(f):
    def f_none(*args):
        ret = f(*args)
        if ret == None:
            return ''
        return ret
    return f_none


@escape
def try_get(item, *index):
    tmp=item
    for i in index:
        if type(tmp)==dict:
            tmp = tmp.get(i)
        elif type(tmp)==list:
            if len(tmp) > i:
                tmp = tmp[i]
            else:
                tmp = None
        if tmp == None:
            return None
    return tmp

def parse_items(path):
    for l in open(path):
        item=json.loads(l)
        try:
            name = try_get(item, 'name', 0)
            material = try_get(item, 'material')
            collar = try_get(item, 'collar')
            pattern = try_get(item, 'pattern')
            thickness = try_get(item, 'thickness')
            style = try_get(item, 'style')
            brand = try_get(item, 'brand')
            sleeve = try_get(item, 'sleeve')
            zipper = try_get(item, 'zipper')
            shoe_head = try_get(item, 'shoe_head')
            heel = try_get(item, 'heel')
            handle = try_get(item, 'handle')
            print "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (name, material, collar, pattern, thickness, style, brand, sleeve, zipper, shoe_head, heel, handle)
        except Exception,e:
            print e
            pass

if __name__ == '__main__':
    try:
        parse_items(sys.argv[1])
    except Exception, e:
        print e
        print "usage: %s [path]" % sys.argv[0]

