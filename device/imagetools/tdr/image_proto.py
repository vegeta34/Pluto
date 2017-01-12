#!/usr/bin/env python
# -*- coding: utf-8 -*-
# created by tdr_py when 2016-12-27 11:58:42.351000, you should not edit this directly...
# any questions, rtx: kevinjzhong, or mail: qq2000zhong@gmail.com
#
# note, tdr's array = python list, and array elems's num: 'Count' = len(list)
# so you should ignore this 'Count' field forever in python's world
#
import sys, string, collections, struct, random

_struct_ulong=struct.Struct('!Q')
_struct_int=struct.Struct('!i')
_struct_float=struct.Struct('!f')
_struct_datetime=struct.Struct('!q')
_struct_char=struct.Struct('!b')
_struct_uint=struct.Struct('!I')
_struct_date=struct.Struct('!I')
_struct_short=struct.Struct('!h')
_struct_uchar=struct.Struct('!B')
_struct_ushort=struct.Struct('!H')
_struct_long=struct.Struct('!q')
_struct_dobule=struct.Struct('!d')
_struct_time=struct.Struct('!I')
VERSION = 1
PKG_MAX_BODY_LEN = 200000

class CsPkgBody(object):
        CURRVERSION = 1
        __slots__ = [\
                "AllocSvrReq","AllocSvrRes","UploadTestImgWithTestIDReq","UploadErrorInfoReq","ReportUIIssueReq", "_selector"\
        ]
        def __init__(self):
                self.AllocSvrReq = AllocSvrReq()
                self.AllocSvrRes = AllocSvrRes()
                self.UploadTestImgWithTestIDReq = UploadTestImgWithTestIDReq()
                self.UploadErrorInfoReq = UploadErrorInfoReq()
                self.ReportUIIssueReq = ReportUIIssueReq()
                self._selector = 0

        def __eq__(self, rh):
                if self._selector != rh._selector: return False
                if self._selector == CMD_ALLOC_SVR_REQ and self.AllocSvrReq != rh.AllocSvrReq: return False
                if self._selector == CMD_ALLOC_SVR_RES and self.AllocSvrRes != rh.AllocSvrRes: return False
                if self._selector == CMD_UPLOAD_TEST_IMG_WITH_TESTID_REQ and self.UploadTestImgWithTestIDReq != rh.UploadTestImgWithTestIDReq: return False
                if self._selector == CMD_UPLOAD_ERROR_INFO_REQ and self.UploadErrorInfoReq != rh.UploadErrorInfoReq: return False
                if self._selector == CMD_REPORT_UI_ISSUE_REQ and self.ReportUIIssueReq != rh.ReportUIIssueReq: return False
                return True
        def __ne__(self, rh):
                return not (self == rh)

        def __str__(self):
                vstr = []
                if self._selector == CMD_ALLOC_SVR_REQ:vstr.append("AllocSvrReq={%s}"%self.AllocSvrReq)
                if self._selector == CMD_ALLOC_SVR_RES:vstr.append("AllocSvrRes={%s}"%self.AllocSvrRes)
                if self._selector == CMD_UPLOAD_TEST_IMG_WITH_TESTID_REQ:vstr.append("UploadTestImgWithTestIDReq={%s}"%self.UploadTestImgWithTestIDReq)
                if self._selector == CMD_UPLOAD_ERROR_INFO_REQ:vstr.append("UploadErrorInfoReq={%s}"%self.UploadErrorInfoReq)
                if self._selector == CMD_REPORT_UI_ISSUE_REQ:vstr.append("ReportUIIssueReq={%s}"%self.ReportUIIssueReq)
                return "CsPkgBody:<" + string.join(vstr, "; ") + ">"
        __repr__ = __str__

        def _adjust_iversion(self, cur_version):
                if 0 == cur_version or 1 < cur_version:
                        cur_version = 1
                if 1 > cur_version:
                        print "illegal cur_version=%d, BASEVERSION=1"%(cur_version)
                        return -1
                return cur_version
        def _check_nversion(self, net_version):
                if 1 > net_version or net_version > 1:
                        print "illegal net_version=%d, CURRVERSION=1"%(net_version)
                        return -1
                return net_version

        def value_random(self):
                self._selector = random.choice([CMD_ALLOC_SVR_REQ,CMD_ALLOC_SVR_RES,CMD_UPLOAD_TEST_IMG_WITH_TESTID_REQ,CMD_UPLOAD_ERROR_INFO_REQ,CMD_REPORT_UI_ISSUE_REQ])
                self.AllocSvrReq.value_random()
                self.AllocSvrRes.value_random()
                self.UploadTestImgWithTestIDReq.value_random()
                self.UploadErrorInfoReq.value_random()
                self.ReportUIIssueReq.value_random()

        def pack(self, selector,  dest_buf, cur_version=0, buf_offset=0):
                "if success, ret last buf_offset, else return < 0"
                self._selector = selector
                buf_start = buf_offset
                cur_version = self._adjust_iversion(cur_version)
                if cur_version < 0:
                        return -1
                if selector == CMD_ALLOC_SVR_REQ:
                        buf_offset = self.AllocSvrReq.pack(dest_buf,  cur_version, buf_offset)
                        if buf_offset <= 0: return buf_offset
                if selector == CMD_ALLOC_SVR_RES:
                        buf_offset = self.AllocSvrRes.pack(dest_buf,  cur_version, buf_offset)
                        if buf_offset <= 0: return buf_offset
                if selector == CMD_UPLOAD_TEST_IMG_WITH_TESTID_REQ:
                        buf_offset = self.UploadTestImgWithTestIDReq.pack(dest_buf,  cur_version, buf_offset)
                        if buf_offset <= 0: return buf_offset
                if selector == CMD_UPLOAD_ERROR_INFO_REQ:
                        buf_offset = self.UploadErrorInfoReq.pack(dest_buf,  cur_version, buf_offset)
                        if buf_offset <= 0: return buf_offset
                if selector == CMD_REPORT_UI_ISSUE_REQ:
                        buf_offset = self.ReportUIIssueReq.pack(dest_buf,  cur_version, buf_offset)
                        if buf_offset <= 0: return buf_offset
                return buf_offset

        def unpack(self, selector,  src_buf, buf_len, cur_version=0, buf_offset=0):
                "if success, ret last buf_offset, err return < 0, =0 need more data"
                self._selector = selector
                buf_start = buf_offset
                cur_version = self._adjust_iversion(cur_version)
                if cur_version < 0: return -1
                if selector == CMD_ALLOC_SVR_REQ:
                        buf_offset = self.AllocSvrReq.unpack(src_buf, buf_len, cur_version, buf_offset)
                        if buf_offset <= 0: return buf_offset
                if selector == CMD_ALLOC_SVR_RES:
                        buf_offset = self.AllocSvrRes.unpack(src_buf, buf_len, cur_version, buf_offset)
                        if buf_offset <= 0: return buf_offset
                if selector == CMD_UPLOAD_TEST_IMG_WITH_TESTID_REQ:
                        buf_offset = self.UploadTestImgWithTestIDReq.unpack(src_buf, buf_len, cur_version, buf_offset)
                        if buf_offset <= 0: return buf_offset
                if selector == CMD_UPLOAD_ERROR_INFO_REQ:
                        buf_offset = self.UploadErrorInfoReq.unpack(src_buf, buf_len, cur_version, buf_offset)
                        if buf_offset <= 0: return buf_offset
                if selector == CMD_REPORT_UI_ISSUE_REQ:
                        buf_offset = self.ReportUIIssueReq.unpack(src_buf, buf_len, cur_version, buf_offset)
                        if buf_offset <= 0: return buf_offset
                return buf_offset


