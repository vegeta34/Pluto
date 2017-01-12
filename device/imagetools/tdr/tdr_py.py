#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import string
import datetime
import collections, re
from xml.etree import ElementTree

#xml paraser
class XmlParser(object):
        """docstring for XmlParser"""
        parsed_xmls = []

        @staticmethod
        def mdcode(str, encoding='utf-8'):
                if isinstance(str, unicode):
                        return str.encode(encoding)
                for c in ('utf-8', 'gbk', 'gb2312','gb18030','utf-16'):
                        try:
                                if encoding == 'unicode':
                                        return str.decode(c)
                                else:
                                        return str.decode(c).encode(encoding)
                        except: 
                                pass
                raise BaseException('Unknown charset')

        @staticmethod
        def parse(xml_path):
                #from other encoding to utf-8
                p = re.compile(r'encoding="\w+"')
                xml_utf8 = p.sub(r'encoding="utf-8"', XmlParser.mdcode(open(xml_path).read()), count=1)
                #print xml_utf8
                root = ElementTree.fromstring(xml_utf8)
                XmlParser.parsed_xmls.append(root)
                return root
        @staticmethod
        def get_exml_by_type(t):
                for e in XmlParser.parsed_xmls:
                        for exml in list(e):
                                if exml.get('name', '') == t:
                                        return exml
                raise BaseException("cant find type=%s in any open xmls"%t)

class ConstMgr(object):
        """docstring for ConstMgr"""
        const_dict = {}
        @staticmethod
        def cset(name, value):
                ConstMgr.const_dict[name] = value
        @staticmethod
        def cget(name):
                return ConstMgr.const_dict[name]

#output
class PObjMgr(object):
        """docstring for PObjMgr"""
        def __init__(self):
                super(PObjMgr, self).__init__()
                self._m = sys.modules['__main__']
        def oset(self, ccode):
                exec(code)
        def init(self, xml_path):
                pass
        def uinit(self):
                pass
        def include(self, xml_path):
                pass
        def test_begin(self):
                pass
        def test_oset(self, ccode):
                pass

py_head_str = """#!/usr/bin/env python
# -*- coding: utf-8 -*-
# created by tdr_py when {time_now}, you should not edit this directly...
# any questions, rtx: kevinjzhong, or mail: qq2000zhong@gmail.com
#
# note, tdr's array = python list, and array elems's num: 'Count' = len(list)
# so you should ignore this 'Count' field forever in python's world
#
import sys, string, collections, struct, random
"""
test_head_str = """
if __name__ == '__main__':
        import getopt, time
        _try_times = 100
        _buf_len = 1024000
        _output_msg = False
        options, args = getopt.getopt(sys.argv[1:], "hrpm:l:")
        for n, v in options:
                if n == '-h':
                        print "usage: " + sys.argv[0] + " -h -r -p [-m] [-l]"
                        print "\t-h=help"
                        print "\t-r=set random seed with now time, default no random seed"
                        print "\t-p=print msg, default no output"
                        print "\t-m=each class pack|unpack times, default 100"
                        print "\t-h=pack or unpack buf len, default 1024000"
                        sys.exit(0)
                if n == '-r':
                        print "random seed set with now time"
                        random.seed()
                elif n == '-p':
                        _output_msg = True
                elif n == '-m':
                        _try_times = int(v)
                elif n == '-l':
                        _buf_len = int(v)
        _b = bytearray(_buf_len)
"""

class FilePyMgr(object):
        """docstring for FilePyMgr"""
        def __init__(self):
                super(FilePyMgr, self).__init__()
        def oset(self, ccode):
                self._f.write(ccode)
                self._f.write("\n")
        def include(self, xml_path):
                self._f.write("from %s import *\n"%xml_path[:xml_path.rfind(".xml")])
        def init(self, xml_path):
                self._fpath = xml_path[:xml_path.rfind(".xml")] + ".py"
                self._f = open(self._fpath, "w")
                self._f.write(py_head_str.format(time_now=datetime.datetime.now()) + "\n")
        def uinit(self):
                print "create %s success..."%self._fpath
                self._f.close()
        def test_begin(self):
                self._f.write(test_head_str)
        def test_oset(self, ccode):
                for e in string.split(ccode, "\n"):
                        self._f.write(' '*XmlClsScanner.TAB_SIZE + e + "\n")

