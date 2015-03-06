#
# -*- coding: utf-8 -*-


import json
import sys
import codecs
import numpy as np
import traceback

UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)


def escape(f):
    def f_esc(*args):
        ret = f(*args)
        if ret is None:
            ret = ''
        ret = "%s" % ret
        return ret.replace('\t','').replace('\r', '').replace('\n', '')
    return f_esc


def none2empty(f):
    def f_none(*args):
        ret = f(*args)
        if ret is None:
            return ''
        return ret
    return f_none


def to_unicode(string):
    return unicode(string.replace('\r', '').replace('\n',''), 'utf-8')


@escape
def try_get(item, *index):
    tmp = item
    for i in index:
        if type(tmp) == dict:
            tmp = tmp.get(i)
        elif type(tmp) == list:
            if len(tmp) > i:
                tmp = tmp[i]
            else:
                tmp = None
        if tmp is None:
            return None
    return tmp


def classify_items(path):
    """

    """
    cls = 1


class Label:
    def __init__(self, l_id, names, l_type='type'):
        self.l_id = l_id
        self.names = names
        self.parent = None
        self.l_type = l_type
        self.sub = []


class LabelGroup:
    def __init__(self, name, fields, group_type='attr', allow_multiple=False):
        self.name = name
        self.fields = fields
        self.group_type = group_type
        self.allow_multiple = allow_multiple
        self.labels = []

    def match(self, text):
        """
        将text和本组立面的label比较，找出匹配的
        """
        ret = []
        for l in self.labels:
            for n in l.names:
                if text.find(n) >= 0:
                    ret.append(l)
                    break
            if len(ret) > 0:
                if self.group_type == 'type':
                    self.match_sub(l, text, ret)
                    break
                elif not self.allow_multiple:
                    break
        return ret

    def match_sub(self, label, text, result):
        for l in label.sub:
            for n in l.names:
                if text.find(n) >= 0:
                    result.append(l)
                    if len(l.sub) > 0:
                        self.match_sub(l, text, result)
                    return


class LabelMap:

    def __init__(self):
        self.name2labels = {}
        self.fields2lg = {}
        self.id2labels = []
        self.global_attr_groups = []    # [label_group0, label_group1]
        self.item_type_groups = []      # [label_group0, label_group1]
        self.item_attr_groups = []      # [[l_g00, l_g01],[l_g10,l_g11]]
        self.next_id = 0

    def new_label(self, names, l_type='type'):
        label = Label(self.next_id, names, l_type)
        self.next_id += 1
        self.id2labels.append(label)
        for n in names:
            self.name2labels[n] = label
        return label

    def label_byname(self, name):
        return self.name2labels.get(name)

    def label_byid(self, l_id):
        return self.id2labels[l_id]

    def load(self, path):
        """
        import labels from file
        label有名字，序号0-based，类型[type, attr]
        """
        cur_labelgroup = None
        cur_parentlabel = None
        last_label = None
        cur_indent = 0
        for l in open(path):
            l = to_unicode(l)
            l_s = l.strip()
            if l_s == '' or l_s.startswith('#'):
                continue
            if l.startswith('='):
                #new labelgroup
                cur_parentlabel = None
                last_label = None
                cur_indent = 0
                tk = l.split()
                group_type, allow_multi = {
                        '0': lambda: ('attr', True),
                        '1': lambda: ('attr', False),
                        '2': lambda: ('type', False),
                }[tk[-1]]()
                cur_labelgroup = LabelGroup(tk[1], tk[2:-1], group_type, allow_multi)
                for f in cur_labelgroup.fields:
                    self.fields2lg[f] = cur_labelgroup
                if group_type == 'attr':
                    if len(self.item_type_groups) == 0: # global attr_group
                        self.global_attr_groups.append(cur_labelgroup)
                    else: # item attr_group
                        self.item_attr_groups[len(self.item_type_groups)-1].append(cur_labelgroup)
                elif group_type == 'type': # new item type
                    self.item_type_groups.append(cur_labelgroup)
                    self.item_attr_groups.append([])
                else:
                    raise Exception('unknown group_type:%s' % group_type)
                pass
            else:
                #new label
                tk = l.split('    ')  # count indent
                indent = len(tk) - 1
                if indent > cur_indent:  # new indent
                    cur_parentlabel = last_label
                    cur_indent = indent
                elif indent < cur_indent:
                    for i in range(cur_indent - indent):
                        if cur_parentlabel is not None:
                            cur_parentlabel = cur_parentlabel.parent
                    cur_indent = indent
                tk = tk[-1].split(' ')
                label = self.new_label(tk, cur_labelgroup.group_type)

                if cur_parentlabel is not None:
                    label.parent = cur_parentlabel
                    cur_parentlabel.sub.append(label)
                cur_labelgroup.labels.append(label)

                last_label = label
                pass