class CsPkgHead(object):
        CURRVERSION = 1
        __slots__ = [\
                "Len","DeviceID","Cmd","Result"\
        ]
        def __init__(self):
                self.Len = int()
                self.DeviceID = int()
                self.Cmd = int()
                self.Result = int()

        def __eq__(self, rh):
                if self.Len != rh.Len: return False
                if self.DeviceID != rh.DeviceID: return False
                if self.Cmd != rh.Cmd: return False
                if self.Result != rh.Result: return False
                return True
        def __ne__(self, rh):
                return not (self == rh)

        def __str__(self):
                vstr = []
                vstr.append("Len={%s}"%self.Len)
                vstr.append("DeviceID={%s}"%self.DeviceID)
                vstr.append("Cmd={%s}"%self.Cmd)
                vstr.append("Result={%s}"%self.Result)
                return "CsPkgHead:<" + string.join(vstr, "; ") + ">"
        __repr__ = __str__

        def _adjust_iversion(self, cur_version):
                if 0 == cur_version or 1 < cur_version:
                        cur_version = 1
                if 1 > cur_version:
                        print "illegal cur_version=%d, BASEVERSION=1"%(cur_version)
                        return -1
                return cur_version
        def _check_nversion(self, net_version):
                if 1 > net_version or net_version > 1:
                        print "illegal net_version=%d, CURRVERSION=1"%(net_version)
                        return -1
                return net_version

        def value_random(self):
                self.Len = int(random.random()*((1<<31)-1))
                self.DeviceID = int(random.random()*((1<<31)-1))
                self.Cmd = int(random.random()*((1<<15)-1))
                self.Result = int(random.random()*((1<<31)-1))

        def pack(self,  dest_buf, cur_version=0, buf_offset=0):
                "if success, ret last buf_offset, else return < 0"
                buf_start = buf_offset
                cur_version = self._adjust_iversion(cur_version)
                if cur_version < 0:
                        return -1
                _struct_uint.pack_into(dest_buf, buf_offset, self.Len); buf_offset += 4
                _struct_uint.pack_into(dest_buf, buf_offset, self.DeviceID); buf_offset += 4
                _struct_ushort.pack_into(dest_buf, buf_offset, self.Cmd); buf_offset += 2
                _struct_int.pack_into(dest_buf, buf_offset, self.Result); buf_offset += 4
                return buf_offset

        def unpack(self,  src_buf, buf_len, cur_version=0, buf_offset=0):
                "if success, ret last buf_offset, err return < 0, =0 need more data"
                buf_start = buf_offset
                cur_version = self._adjust_iversion(cur_version)
                if cur_version < 0: return -1
                self.Len = _struct_uint.unpack_from(src_buf, buf_offset)[0]; buf_offset += 4
                self.DeviceID = _struct_uint.unpack_from(src_buf, buf_offset)[0]; buf_offset += 4
                self.Cmd = _struct_ushort.unpack_from(src_buf, buf_offset)[0]; buf_offset += 2
                self.Result = _struct_int.unpack_from(src_buf, buf_offset)[0]; buf_offset += 4
                return buf_offset