g_om = None
FA = collections.namedtuple('FA', 'size, format')

class FM(object):
        transfer_fields = {'byte': 'uchar', 'tinyint': 'char', 'tinyuint': 'uchar', 'smallint': 'short', 'smalluint': 'ushort', 'int8': 'char', \
                'uint8': 'uchar', 'int16': 'short', 'uint16': 'ushort', 'int32': 'int', 'uint32': 'uint', 'int64': 'long', 'uint64': 'ulong', \
                'bigint': 'long', 'biguint': 'ulong'}

        int_fields = {'char':FA(1, 'b'), 'uchar':FA(1, 'B'), \
                'short': FA(2, 'h'), 'ushort': FA(2, 'H'), \
                'int': FA(4, 'i'), 'uint': FA(4, 'I'), 'long': FA(8, 'q'), 'ulong': FA(8, 'Q'), \
                'float': FA(4, 'f'), 'dobule': FA(8, 'd'), \
                'date': FA(4, 'I'), 'time': FA(4, 'I'), 'datetime': FA(8, 'q')}

        @staticmethod
        def init():
                for k, v in FM.int_fields.iteritems():
                        g_om.oset("_struct_%s=struct.Struct('!%s')"%(k, v.format))

        @staticmethod
        def get_type(e):
                if e.tag == 'union' or e.tag == 'struct':
                        return e.tag
                t = FM.transfer_fields.get(e.get('type').lower(), None)
                return t if t else e.get('type')
        @staticmethod
        def get_ptype(e, raw=False):
                if (not raw):
                        if FM.is_array(e):
                                return 'list()'
                        if FM.is_tuple(e):
                                return '[' + ((FM.get_ptype(e, True) + ",") * FM.get_tuple_size(e)) [:-1]+ ']'
                if FM.is_cls(e):
                        return e.tag + "()"
                t = FM.get_type(e)
                if t == 'float' or t == 'dobule':
                        return 'float()'
                elif t in FM.int_fields:
                        return 'int()'
                elif t == 'string':
                        return 'str()'
                else:
                        return t + "()"
        @staticmethod
        def is_cls(e):
                return e.tag == 'union' or e.tag == 'struct'                        
        @staticmethod
        def is_base_fields(t):
                return t in FM.int_fields or t == 'string'
        @staticmethod
        def is_array(e):
                return e.get('count') != None and e.get('refer') != None
        @staticmethod
        def is_tuple(e):
                return e.get('count') != None and e.get('refer') == None
        @staticmethod
        def get_tuple_size(e):
                count = e.get('count')
                return int(count if count.isdigit() else ConstMgr.cget(count))

        @staticmethod
        def get_bversion(e):
                return int(e.get('version', '0'))
        @staticmethod
        def get_version(e):
                "return 0 - no version"
                #print e.tag, e.get('name'), e.get('type')
                t = FM.get_type(e)
                v = FM.get_bversion(e)
                if FM.is_base_fields(t):
                        return v
                elif e.tag == 'entry':
                        return FM.get_version(XmlParser.get_exml_by_type(t))
                elif FM.is_cls(e):
                        return max(v, max([FM.get_version(ec) for ec in list(e)]))
                else:
                        raise BaseException("cant get version from e=%s"%(e.tag))

        @staticmethod
        def get_offset(e, depth):
                "just support fixed offset"
                offset = 0
                ecs = (list(e) if FM.is_cls(e) else XmlParser.get_exml_by_type(e.get('type')))[:depth[0]+1]
                #print e.tag, e.get('name'), depth, ", ecs:", len(ecs)#, list(e)
                for ec in ecs[:-1]:
                        t = FM.get_type(ec)
                        if (t not in FM.int_fields) or FM.is_array(ec):
                                print "still not support unfixed offset, cause ec=", ec.get('name')
                                sys.exit(-1)
                        if FM.is_tuple(ec):
                                offset += (FM.int_fields[t].size * FM.get_tuple_size(ec))
                        else:
                                offset += FM.int_fields[t].size
                return offset if len(depth)==1 else FM.get_offset(ecs[-1], depth[1:])

        @staticmethod
        def create_pack_code(e, voffset_name='buf_offset', value_name=None):
                t = FM.get_type(e)
                name = value_name if value_name else 'self.%s'%e.get('name')
                if t in FM.int_fields:
                        fld = FM.int_fields[t]
                        return "%s.pack_into(dest_buf, %s, %s); %s += %d"%('_struct_'+t, voffset_name, name, voffset_name, fld.size)
                if t == "string":
                        return "_s = %s+'\\0'; _len = len(_s); _struct_int.pack_into(dest_buf, %s, _len); %s += 4;"%(name, voffset_name, voffset_name) + \
                                "dest_buf[%s:%s+_len] = _s; %s += _len"%(voffset_name, voffset_name, voffset_name)

        @staticmethod
        def create_unpack_code(e, voffset_name='buf_offset', value_name=None):
                t = FM.get_type(e)
                name = value_name if value_name else 'self.%s'%e.get('name')
                if t in FM.int_fields:
                        fld = FM.int_fields[t]
                        return "%s = %s.unpack_from(src_buf, %s)[0]; %s += %d"%(name, '_struct_'+t, voffset_name, voffset_name, fld.size)
                if t == "string":
                        return "_len = _struct_int.unpack_from(src_buf, %s)[0]; %s += 4;"%(voffset_name, voffset_name) + \
                                "%s = src_buf[%s:%s+_len-1]; %s += _len"%(name, voffset_name, voffset_name, voffset_name)
