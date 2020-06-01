# -*- coding: utf-8 -*-
from .environment import *


class Locator:

    @classmethod
    def initWithText(cls, Text, remark='', idx=0, direction='', name='', cover_racts=None):
        return cls(Text, remark, idx, direction, name, ElementAttribute.TEXT, cover_racts)

    @classmethod
    def initWithDescription(cls, Description, remark='', idx=0, direction='', name='', cover_racts=None):
        return cls(Description, remark, idx, direction, name, ElementAttribute.ACCESSIBILITY_ID, cover_racts)

    @classmethod
    def initWithClassName(cls, ClassName, remark='', idx=0, direction='', name='', cover_racts=None):
        return cls(ClassName, remark, idx, direction, name, ElementAttribute.CLASS_NAME, cover_racts)

    @classmethod
    def initWithName(cls, Name, remark='', idx=0, direction='', name='', cover_racts=None):
        return cls(Name, remark, idx, direction, name, ElementAttribute.NAME, cover_racts)

    @classmethod
    def initWithUp(cls, Id, remark='', idx=0, name='', cover_racts=None):
        return cls(Id, remark, idx, ScrollDirection.UP, name, ElementAttribute.ID, cover_racts)

    @classmethod
    def initWithTextAndUp(cls, Text, remark='', idx=0, name='', cover_racts=None):
        return cls(Text, remark, idx, ScrollDirection.UP, name, ElementAttribute.TEXT, cover_racts)

    @classmethod
    def initWithTextAndLeft(cls, Text, remark='', idx=0, name='', cover_racts=None):
        return cls(Text, remark, idx, ScrollDirection.LEFT, name, ElementAttribute.TEXT, cover_racts)

    @classmethod
    def initWithXpath(cls, location, cover_racts=None):
        return cls(location, '', 0, '', '', By.XPATH, cover_racts)

    def __init__(self, location='', remark='', idx=0, direction='', name='', by_type='id', cover_racts=None):
        self.location = location
        self.remark = remark
        self.idx = idx
        self.direction = direction
        self.by_type = by_type
        self.name = name
        if cover_racts is None:
            self.cover_racts = []
        else:
            self.cover_racts = cover_racts

    def addCoverRact(self, racts):
        self.cover_racts.append(racts)

    def __str__(self):
        return '[Locator-> name:{}, location:{}, type:{}, index:{}, direction:{}, remark:{}]'.format(
            self.name, self.location, self.by_type, self.idx, self.direction, self.remark)

    def input(self, text, clear=False):
        """输入文本"""

    def clear(self):
        """清除文本"""

    def click(self):
        """点击元素"""

    def displayed(self):
        """元素是否可见"""

    def selected(self):
        """元素是否选中"""

    def enabled(self):
        """元素是否可点击"""

    def checked(self):
        """开关是否开启"""

    def text(self):
        """获取元素文本"""


class completingLocator(type):

    def __new__(cls, name, base, attr):
        r = super().__new__(cls, name, base, attr)

        def completing():
            for k, v in attr.items():
                locator = getattr(r, k)  # type:Locator
                if isinstance(locator, Locator):
                    locator.name = k
                    if locator.by_type == 'id' and ':id' not in locator.location:
                        locator.location = env.appPackage + ':id/' + locator.location
                    if not locator.remark and locator.by_type in ['text', 'name']:
                        locator.remark = locator.location
                    """增加page引用"""
                    locator.page = r
        completing()
        env.platform = Platform.IOS if env.platform is Platform.ANDROID else Platform.ANDROID
        completing()
        env.platform = Platform.IOS if env.platform is Platform.ANDROID else Platform.ANDROID
        return r


class Locators:

    def __init__(self, android: Locator = None, ios: Locator = None):
        self.android = android or ios
        self.ios = ios or android

    def __get__(self, instance, Type):
        if env.platform is Platform.ANDROID:
            return self.android
        return self.ios