class CsPkg(object):
        CURRVERSION = 1
        __slots__ = [\
                "Head","Body"\
        ]
        def __init__(self):
                self.Head = CsPkgHead()
                self.Body = CsPkgBody()

        def __eq__(self, rh):
                if self.Head != rh.Head: return False
                if self.Body != rh.Body: return False
                return True
        def __ne__(self, rh):
                return not (self == rh)

        def __str__(self):
                vstr = []
                vstr.append("Head={%s}"%self.Head)
                vstr.append("Body={%s}"%self.Body)
                return "CsPkg:<" + string.join(vstr, "; ") + ">"
        __repr__ = __str__

        def _adjust_iversion(self, cur_version):
                if 0 == cur_version or 1 < cur_version:
                        cur_version = 1
                if 1 > cur_version:
                        print "illegal cur_version=%d, BASEVERSION=1"%(cur_version)
                        return -1
                return cur_version
        def _check_nversion(self, net_version):
                if 1 > net_version or net_version > 1:
                        print "illegal net_version=%d, CURRVERSION=1"%(net_version)
                        return -1
                return net_version

        def value_random(self):
                self.Head.value_random()
                self.Body.value_random()

        def pack(self,  dest_buf, cur_version=0, buf_offset=0):
                "if success, ret last buf_offset, else return < 0"
                buf_start = buf_offset
                cur_version = self._adjust_iversion(cur_version)
                if cur_version < 0:
                        return -1
                buf_offset = self.Head.pack(dest_buf,  cur_version, buf_offset)
                if buf_offset <= 0: return buf_offset
                buf_offset = self.Body.pack(self.Head.Cmd, dest_buf,  cur_version, buf_offset)
                if buf_offset <= 0: return buf_offset
                self.Head.Len = buf_offset - buf_start
                _tmp_pos = buf_start + 0
                _struct_uint.pack_into(dest_buf, _tmp_pos, self.Head.Len); _tmp_pos += 4
                return buf_offset

        def unpack(self,  src_buf, buf_len, cur_version=0, buf_offset=0):
                "if success, ret last buf_offset, err return < 0, =0 need more data"
                buf_start = buf_offset
                _tmp_pos = buf_start + 0
                self.Head.Len = _struct_uint.unpack_from(src_buf, _tmp_pos)[0]; _tmp_pos += 4
                if self.Head.Len > buf_len - buf_start: return 0
                cur_version = self._adjust_iversion(cur_version)
                if cur_version < 0: return -1
                buf_offset = self.Head.unpack(src_buf, buf_len, cur_version, buf_offset)
                if buf_offset <= 0: return buf_offset
                buf_offset = self.Body.unpack(self.Head.Cmd, src_buf, buf_len, cur_version, buf_offset)
                if buf_offset <= 0: return buf_offset
                buf_offset = self.Head.Len + buf_start
                return buf_offset

CMD_ALLOC_SVR_REQ = 1020
CMD_ALLOC_SVR_RES = 1021
CMD_UPLOAD_TEST_IMG_WITH_TESTID_REQ = 1067
CMD_REPORT_UI_ISSUE_REQ = 1083
CMD_REPORT_UI_ISSUE_RES = 1084
CMD_UPLOAD_ERROR_INFO_REQ = 1094
CMD_UPLOAD_ERROR_INFO_RES = 1095

class AllocSvrReq(object):
        CURRVERSION = 1
        __slots__ = [\
                "Type"\
        ]
        def __init__(self):
                self.Type = int()

        def __eq__(self, rh):
                if self.Type != rh.Type: return False
                return True
        def __ne__(self, rh):
                return not (self == rh)

        def __str__(self):
                vstr = []
                vstr.append("Type={%s}"%self.Type)
                return "AllocSvrReq:<" + string.join(vstr, "; ") + ">"
        __repr__ = __str__

        def _adjust_iversion(self, cur_version):
                if 0 == cur_version or 1 < cur_version:
                        cur_version = 1
                if 1 > cur_version:
                        print "illegal cur_version=%d, BASEVERSION=1"%(cur_version)
                        return -1
                return cur_version
        def _check_nversion(self, net_version):
                if 1 > net_version or net_version > 1:
                        print "illegal net_version=%d, CURRVERSION=1"%(net_version)
                        return -1
                return net_version

        def value_random(self):
                self.Type = int(random.random()*((1<<7)-1))

        def pack(self,  dest_buf, cur_version=0, buf_offset=0):
                "if success, ret last buf_offset, else return < 0"
                buf_start = buf_offset
                cur_version = self._adjust_iversion(cur_version)
                if cur_version < 0:
                        return -1
                _struct_uchar.pack_into(dest_buf, buf_offset, self.Type); buf_offset += 1
                return buf_offset

        def unpack(self,  src_buf, buf_len, cur_version=0, buf_offset=0):
                "if success, ret last buf_offset, err return < 0, =0 need more data"
                buf_start = buf_offset
                cur_version = self._adjust_iversion(cur_version)
                if cur_version < 0: return -1
                self.Type = _struct_uchar.unpack_from(src_buf, buf_offset)[0]; buf_offset += 1
                return buf_offset