#
# driver
#
class XmlClsScanner(object):
        """docstring for XmlClsScanner"""
        TAB_SIZE = 8
        def __init__(self, root):
                super(XmlClsScanner, self).__init__()
                self.tab_offset = 0
                self._root = root
                self._top_exml = None
                self._tpl = ""
                self._opfn = None

        def create(self, e):
                self._top_exml = e
                self._vcode = []
                clsattrs = {'clsname': e.get('name') , 'BASEVERSION': FM.get_bversion(e), 'CURRVERSION': FM.get_version(e), \
                                'selector' : 'selector, ' if e.tag == 'union' else ''}
                print e.get('name'), clsattrs
                scode = self._tpl.format(**clsattrs)
                for es in string.split(scode, "\n"):
                        ses = es.strip()
                        if not ses or ses[0] != '$':
                                self._vcode.append(es)
                                continue
                        self.tab_offset = es.index('$') / ClassCreator.TAB_SIZE
                        exec(ses[1:])
                self._opfn(string.join(self._vcode, "\n"))

        def add_lcode(self, *scode):
                for e in scode:
                        #print self.tab_offset, scode
                        self._vcode.append(' '*(XmlClsScanner.TAB_SIZE*self.tab_offset) + e)

clsTpl = """
class {clsname}(object):
        CURRVERSION = {CURRVERSION}
        __slots__ = [\\
                $self.add_lcode(string.join(['"%s"'%(ec.get('name')) for ec in list(e)], ",") + (', "_selector"' if e.tag == 'union' else '') + "\\\\")
        ]
        def __init__(self):
                $for ec in list(e): self.add_lcode('self.%s = %s'%(ec.get('name'), FM.get_ptype(ec)))
                $if e.tag == 'union': self.add_lcode('self._selector = 0')

        def __eq__(self, rh):
                $if e.tag == 'union': self.add_lcode('if self._selector != rh._selector: return False')
                $for ec in list(e): self._eq_field(e, ec)
                return True
        def __ne__(self, rh):
                return not (self == rh)

        def __str__(self):
                vstr = []
                $for ec in list(e): self._str_field(e, ec)
                return "{clsname}:<" + string.join(vstr, "; ") + ">"
        __repr__ = __str__

        def _adjust_iversion(self, cur_version):
                if 0 == cur_version or {CURRVERSION} < cur_version:
                        cur_version = {CURRVERSION}
                if {BASEVERSION} > cur_version:
                        print "illegal cur_version=%d, BASEVERSION={BASEVERSION}"%(cur_version)
                        return -1
                return cur_version
        def _check_nversion(self, net_version):
                if {BASEVERSION} > net_version or net_version > {CURRVERSION}:
                        print "illegal net_version=%d, CURRVERSION={CURRVERSION}"%(net_version)
                        return -1
                return net_version

        def value_random(self):
                $if e.tag == 'union': self._random_selector(e)
                $for ec in list(e): self._random_field(ec)

        def pack(self, {selector} dest_buf, cur_version=0, buf_offset=0):
                "if success, ret last buf_offset, else return < 0"
                $if e.tag == 'union': self.add_lcode('self._selector = selector')
                buf_start = buf_offset
                cur_version = self._adjust_iversion(cur_version)
                if cur_version < 0:
                        return -1
                $self.up_sizeinfo_head(e)
                $self.pack_fields(e)
                $self.set_versionindicator(e)
                $self.up_sizeinfo_tail(e)
                return buf_offset

        def unpack(self, {selector} src_buf, buf_len, cur_version=0, buf_offset=0):
                "if success, ret last buf_offset, err return < 0, =0 need more data"
                $if e.tag == 'union': self.add_lcode('self._selector = selector')
                buf_start = buf_offset
                $self.up_sizeinfo_head(e, False)
                $self.unpack_version(e)
                $self.unpack_fields(e)
                $self.up_sizeinfo_tail(e, False)
                return buf_offset
"""

