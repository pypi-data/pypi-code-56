# -*- coding: utf-8 -*-
import xml.sax


class List:

    def __init__(self):
        self.list = []

    def __get__(self, instance, owner):
        return self.list

    def append(self, value):
        self.list.append(value)

    def len(self):
        return len(self.list)

    def __contains__(self, item):
        for x in self.list:
            if item == x:
                return True
            else:
                continue
        return False


class ManifestXmlHandler(xml.sax.ContentHandler):
    def __init__(self, app_package, platformversion):
        self.CurrentTag = ""
        self.list = List()
        self.app_pacage = app_package
        self.platformversion = platformversion

    # 元素开始事件处理
    def startElement(self, tag, attributes):
        if tag == self.CurrentTag:
            title = attributes["android:name"]
            # title = self.shortened(title)
            self.list.append(title)

    def parse(self, source, tag):
        self.CurrentTag = tag
        # 创建一个 XMLReader
        parser = xml.sax.make_parser()
        # turn off namepsaces
        parser.setFeature(xml.sax.handler.feature_namespaces, 0)
        parser.setContentHandler(self)
        parser.parse(source)
        return self.list

    def version_compare(self, target_version, base_version):
        """版本号比对"""
        v1_list = target_version.split('.')
        v2_list = base_version.split('.')
        v = 0
        v1_len = len(v1_list)
        v2_len = len(v2_list)
        if v1_len > v2_len:
            for i in range(v1_len - v2_len):
                v2_list.append('0')
        elif v2_len > v1_len:
            for i in range(v2_len - v1_len):
                v1_list.append('0')
        else:
            ...
        for i, v in enumerate(v1_list):
            if int(v1_list[i]) > int(v2_list[i]):
                return True
            if int(v1_list[i]) < int(v2_list[i]):
                return False
        return True

    def shortened(self, tag):
        """android 8.1对长度大于77字符的layer名称做了缩短处理
            见源码/frameworks/native/services/surfaceflinger/Layer.cpp Layer::miniDump
        """
        name = self.app_pacage + "/" + tag + "#0"
        if len(name) > 77 and self.version_compare(self.platformversion, '8.0'):
            shortstr = name[0:36]
            shortstr += "[...]"
            shortstr += name[-36:]
            """去处尾部#0"""
            shortstr = shortstr.split("#")[0]
            """去处包名"""
            shortstr = shortstr.split("/")[1]
            name = shortstr
        else:
            name = tag
        return name