class AllocSvrRes(object):
        CURRVERSION = 1
        __slots__ = [\
                "Type","SvrIP","SvrPort"\
        ]
        def __init__(self):
                self.Type = int()
                self.SvrIP = int()
                self.SvrPort = int()

        def __eq__(self, rh):
                if self.Type != rh.Type: return False
                if self.SvrIP != rh.SvrIP: return False
                if self.SvrPort != rh.SvrPort: return False
                return True
        def __ne__(self, rh):
                return not (self == rh)

        def __str__(self):
                vstr = []
                vstr.append("Type={%s}"%self.Type)
                vstr.append("SvrIP={%s}"%self.SvrIP)
                vstr.append("SvrPort={%s}"%self.SvrPort)
                return "AllocSvrRes:<" + string.join(vstr, "; ") + ">"
        __repr__ = __str__

        def _adjust_iversion(self, cur_version):
                if 0 == cur_version or 1 < cur_version:
                        cur_version = 1
                if 1 > cur_version:
                        print "illegal cur_version=%d, BASEVERSION=1"%(cur_version)
                        return -1
                return cur_version
        def _check_nversion(self, net_version):
                if 1 > net_version or net_version > 1:
                        print "illegal net_version=%d, CURRVERSION=1"%(net_version)
                        return -1
                return net_version

        def value_random(self):
                self.Type = int(random.random()*((1<<7)-1))
                self.SvrIP = int(random.random()*((1<<31)-1))
                self.SvrPort = int(random.random()*((1<<15)-1))

        def pack(self,  dest_buf, cur_version=0, buf_offset=0):
                "if success, ret last buf_offset, else return < 0"
                buf_start = buf_offset
                cur_version = self._adjust_iversion(cur_version)
                if cur_version < 0:
                        return -1
                _struct_uchar.pack_into(dest_buf, buf_offset, self.Type); buf_offset += 1
                _struct_uint.pack_into(dest_buf, buf_offset, self.SvrIP); buf_offset += 4
                _struct_ushort.pack_into(dest_buf, buf_offset, self.SvrPort); buf_offset += 2
                return buf_offset

        def unpack(self,  src_buf, buf_len, cur_version=0, buf_offset=0):
                "if success, ret last buf_offset, err return < 0, =0 need more data"
                buf_start = buf_offset
                cur_version = self._adjust_iversion(cur_version)
                if cur_version < 0: return -1
                self.Type = _struct_uchar.unpack_from(src_buf, buf_offset)[0]; buf_offset += 1
                self.SvrIP = _struct_uint.unpack_from(src_buf, buf_offset)[0]; buf_offset += 4
                self.SvrPort = _struct_ushort.unpack_from(src_buf, buf_offset)[0]; buf_offset += 2
                return buf_offset


class Image(object):
        CURRVERSION = 1
        __slots__ = [\
                "Len","Data"\
        ]
        def __init__(self):
                self.Len = int()
                self.Data = list()

        def __eq__(self, rh):
                if self.Len != rh.Len: return False
                if self.Data != rh.Data: return False
                return True
        def __ne__(self, rh):
                return not (self == rh)

        def __str__(self):
                vstr = []
                vstr.append("Len={%s}"%self.Len)
                vstr.append("Data={%s}"%self.Data)
                return "Image:<" + string.join(vstr, "; ") + ">"
        __repr__ = __str__

        def _adjust_iversion(self, cur_version):
                if 0 == cur_version or 1 < cur_version:
                        cur_version = 1
                if 1 > cur_version:
                        print "illegal cur_version=%d, BASEVERSION=1"%(cur_version)
                        return -1
                return cur_version
        def _check_nversion(self, net_version):
                if 1 > net_version or net_version > 1:
                        print "illegal net_version=%d, CURRVERSION=1"%(net_version)
                        return -1
                return net_version

        def value_random(self):
                self.Len = int(random.random()*((1<<31)-1))
                _len = int(random.random()*PKG_MAX_BODY_LEN)
                self.Data = []
                for i in range(_len):
                        self.Data.append(int())
                        self.Data[i] = int(random.random()*((1<<7)-1))

        def pack(self,  dest_buf, cur_version=0, buf_offset=0):
                "if success, ret last buf_offset, else return < 0"
                buf_start = buf_offset
                cur_version = self._adjust_iversion(cur_version)
                if cur_version < 0:
                        return -1
                self.Len = len(self.Data)
                _struct_int.pack_into(dest_buf, buf_offset, self.Len); buf_offset += 4
                for ea in self.Data:
                        _struct_uchar.pack_into(dest_buf, buf_offset, ea); buf_offset += 1
                return buf_offset

        def unpack(self,  src_buf, buf_len, cur_version=0, buf_offset=0):
                "if success, ret last buf_offset, err return < 0, =0 need more data"
                buf_start = buf_offset
                cur_version = self._adjust_iversion(cur_version)
                if cur_version < 0: return -1
                self.Len = _struct_int.unpack_from(src_buf, buf_offset)[0]; buf_offset += 4
                self.Data = []
                for i in range(self.Len):
                        self.Data.append(int())
                        self.Data[i] = _struct_uchar.unpack_from(src_buf, buf_offset)[0]; buf_offset += 1
                return buf_offset