class ClassCreator(XmlClsScanner):
        """docstring for ClassCreator"""
        def __init__(self, root):
                super(ClassCreator, self).__init__(root)
                self._tpl = clsTpl
                self._opfn = g_om.oset

        @staticmethod
        def _find_by_path(e, dot_path):
                depth = []
                for i, ec in enumerate(list(e)):
                        if ec.get('name') == dot_path[0]:
                                depth.append(i)
                                if len(dot_path) == 1:
                                        return ec, depth
                                ec = XmlParser.get_exml_by_type(ec.get('type'))
                                ec, cdepth = ClassCreator._find_by_path(ec, dot_path[1:])
                                depth.extend(cdepth)
                                return ec, depth
                raise BaseException("cant find path(%s) in %s:%s"%(string.join(dot_path, "."), e.tag, e.get('name')))

        def _find(self, str_path):
                #print str_path
                return self._find_by_path(self._top_exml, string.split(str_path, '.'))

        #eq
        def _eq_field(self, e, ec):
                name = ec.get('name')
                if e.tag == 'union':
                        self.add_lcode('if self._selector == %s and self.%s != rh.%s: return False'%(ec.get('id'), name, name))
                else:
                        self.add_lcode('if self.%s != rh.%s: return False'%(ec.get('name'), name))

        #str
        def _str_field(self, e, ec):
                name = ec.get('name')
                astr = 'vstr.append("%s={%%s}"%%self.%s)'%(name, name)
                if e.tag == 'union':
                        self.add_lcode('if self._selector == %s:'%ec.get('id') + astr)
                else:
                        self.add_lcode(astr)

        #random
        def _random_selector(self, e):
                selectors = []
                for ec in list(e):
                        selectors.append(ec.get('id'))
                self.add_lcode('self._selector = random.choice([%s])'%string.join(selectors, ','))

        def _random_field_content(self, ec, vn):
                t = FM.get_type(ec)
                if t in FM.int_fields:
                        if t == 'float':
                                self.add_lcode('%s = struct.unpack("f", struct.pack("f", random.random() * 9999))[0]'%vn)
                        elif t == 'dobule':
                                self.add_lcode('%s = struct.unpack("f", struct.pack("f", random.random() * 9999999))[0]'%vn)
                        else:
                                bit_num = FM.int_fields[t].size*8 - 1
                                self.add_lcode('%s = int(random.random()*((1<<%d)-1))'%(vn, bit_num))
                elif t == 'string':
                        #from  assic 32 -> 126
                        self.add_lcode('%s = "%%c"%%(int(random.random()*94) + 32)*%s'%(vn, ec.get('size')))
                else:
                        self.add_lcode('%s.value_random()'%vn)

        def _random_field(self, ec):
                vn = 'self.%s'%ec.get('name')
                if FM.is_array(ec):
                        self.add_lcode('_len = int(random.random()*%s)'%(ec.get('count')))
                        self.add_lcode('%s = []'%vn)
                        self.add_lcode('for i in range(_len):')
                        self.tab_offset += 1
                        self.add_lcode('%s.append(%s)'%(vn, FM.get_ptype(ec, True)))
                        self._random_field_content(ec, "%s[i]"%vn)
                        self.tab_offset -= 1
                elif FM.is_tuple(ec):
                        self.add_lcode('for i in range(%d):'%FM.get_tuple_size(ec))
                        self.tab_offset += 1
                        self._random_field_content(ec, "%s[i]"%vn)
                        self.tab_offset -= 1
                else:
                        self._random_field_content(ec, vn)

        #pack & unpack's common utils method----
        def _up_path(self, str_path, pack=True):
                e = self._top_exml
                target_ec, depth = self._find(str_path)
                target_offset = FM.get_offset(self._top_exml, depth)
                print "_up_path: ", e.tag, e.get('name'), str_path, "offset=", target_offset
                self.add_lcode('_tmp_pos = buf_start + %s'%target_offset, \
                        (FM.create_pack_code if pack else FM.create_unpack_code)(target_ec, voffset_name='_tmp_pos', value_name='self.%s'%str_path))

        def _up_fields(self, e, pack=True):
                for ec in list(e):
                        if e.tag == 'union':
                                self.add_lcode('if selector == %s:'%ec.get('id'))
                                self.tab_offset += 1
                        self._up_field(ec, pack)
                        if e.tag == 'union':
                                self.tab_offset -= 1

        def _up_field(self, e, pack=True):
                #version-head
                v = FM.get_bversion(e)
                if v:
                        self.add_lcode('if %d <= cur_version:'%(v))
                        self.tab_offset += 1
                (self._pack_field if pack else self._unpack_field)(e)
                #version-tail
                if v:
                        self.tab_offset -= 1

        def _up_field_content(self, e, vn, pack=True):
                t = FM.get_type(e)
                if FM.is_base_fields(t):
                        self.add_lcode((FM.create_pack_code if pack else FM.create_unpack_code)(e, value_name=vn))
                        return
                method = "pack" if pack else "unpack"
                buf_len = "" if pack else "buf_len,"
                buf_name = "dest_buf" if pack else "src_buf"
                union_select = e.get('select')
                if union_select:
                        self.add_lcode("buf_offset = %s.%s(self.%s, %s, %s cur_version, buf_offset)"%(vn, method, union_select, buf_name, buf_len))
                else:
                        self.add_lcode("buf_offset = %s.%s(%s, %s cur_version, buf_offset)"%(vn, method, buf_name, buf_len))
                self.add_lcode("if buf_offset <= 0: return buf_offset")

        def up_sizeinfo_head(self, e, pack=True):
                sizeinfo = e.get('sizeinfo')
                if not sizeinfo:
                        return
                t = e.get('type')
                value_name = 'buf_start'
                if t:
                        value_name = "%s_%s"%(e.get('name'), t)
                        self.add_lcode('%s = buf_offset'%value_name)
                if not pack:
                        self._up_path(sizeinfo, False)
                        self.add_lcode('if self.%s > buf_len - %s: return 0'%(sizeinfo, value_name))

        def up_sizeinfo_tail(self, e, pack=True):
                sizeinfo = e.get('sizeinfo')
                if not sizeinfo:
                        return
                t = e.get('type')
                value_name = "%s_%s"%(e.get('name'), t) if t else 'buf_start'
                if pack:
                        self.add_lcode('self.%s = buf_offset - %s'%(sizeinfo, value_name))
                        self._up_path(sizeinfo)
                else:
                        #important, may read < sizeinfo's size
                        self.add_lcode('buf_offset = self.%s + %s'%(sizeinfo, value_name))

        # pack------
        def pack_fields(self, e):
                #if pack, set array len's refer val from len(array)
                for ec in list(e):
                        if FM.is_array(ec):
                                self.add_lcode('self.%s = len(self.%s)'%(ec.get('refer'), ec.get('name')))
                self._up_fields(e)

        def _pack_field(self, e):
                #sizeinfo-head
                self.up_sizeinfo_head(e)
                #field-self
                vn = 'self.%s'%e.get('name')
                if FM.is_tuple(e):
                        self.add_lcode('assert len(%s) == %d'%(vn, FM.get_tuple_size(e)))
                if FM.is_array(e) or FM.is_tuple(e):
                        self.add_lcode('for ea in %s:'%vn)
                        self.tab_offset += 1
                        self._up_field_content(e, 'ea')
                        self.tab_offset -= 1
                else:
                        self._up_field_content(e, vn)

                #sizeinfo-tail
                self.up_sizeinfo_tail(e)

        def set_versionindicator(self, e):
                versionindicator = e.get('versionindicator')
                if versionindicator:
                        self.add_lcode('self.%s = cur_version'%versionindicator)
                        self._up_path(versionindicator)
        #unpack
        def unpack_fields(self, e):
                self._up_fields(e, False)

        def _unpack_field(self, e):
                #sizeinfo-head
                self.up_sizeinfo_head(e, False)
                sizeinfo = e.get('sizeinfo')

                #field-self
                vn = 'self.%s'%e.get('name')
                if FM.is_array(e):
                        self.add_lcode('%s = []'%vn)
                        self.add_lcode('for i in range(self.%s):'%e.get('refer'))
                        self.tab_offset += 1
                        self.add_lcode('%s.append(%s)'%(vn, FM.get_ptype(e, True)))
                        self._up_field_content(e, '%s[i]'%vn, False)
                        self.tab_offset -= 1
                elif FM.is_tuple(e):
                        self.add_lcode('for i in range(%d):'%FM.get_tuple_size(e))
                        self.tab_offset += 1
                        self._up_field_content(e, '%s[i]'%vn, False)
                        self.tab_offset -= 1
                else:
                        self._up_field_content(e, vn, False)

                #sizeinfo-tail
                self.up_sizeinfo_tail(e, False)

        def unpack_version(self, e):
                versionindicator = e.get('versionindicator')
                if not versionindicator:
                        self.add_lcode('cur_version = self._adjust_iversion(cur_version)', 'if cur_version < 0: return -1')
                        return
                self._up_path(versionindicator, False)
                self.add_lcode('cur_version = self._check_nversion(self.%s)'%versionindicator, 'if cur_version < 0: return -1')