def export_labels(label_path):
    lm = LabelMap()
    lm.load(label_path)
    l_id = 0
    for l in lm.id2labels:
        if type(l.names) == list:
            n = l.names[0]
        else:
            n = l.names
        print "%d\t%s" % (l_id, n)
        l_id += 1
    pass


def fill_all(label_group, vector, default_value=-1):
    start_index, end_index = label_group.labels[0].l_id, label_group.labels[-1].l_id
    vector[start_index:end_index+1] = default_value


def lookup_label_in(item, label_group):
    name = try_get(item, 'name', 0)
    found_labels = []
    for field in label_group.fields:
        field_value = try_get(item, field)
        labels = label_group.match(field_value)
        found_labels += labels
        if len(labels) > 0 and not label_group.allow_multiple:
            break
    if len(found_labels) == 0 or label_group.allow_multiple:
        labels = label_group.match(name)
        found_labels += labels
    return found_labels


def lookup_label_fill_in(item, label_group, vector):
    """
    在 item[label_group.field] 和 item['name'] 两个字段里面查找这个LabelGroup的所有标签，
    并且在label vector里面赋值
    """
    found_labels = lookup_label_in(item, label_group)
    if len(found_labels) == 0:
        fill_all(label_group, vector, 0)
    else:
        fill_all(label_group, vector, -1)
        for l in found_labels:
            vector[l.l_id] = 1
    return found_labels

def export_images(label_path, item_path):
    """
    解析 item_path对应的 scrapy item json，
    输出每个image对应的label

    """
    lm = LabelMap()
    lm.load(label_path)
    for line in open(item_path):
        item = json.loads(line)
        l_vector = np.zeros(len(lm.id2labels), dtype=np.int8)
        try:
            name = try_get(item, 'name', 0)
            """
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
            girdle = try_get(item, 'girdle')
            hardness = try_get(item, 'hardness')
            shape = try_get(item, 'shape')
            case_handle = try_get(item, 'case_handle')
            wheel = try_get(item, 'wheel')
            """
            #先判断物品的类型
            type_group = None
            type_labels = None
            item_attr_groups = None
            found_labels = []
            # 找物品类型
            for i in range(len(lm.item_type_groups)):
                t_group = lm.item_type_groups[i]
                labels = t_group.match(name)
                if len(labels) > 0:
                    type_group = t_group
                    type_labels = labels
                    item_attr_groups = lm.item_attr_groups[i]
                    break
            found_labels += type_labels
            # 根据物品类型，确定那些labelGroup需要赋值。
            # 不属于此物品类型的，全部 -1
            # 对于需要的LabelGroup，找到的label 1, 其余-1；一个label都找不到，全体0
            # 每个LabelGroup：先从所属的fields 里面找，然后从names里面找

            # 找共有属性
            for global_attr in lm.global_attr_groups:
                found_labels += lookup_label_fill_in(item, global_attr, l_vector)
            # 类型属性
            for t_group in lm.item_type_groups:
                fill_all(t_group, l_vector, -1)
                if t_group is type_group:
                    for l in type_labels:
                        l_vector[l.l_id] = 1
            # 类型的物品属性
            for t_groups in lm.item_attr_groups:
                if t_groups is item_attr_groups:
                    for t_group in t_groups:
                        found_labels += lookup_label_fill_in(item, t_group, l_vector)
                else:
                    for t_group in t_groups:
                        fill_all(t_group, l_vector, -1)

            # l_string = " ".join(np.asarray(l_vector, dtype=np.str))
            l_string = u" ".join([x.names[0] for x in found_labels])
            print "type: %s" % (u"".join([x.names[0] for x in type_labels]))
            images = item['images']
#            for image in images:
#                print "%s %s" % (l_string, image['path'])

            # print "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s"
            # % (name, material, collar, pattern, thickness, style, brand, sleeve, zipper,
            # shoe_head, heel, handle, girdle, hardness, shape, case_handle, wheel)
        except Exception, e:
            print e
            print traceback.format_exc()
            pass

    pass


def parse_items(path):
    for l in open(path):
        item = json.loads(l)
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
            girdle = try_get(item, 'girdle')
            hardness = try_get(item, 'hardness')
            shape = try_get(item, 'shape')
            case_handle = try_get(item, 'case_handle')
            wheel = try_get(item, 'wheel')
            print "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (name, material, collar, pattern, thickness, style, brand, sleeve, zipper, shoe_head, heel, handle, girdle, hardness, shape, case_handle, wheel)
        except Exception,e:
            print e
            pass


if __name__ == '__main__0':
    try:
        parse_items(sys.argv[1])
    except Exception, e:
        print e
        print "usage: %s [path]" % sys.argv[0]

if __name__ == '__main__':
    try:
        export_images(sys.argv[1], sys.argv[2])
    except Exception, e:
        print e
        print "usage: %s [label_path] [item_path]" % sys.argv[0]