class UploadTestImgWithTestIDReq(object):
        CURRVERSION = 1
        __slots__ = [\
                "TestID","Index","Image","Timestamp"\
        ]
        def __init__(self):
                self.TestID = int()
                self.Index = int()
                self.Image = Image()
                self.Timestamp = int()

        def __eq__(self, rh):
                if self.TestID != rh.TestID: return False
                if self.Index != rh.Index: return False
                if self.Image != rh.Image: return False
                if self.Timestamp != rh.Timestamp: return False
                return True
        def __ne__(self, rh):
                return not (self == rh)

        def __str__(self):
                vstr = []
                vstr.append("TestID={%s}"%self.TestID)
                vstr.append("Index={%s}"%self.Index)
                vstr.append("Image={%s}"%self.Image)
                vstr.append("Timestamp={%s}"%self.Timestamp)
                return "UploadTestImgWithTestIDReq:<" + string.join(vstr, "; ") + ">"
        __repr__ = __str__

        def _adjust_iversion(self, cur_version):
                if 0 == cur_version or 1 < cur_version:
                        cur_version = 1
                if 1 > cur_version:
                        print "illegal cur_version=%d, BASEVERSION=1"%(cur_version)
                        return -1
                return cur_version
        def _check_nversion(self, net_version):
                if 1 > net_version or net_version > 1:
                        print "illegal net_version=%d, CURRVERSION=1"%(net_version)
                        return -1
                return net_version

        def value_random(self):
                self.TestID = int(random.random()*((1<<31)-1))
                self.Index = int(random.random()*((1<<31)-1))
                self.Image.value_random()
                self.Timestamp = int(random.random()*((1<<63)-1))

        def pack(self,  dest_buf, cur_version=0, buf_offset=0):
                "if success, ret last buf_offset, else return < 0"
                buf_start = buf_offset
                cur_version = self._adjust_iversion(cur_version)
                if cur_version < 0:
                        return -1
                _struct_uint.pack_into(dest_buf, buf_offset, self.TestID); buf_offset += 4
                _struct_uint.pack_into(dest_buf, buf_offset, self.Index); buf_offset += 4
                buf_offset = self.Image.pack(dest_buf,  cur_version, buf_offset)
                if buf_offset <= 0: return buf_offset
                _struct_long.pack_into(dest_buf, buf_offset, self.Timestamp); buf_offset += 8
                return buf_offset

        def unpack(self,  src_buf, buf_len, cur_version=0, buf_offset=0):
                "if success, ret last buf_offset, err return < 0, =0 need more data"
                buf_start = buf_offset
                cur_version = self._adjust_iversion(cur_version)
                if cur_version < 0: return -1
                self.TestID = _struct_uint.unpack_from(src_buf, buf_offset)[0]; buf_offset += 4
                self.Index = _struct_uint.unpack_from(src_buf, buf_offset)[0]; buf_offset += 4
                buf_offset = self.Image.unpack(src_buf, buf_len, cur_version, buf_offset)
                if buf_offset <= 0: return buf_offset
                self.Timestamp = _struct_long.unpack_from(src_buf, buf_offset)[0]; buf_offset += 8
                return buf_offset


class ReportUIIssueReq(object):
        CURRVERSION = 1
        __slots__ = [\
                "IssueType","Index","time"\
        ]
        def __init__(self):
                self.IssueType = int()
                self.Index = int()
                self.time = int()

        def __eq__(self, rh):
                if self.IssueType != rh.IssueType: return False
                if self.Index != rh.Index: return False
                if self.time != rh.time: return False
                return True
        def __ne__(self, rh):
                return not (self == rh)

        def __str__(self):
                vstr = []
                vstr.append("IssueType={%s}"%self.IssueType)
                vstr.append("Index={%s}"%self.Index)
                vstr.append("time={%s}"%self.time)
                return "ReportUIIssueReq:<" + string.join(vstr, "; ") + ">"
        __repr__ = __str__

        def _adjust_iversion(self, cur_version):
                if 0 == cur_version or 1 < cur_version:
                        cur_version = 1
                if 1 > cur_version:
                        print "illegal cur_version=%d, BASEVERSION=1"%(cur_version)
                        return -1
                return cur_version
        def _check_nversion(self, net_version):
                if 1 > net_version or net_version > 1:
                        print "illegal net_version=%d, CURRVERSION=1"%(net_version)
                        return -1
                return net_version

        def value_random(self):
                self.IssueType = int(random.random()*((1<<7)-1))
                self.Index = int(random.random()*((1<<31)-1))
                self.time = int(random.random()*((1<<63)-1))

        def pack(self,  dest_buf, cur_version=0, buf_offset=0):
                "if success, ret last buf_offset, else return < 0"
                buf_start = buf_offset
                cur_version = self._adjust_iversion(cur_version)
                if cur_version < 0:
                        return -1
                _struct_uchar.pack_into(dest_buf, buf_offset, self.IssueType); buf_offset += 1
                _struct_uint.pack_into(dest_buf, buf_offset, self.Index); buf_offset += 4
                _struct_long.pack_into(dest_buf, buf_offset, self.time); buf_offset += 8
                return buf_offset

        def unpack(self,  src_buf, buf_len, cur_version=0, buf_offset=0):
                "if success, ret last buf_offset, err return < 0, =0 need more data"
                buf_start = buf_offset
                cur_version = self._adjust_iversion(cur_version)
                if cur_version < 0: return -1
                self.IssueType = _struct_uchar.unpack_from(src_buf, buf_offset)[0]; buf_offset += 1
                self.Index = _struct_uint.unpack_from(src_buf, buf_offset)[0]; buf_offset += 4
                self.time = _struct_long.unpack_from(src_buf, buf_offset)[0]; buf_offset += 8
                return buf_offset