testTpl = """
_packed = {clsname}()
_unpacked = {clsname}()
_packed.value_random()
_bl = _packed.pack(_b, {CURRVERSION})
if _output_msg:
        print _packed
_rbl = _unpacked.unpack(_b, _bl / 2)
if _rbl == 0:
        print "%-28s support frame, you know what i mean..."%('{clsname}')
_time_start = time.time()
for x in xrange(_try_times):
        _bl = _packed.pack(_b, {CURRVERSION})
        _rbl = _unpacked.unpack(_b, _bl)
        if _bl != _rbl:
                print _packed
                raise BaseException("pack_len=%d != unpack_len=%d"%(_bl, _rbl))
        if _packed != _unpacked:
                print _packed
                print _unpacked
                raise BaseException("pack cls != unpack cls")
print "%-28s pack<->unpack %10d times in %6d seconds......."%('{clsname}', _try_times, time.time() - _time_start)
"""
# testor creator
class ClsTestorCreator(XmlClsScanner):
        """docstring for ClsTestorCreator"""
        def __init__(self, root):
                super(ClsTestorCreator, self).__init__(root)
                self._tpl = testTpl
                self._opfn = g_om.test_oset
#
#interface class
#
class TdrXml2Py(object):
        """docstring for TdrXml2Py"""
        def __init__(self):
                super(TdrXml2Py, self).__init__()

        def x_include(self, e):
                child_parser = TdrXml2Py()
                child_parser.parse(e.get("file"))

        def x_macro(self, e):
                ConstMgr.cset(e.get("name"), e.get("value"))
                g_om.oset("%s = %s"%(e.get("name"), e.get("value")))

        def x_macrosgroup(self, e):
                for ec in list(e):
                        assert ec.tag == "macro"
                        self.x_macro(ec)
        
        def x_union(self, e):
                for ec in list(e):
                        assert ec.tag == "entry"
                ClassCreator(self._root).create(e)
        x_struct = x_union

        def parse(self, xml_path):
                global g_om
                org_gom = g_om
                if org_gom:
                        org_gom.include(xml_path)
                g_om = FilePyMgr()
                g_om.init(xml_path)
                FM.init()

                root = XmlParser.parse(xml_path)
                self._root = root

                #create class code
                for ec in list(root):
                        pf = getattr(self, "x_"+ec.tag, None)
                        if not pf:
                                print "err tag: ", ec.tag
                                sys.exit(-1)
                        pf(ec)

                g_om.test_begin()
                #create test code
                for ec in list(root):
                        if ec.tag == 'struct':
                                ClsTestorCreator(self._root).create(ec)
                g_om.uinit()
                g_om = org_gom

def main(xml_path):
        TdrXml2Py().parse(xml_path)

if __name__ == '__main__':
        if len(sys.argv) < 2:
                print "usage: %s xml_path"%(sys.argv[0])
                sys.exit(-2)
        main(sys.argv[1])