class UploadErrorInfoReq(object):
        CURRVERSION = 1
        __slots__ = [\
                "Code","Level","Time","Scene","Desc","Content"\
        ]
        def __init__(self):
                self.Code = int()
                self.Level = int()
                self.Time = int()
                self.Scene = str()
                self.Desc = str()
                self.Content = str()

        def __eq__(self, rh):
                if self.Code != rh.Code: return False
                if self.Level != rh.Level: return False
                if self.Time != rh.Time: return False
                if self.Scene != rh.Scene: return False
                if self.Desc != rh.Desc: return False
                if self.Content != rh.Content: return False
                return True
        def __ne__(self, rh):
                return not (self == rh)

        def __str__(self):
                vstr = []
                vstr.append("Code={%s}"%self.Code)
                vstr.append("Level={%s}"%self.Level)
                vstr.append("Time={%s}"%self.Time)
                vstr.append("Scene={%s}"%self.Scene)
                vstr.append("Desc={%s}"%self.Desc)
                vstr.append("Content={%s}"%self.Content)
                return "UploadErrorInfoReq:<" + string.join(vstr, "; ") + ">"
        __repr__ = __str__

        def _adjust_iversion(self, cur_version):
                if 0 == cur_version or 1 < cur_version:
                        cur_version = 1
                if 1 > cur_version:
                        print "illegal cur_version=%d, BASEVERSION=1"%(cur_version)
                        return -1
                return cur_version
        def _check_nversion(self, net_version):
                if 1 > net_version or net_version > 1:
                        print "illegal net_version=%d, CURRVERSION=1"%(net_version)
                        return -1
                return net_version

        def value_random(self):
                self.Code = int(random.random()*((1<<31)-1))
                self.Level = int(random.random()*((1<<7)-1))
                self.Time = int(random.random()*((1<<63)-1))
                self.Scene = "%c"%(int(random.random()*94) + 32)*1024
                self.Desc = "%c"%(int(random.random()*94) + 32)*1024
                self.Content = "%c"%(int(random.random()*94) + 32)*102400

        def pack(self,  dest_buf, cur_version=0, buf_offset=0):
                "if success, ret last buf_offset, else return < 0"
                buf_start = buf_offset
                cur_version = self._adjust_iversion(cur_version)
                if cur_version < 0:
                        return -1
                _struct_int.pack_into(dest_buf, buf_offset, self.Code); buf_offset += 4
                _struct_uchar.pack_into(dest_buf, buf_offset, self.Level); buf_offset += 1
                _struct_long.pack_into(dest_buf, buf_offset, self.Time); buf_offset += 8
                _s = self.Scene+'\0'; _len = len(_s); _struct_int.pack_into(dest_buf, buf_offset, _len); buf_offset += 4;dest_buf[buf_offset:buf_offset+_len] = _s; buf_offset += _len
                _s = self.Desc+'\0'; _len = len(_s); _struct_int.pack_into(dest_buf, buf_offset, _len); buf_offset += 4;dest_buf[buf_offset:buf_offset+_len] = _s; buf_offset += _len
                _s = self.Content+'\0'; _len = len(_s); _struct_int.pack_into(dest_buf, buf_offset, _len); buf_offset += 4;dest_buf[buf_offset:buf_offset+_len] = _s; buf_offset += _len
                return buf_offset

        def unpack(self,  src_buf, buf_len, cur_version=0, buf_offset=0):
                "if success, ret last buf_offset, err return < 0, =0 need more data"
                buf_start = buf_offset
                cur_version = self._adjust_iversion(cur_version)
                if cur_version < 0: return -1
                self.Code = _struct_int.unpack_from(src_buf, buf_offset)[0]; buf_offset += 4
                self.Level = _struct_uchar.unpack_from(src_buf, buf_offset)[0]; buf_offset += 1
                self.Time = _struct_long.unpack_from(src_buf, buf_offset)[0]; buf_offset += 8
                _len = _struct_int.unpack_from(src_buf, buf_offset)[0]; buf_offset += 4;self.Scene = src_buf[buf_offset:buf_offset+_len-1]; buf_offset += _len
                _len = _struct_int.unpack_from(src_buf, buf_offset)[0]; buf_offset += 4;self.Desc = src_buf[buf_offset:buf_offset+_len-1]; buf_offset += _len
                _len = _struct_int.unpack_from(src_buf, buf_offset)[0]; buf_offset += 4;self.Content = src_buf[buf_offset:buf_offset+_len-1]; buf_offset += _len
                return buf_offset

TYPE_ISSUE_NORMAL = 0
TYPE_ISSUE_BLACK = 1
TYPE_ISSUE_WHITE = 2
TYPE_ISSUE_BLACK_BORDER = 4
TYPE_ISSUE_SIMILAR = 8
ERR_NO_ERROR = 0
ERR_DEVICE_UNEXIST = 101
ERR_PERMISSION_DENIED = 102
ERR_SERVER_MEM_ERROR = 103
ERR_DEVICE_BUSY = 104
ERR_INVALIED_REQ = 105
ERR_VERSION_TOO_OLD = 106
ERR_DEVICE_OFFLINE = 107
ERR_DOWNLOAD = 108
ERR_APK = 109
ERR_INSTALL = 110
ERR_START_APP = 111
ERR_NO_SVR = 112
ERR_APK_CRASH = 113
ERR_APK_UNINSTALL = 114
ERR_DOWNLOAD_SCRIPT = 115
ERR_OPEN_SCRIPT_FILE = 116
ERR_ERROR_SCRIPT = 117
ERR_ERROR_ADAPTER = 118
ERR_ERROR_CANCELED = 119
ERR_DEVICE_FREE = 120
ERR_ANR = 121
ERR_TEST_UNEXIST = 122
ERR_FAIL = 123
ERR_LOGIN_FAIL = 124
ERR_NO_QQ = 125
ERR_NOT_IN_QQ_LOGIN_UI = 126
ERR_SWITCH_NETWORK = 127
ERR_LAUNCH_QQ = 128
ERR_WIFI_NOT_CONNECT = 129
ERR_AE_ERROR = 130
ERR_ADB_DEVICE_OFFLINE = 131
ERR_ADB_DEVICE_NOT_FOUND = 132
ERR_NETWORK_NOT_CONNECT = 133
ERR_INSUFFICIENT_STORAGE = 134
ERR_NO_DISK_SPACE = 135
ERR_CONTROL_AUTH = 136
ERR_UI = 137
ERR_FUNCTIONAL = 138
ERR_NORMAL_EXIT = 139
ERR_APK_EXCEPTION = 140
ERR_BLACK_IMAGE = 141
ERR_WHITE_IMAGE = 142
ERR_BLACK_BORDER = 143
ERR_SIMILAR_IMAGE = 144
ERR_START_APP_BY_PLATFORM = 145
ERR_ADB_SERVER_NOT_ACK = 146
ERR_ADB_DAEMON_NOT_RUNNING = 147
ERR_SCRIPT_ERROR = 148
ERR_SUGGEST = 4
ERR_NORMAL = 2
ERR_CRITICAL = 1
ERR_FATAL = 0

if __name__ == '__main__':
        import getopt, time
        _try_times = 100
        _buf_len = 1024000
        _output_msg = False
        options, args = getopt.getopt(sys.argv[1:], "hrpm:l:")
        for n, v in options:
                if n == '-h':
                        print "usage: " + sys.argv[0] + " -h -r -p [-m] [-l]"
                        print "	-h=help"
                        print "	-r=set random seed with now time, default no random seed"
                        print "	-p=print msg, default no output"
                        print "	-m=each class pack|unpack times, default 100"
                        print "	-h=pack or unpack buf len, default 1024000"
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
        
        _packed = CsPkgHead()
        _unpacked = CsPkgHead()
        _packed.value_random()
        _bl = _packed.pack(_b, 1)
        if _output_msg:
                print _packed
        _rbl = _unpacked.unpack(_b, _bl / 2)
        if _rbl == 0:
                print "%-28s support frame, you know what i mean..."%('CsPkgHead')
        _time_start = time.time()
        for x in xrange(_try_times):
                _bl = _packed.pack(_b, 1)
                _rbl = _unpacked.unpack(_b, _bl)
                if _bl != _rbl:
                        print _packed
                        raise BaseException("pack_len=%d != unpack_len=%d"%(_bl, _rbl))
                if _packed != _unpacked:
                        print _packed
                        print _unpacked
                        raise BaseException("pack cls != unpack cls")
        print "%-28s pack<->unpack %10d times in %6d seconds......."%('CsPkgHead', _try_times, time.time() - _time_start)
        
        
        _packed = CsPkg()
        _unpacked = CsPkg()
        _packed.value_random()
        _bl = _packed.pack(_b, 1)
        if _output_msg:
                print _packed
        _rbl = _unpacked.unpack(_b, _bl / 2)
        if _rbl == 0:
                print "%-28s support frame, you know what i mean..."%('CsPkg')
        _time_start = time.time()
        for x in xrange(_try_times):
                _bl = _packed.pack(_b, 1)
                _rbl = _unpacked.unpack(_b, _bl)
                if _bl != _rbl:
                        print _packed
                        raise BaseException("pack_len=%d != unpack_len=%d"%(_bl, _rbl))
                if _packed != _unpacked:
                        print _packed
                        print _unpacked
                        raise BaseException("pack cls != unpack cls")
        print "%-28s pack<->unpack %10d times in %6d seconds......."%('CsPkg', _try_times, time.time() - _time_start)
        
        
        _packed = AllocSvrReq()
        _unpacked = AllocSvrReq()
        _packed.value_random()
        _bl = _packed.pack(_b, 1)
        if _output_msg:
                print _packed
        _rbl = _unpacked.unpack(_b, _bl / 2)
        if _rbl == 0:
                print "%-28s support frame, you know what i mean..."%('AllocSvrReq')
        _time_start = time.time()
        for x in xrange(_try_times):
                _bl = _packed.pack(_b, 1)
                _rbl = _unpacked.unpack(_b, _bl)
                if _bl != _rbl:
                        print _packed
                        raise BaseException("pack_len=%d != unpack_len=%d"%(_bl, _rbl))
                if _packed != _unpacked:
                        print _packed
                        print _unpacked
                        raise BaseException("pack cls != unpack cls")
        print "%-28s pack<->unpack %10d times in %6d seconds......."%('AllocSvrReq', _try_times, time.time() - _time_start)
        
        
        _packed = AllocSvrRes()
        _unpacked = AllocSvrRes()
        _packed.value_random()
        _bl = _packed.pack(_b, 1)
        if _output_msg:
                print _packed
        _rbl = _unpacked.unpack(_b, _bl / 2)
        if _rbl == 0:
                print "%-28s support frame, you know what i mean..."%('AllocSvrRes')
        _time_start = time.time()
        for x in xrange(_try_times):
                _bl = _packed.pack(_b, 1)
                _rbl = _unpacked.unpack(_b, _bl)
                if _bl != _rbl:
                        print _packed
                        raise BaseException("pack_len=%d != unpack_len=%d"%(_bl, _rbl))
                if _packed != _unpacked:
                        print _packed
                        print _unpacked
                        raise BaseException("pack cls != unpack cls")
        print "%-28s pack<->unpack %10d times in %6d seconds......."%('AllocSvrRes', _try_times, time.time() - _time_start)
        
        
        _packed = Image()
        _unpacked = Image()
        _packed.value_random()
        _bl = _packed.pack(_b, 1)
        if _output_msg:
                print _packed
        _rbl = _unpacked.unpack(_b, _bl / 2)
        if _rbl == 0:
                print "%-28s support frame, you know what i mean..."%('Image')
        _time_start = time.time()
        for x in xrange(_try_times):
                _bl = _packed.pack(_b, 1)
                _rbl = _unpacked.unpack(_b, _bl)
                if _bl != _rbl:
                        print _packed
                        raise BaseException("pack_len=%d != unpack_len=%d"%(_bl, _rbl))
                if _packed != _unpacked:
                        print _packed
                        print _unpacked
                        raise BaseException("pack cls != unpack cls")
        print "%-28s pack<->unpack %10d times in %6d seconds......."%('Image', _try_times, time.time() - _time_start)
        
        
        _packed = UploadTestImgWithTestIDReq()
        _unpacked = UploadTestImgWithTestIDReq()
        _packed.value_random()
        _bl = _packed.pack(_b, 1)
        if _output_msg:
                print _packed
        _rbl = _unpacked.unpack(_b, _bl / 2)
        if _rbl == 0:
                print "%-28s support frame, you know what i mean..."%('UploadTestImgWithTestIDReq')
        _time_start = time.time()
        for x in xrange(_try_times):
                _bl = _packed.pack(_b, 1)
                _rbl = _unpacked.unpack(_b, _bl)
                if _bl != _rbl:
                        print _packed
                        raise BaseException("pack_len=%d != unpack_len=%d"%(_bl, _rbl))
                if _packed != _unpacked:
                        print _packed
                        print _unpacked
                        raise BaseException("pack cls != unpack cls")
        print "%-28s pack<->unpack %10d times in %6d seconds......."%('UploadTestImgWithTestIDReq', _try_times, time.time() - _time_start)
        
        
        _packed = ReportUIIssueReq()
        _unpacked = ReportUIIssueReq()
        _packed.value_random()
        _bl = _packed.pack(_b, 1)
        if _output_msg:
                print _packed
        _rbl = _unpacked.unpack(_b, _bl / 2)
        if _rbl == 0:
                print "%-28s support frame, you know what i mean..."%('ReportUIIssueReq')
        _time_start = time.time()
        for x in xrange(_try_times):
                _bl = _packed.pack(_b, 1)
                _rbl = _unpacked.unpack(_b, _bl)
                if _bl != _rbl:
                        print _packed
                        raise BaseException("pack_len=%d != unpack_len=%d"%(_bl, _rbl))
                if _packed != _unpacked:
                        print _packed
                        print _unpacked
                        raise BaseException("pack cls != unpack cls")
        print "%-28s pack<->unpack %10d times in %6d seconds......."%('ReportUIIssueReq', _try_times, time.time() - _time_start)
        
        
        _packed = UploadErrorInfoReq()
        _unpacked = UploadErrorInfoReq()
        _packed.value_random()
        _bl = _packed.pack(_b, 1)
        if _output_msg:
                print _packed
        _rbl = _unpacked.unpack(_b, _bl / 2)
        if _rbl == 0:
                print "%-28s support frame, you know what i mean..."%('UploadErrorInfoReq')
        _time_start = time.time()
        for x in xrange(_try_times):
                _bl = _packed.pack(_b, 1)
                _rbl = _unpacked.unpack(_b, _bl)
                if _bl != _rbl:
                        print _packed
                        raise BaseException("pack_len=%d != unpack_len=%d"%(_bl, _rbl))
                if _packed != _unpacked:
                        print _packed
                        print _unpacked
                        raise BaseException("pack cls != unpack cls")
        print "%-28s pack<->unpack %10d times in %6d seconds......."%('UploadErrorInfoReq', _try_times, time.time() - _time_start)
        
