# -*- coding: utf-8 -*-#
"""
@author:Galen.Wang
@file: Ducut.py
@time: 2020/5/27
@description:
Great artist always hid themselves in their work.

"""
import re
import os
import jieba

jieba.re_han_default = re.compile("([\u4E00-\u9FD5a-zA-Z0-9+#&\._%/ ]+)", re.U)

WORD_DIR = './data/word_dict'


def clean_str(data_str: str, diagonal=False, is_lower=True):
    """有效字符包括中英文和数字，以及-和.这两种标点，删除多余字符串
    """
    if not isinstance(data_str, str):
        return ''
    if is_lower:
        data_str = data_str.lower()
    if diagonal:
        reg = '[^\\u3400-\\u9FEFa-zA-Z0-9.-/]'
        data_str = data_str.replace('\\', '/')
    else:
        reg = '[^\\u3400-\\u9FEFa-zA-Z0-9.-]'
    data_str = re.sub(reg, ' ', data_str)
    return re.sub(' +', ' ', data_str).strip()


def keep_en_ch_num_str(data_str: str, is_lower=True, blank=True):
    """仅保留中英文和数字
    """
    if not isinstance(data_str, str):
        return ''
    if is_lower:
        data_str = data_str.lower()
    reg = '[^\\u3400-\\u9FEFa-zA-Z0-9]'
    data_str = re.sub(reg, ' ', data_str)
    if blank:
        return re.sub(' +', ' ', data_str).strip()
    return re.sub(' +', ' ', data_str).replace(' ', '')


def load_text_to_list(file_path):
    with open(file_path, 'r')as f:
        return f.read().splitlines()


class Trie:

    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.root = {}
        self.end = -1

    def insert(self, word):
        """
        Inserts a word into the trie.
        :type word: str
        :rtype: void
        """

        curNode = self.root
        for c in word:
            if c not in curNode:
                curNode[c] = {}
            curNode = curNode[c]
        curNode[self.end] = True

    def search(self, word):
        """
        Returns if the word is in the trie.
        :type word: str
        :rtype: bool
        """
        curNode = self.root
        for c in word:
            if c not in curNode:
                return False
            curNode = curNode[c]

        # Doesn't end here
        if self.end not in curNode:
            return False

        return True

    def startsWith(self, prefix):
        """
        Returns if there is any word in the trie that starts with the given prefix.
        :type prefix: str
        :rtype: bool
        """
        curNode = self.root
        for c in prefix:
            if c not in curNode:
                return False
            curNode = curNode[c]

        return True

    def get_start(self, prefix):
        """
        给出一个前辍，打印出所有匹配的字符串
        :param prefix:
        :return:
        """

        def get_key(pre, pre_node):
            result = []
            if pre_node.get(self.end):
                result.append(pre)
            for key in pre_node.keys():
                if key != self.end:
                    result.extend(get_key(pre + key, pre_node.get(key)))
            return result

        if not self.startsWith(prefix):
            return []
        else:
            node = self.root
            for p in prefix:
                node = node.get(p)
            else:
                return get_key(prefix, node)


class Cuter:
    def __init__(self, raw_str):
        self.raw_str = raw_str
        self.cut_list = []
        self.brand = []
        self.series = []
        self.color = []
        self.category = []
        self.proper = []
        self.word = []
        self.other = []


class DuCut:
    def __init__(self, word_dir=WORD_DIR):
        self.word_dir = word_dir
        self.sim_en_cn_dict = {}
        self.sim_cn_en_dict = {}
        self.brand_dict = {}
        self.series_dict = {}
        self.color_set = set()
        self.category_set = set()
        self.proper_set = set()
        self.brand_tire = Trie()
        self.series_tire = Trie()
        self.__initial()

    @staticmethod
    def add_word_file(path):
        # 加载自定义词典
        jieba.load_userdict(path)

    @staticmethod
    def add_word(word):
        jieba.add_word(word)

    def __initial(self):
        # brand_name_ml.txt   category_ml.txt     color_ml.txt        dic_sim_new.csv     series_names_ml.txt synonym_ml.txt
        # 加载同义词库
        file_list = os.listdir(self.word_dir)
        # 先加载同义词
        self.__load_dic_sim(os.path.join(self.word_dir, 'dic_sim_new.csv'))
        self.__load_synonym(os.path.join(self.word_dir, 'synonym_ml.txt'))
        self.__load_synonym(os.path.join(self.word_dir, 'synonym_hand.txt'))
        # 加载其他词
        for file_name in file_list:
            file_path = os.path.join(self.word_dir, file_name)
            if file_name.startswith('brand_name'):
                self.__load_brand_name(file_path)
            elif file_name.startswith('series_names'):
                self.__load_series_names(file_path)
            elif file_name.startswith('color'):
                self.__load_color(file_path)
            elif file_name.startswith('category'):
                self.__load_category(file_path)
            elif file_name.startswith('proper'):
                self.__load_proper(file_path)
            else:
                pass

    def __load_dic_sim(self, data_path):
        data_list = load_text_to_list(data_path)
        # New Balance,"新百伦,纽百伦" kiss of death,死亡之吻 中文=>英文
        for data in data_list:
            if '_word,' in data or len(data) < 1:
                continue
            data_en_ch = data.split(',')
            data_en_ch = [i.strip('"') for i in data_en_ch]
            if len(data_en_ch) < 2:
                print(f'data sim error {data}')
                continue
            en_clean = keep_en_ch_num_str(data_en_ch[0])
            for ch in data_en_ch[1:]:
                self.sim_cn_en_dict[ch] = en_clean
                jieba.add_word(ch)
            self.sim_en_cn_dict[en_clean] = data_en_ch[1:]
        print(f'loading sim_en_cn_dict num is {len(self.sim_en_cn_dict)}')
        print(f'loading sim_cn_en_dict num is {len(self.sim_cn_en_dict)}')

    def __load_synonym(self, data_path):
        data_list = load_text_to_list(data_path)
        # cur l=珂润
        for data in data_list:
            if len(data) < 1:
                continue
            data_en_ch = data.split('=')
            if len(data_en_ch) < 2:
                print(f'data __load_synonym error {data}')
                continue
            en_clean = keep_en_ch_num_str(data_en_ch[0])
            ch_clean = keep_en_ch_num_str(data_en_ch[1])
            self.sim_en_cn_dict[en_clean] = [ch_clean]
            self.sim_cn_en_dict[ch_clean] = en_clean
            jieba.add_word(en_clean)
            jieba.add_word(ch_clean)
        print(f'loading {data_path} sim_cn_en_dict num is {len(self.sim_en_cn_dict)}')
        print(f'loading {data_path}  sim_cn_en_dict num is {len(self.sim_cn_en_dict)}')

    def __load_brand_name(self, data_path):
        data_list = load_text_to_list(data_path)
        for data in data_list:
            if len(data) < 1:
                continue
            data_clean = keep_en_ch_num_str(data)
            # 英文到中文 ['aj','乔丹]
            sim_words = self.sim_en_cn_dict.get(data_clean, None)
            if sim_words is not None:
                for sim in sim_words:
                    jieba.add_word(sim)
                    self.brand_tire.insert(sim)
                    sim_compact = keep_en_ch_num_str(sim, blank=False)
                    self.brand_dict[sim_compact] = sim
            jieba.add_word(data)
            data_compact = keep_en_ch_num_str(data_clean, blank=False)
            # 不然切不出来
            jieba.add_word(data_compact)
            self.brand_dict[data_compact] = data_clean
            self.brand_tire.insert(data_compact)
        print(f'loading {data_path} brand_dict num is {len(self.brand_dict)}')

    def __load_series_names(self, data_path):
        data_list = load_text_to_list(data_path)
        for data in data_list:
            if len(data) < 1:
                continue
            data_clean = keep_en_ch_num_str(data)
            jieba.add_word(data)
            data_compact = data_clean.replace(' ', '')
            jieba.add_word(data_compact)
            self.series_dict[data_compact] = data_clean
            self.series_tire.insert(data_compact)
        print(f'loading {data_path} series_dict num is {len(self.series_dict)}')

    def __load_base(self, data_path):
        data_list = load_text_to_list(data_path)
        data_new_list = []
        for data in data_list:
            if len(data) < 1:
                continue
            jieba.add_word(data)
            data_new_list.append(data)
            sim_word = self.sim_cn_en_dict.get(data, None)
            if sim_word is not None:
                jieba.add_word(sim_word)
                data_new_list.append(sim_word)
        return set(data_new_list)

    def __load_color(self, data_path):
        self.color_set = self.color_set | self.__load_base(data_path)
        print(f'loading {data_path} color_set num is {len(self.color_set)}')

    def __load_category(self, data_path):
        self.category_set = self.category_set | self.__load_base(data_path)
        print(f'loading {data_path} _load_category num is {len(self.category_set)}')

    def __load_proper(self, data_path):
        self.proper_set = self.proper_set | self.__load_base(data_path)
        print(f'loading {data_path} __load_proper num is {len(self.proper_set)}')

    def get_max_keywords(self, data_list, mode=0):
        data_len = len(data_list)
        # print('get_max_keywords', data_list)
        for index in range(data_len):
            data_prefix = keep_en_ch_num_str(''.join(data_list[0:index + 1]), blank=False)
            # print('data_prefix', data_prefix)
            if mode == 0:
                # if not self.brand_dict.get(data_prefix, None) is None:
                if not self.brand_tire.startsWith(data_prefix):
                    return index
            else:
                if not self.series_tire.startsWith(data_prefix):
                    return index
        return len(data_list)

    def get_brand(self, data_list):
        # 解析品牌
        brand_list = []
        brand_start = None
        data_len = len(data_list)
        index = 0
        while True:
            if index + 1 > data_len:
                break
            if self.brand_tire.startsWith(data_list[index]) and brand_start is None:
                brand_start = index
            if brand_start is None:
                index += 1
                continue
            brand_step = self.get_max_keywords(data_list[brand_start:])
            # print(brand_step, index, data_list[index])
            if brand_step == 0:
                index += 1
                brand_word = data_list[brand_start]
            else:
                index += brand_step
                brand_word = ' '.join(data_list[brand_start:brand_start + brand_step])
            brand_key = keep_en_ch_num_str(brand_word, blank=False)
            if self.brand_dict.get(brand_key, None) is not None:
                brand_list.append(brand_word)
            brand_start = None
        brand_list = [keep_en_ch_num_str(i) for i in brand_list if len(i) >= 2]
        return brand_list

    def get_series(self, data_list):
        # 解析系列
        series_list = []
        series_start = None
        data_len = len(data_list)
        index = 0
        while True:
            if index + 1 > data_len:
                break
            # print(data_list[index], index)
            if self.series_tire.startsWith(data_list[index]) and series_start is None:
                series_start = index
            index += 1
            if series_start is None:
                continue
            series_step = self.get_max_keywords(data_list[series_start:], 1)
            if series_step == 0:
                index += 1
                series_word = data_list[series_start]
            else:
                index += series_step
                series_word = ' '.join(data_list[series_start:series_start + series_step])
            series_key = keep_en_ch_num_str(series_word, blank=False)
            if self.series_dict.get(series_key, None) is not None:
                series_list.append(series_word)
            series_start = None
        series_list = [keep_en_ch_num_str(i) for i in series_list if len(i) >= 2]
        return series_list

    def parse_proper(self, data_list, cuter):
        cuter.brand = self.get_brand(data_list)
        cuter.series = self.get_series(data_list)
        # 'air fear of god shoot around',  # 能识别出 品牌 fear of god 其实是耐克 有系列删除品牌
        if len(cuter.series) > 0:
            for brand in cuter.brand:
                if brand in ''.join(cuter.series):
                    cuter.brand.remove(brand)
        for word in data_list:
            if len(word.strip()) == 0:
                continue
            if word in ''.join(cuter.brand) or word in ''.join(cuter.series):
                continue
            if word in self.color_set:
                cuter.color.append(word)
            elif word in self.category_set:
                cuter.category.append(word)
            elif word in self.proper_set:
                cuter.proper.append(word)
            else:
                cuter.word.append(word)

    def cut_query(self, data_str, keep_blank=True):
        cuter = Cuter(data_str)

        data_clean_str = clean_str(data_str)
        if keep_blank:
            data_clean_str = data_clean_str.replace(' ', '')
        # 一刀切
        if ' ' not in data_clean_str:
            cut_list = jieba.lcut(data_clean_str)
        else:
            # 切了又切
            text_list = data_clean_str.split(' ')
            cut_list = []
            for text in text_list:
                text_small = keep_en_ch_num_str(text, blank=False)
                if len(text_small) <= 4:
                    cut_list.append(text)
                    continue
                if text_small.encode('utf-8').isalpha() or text_small.isdigit():
                    cut_list.append(text)
                    continue
                # 结巴分词长问题要进行过滤
                word_cut_list = jieba.lcut(text)
                if len(word_cut_list) > 0:
                    cut_list.extend(word_cut_list)
        # print(cut_list)
        cut_list = [i for i in cut_list if len(i.strip()) > 0]
        cuter.cut_list = cut_list
        self.parse_proper(cut_list, cuter)
        return cuter

    def cut_title(self, data_str):
        pass

    def cut(self, data_str):
        return jieba.lcut(data_str)


if __name__ == '__main__':
    dc = DuCut()
    demo_list = [
        # 'new balance madness',
        # '芋泥紫 匡威',
        # '匡威 芋泥紫 ',
        # '耐克 芋泥紫 ',
        # '耐克 芋泥紫 女鞋',
        # '耐克 芋泥紫  t.n.t',
        # '圣水 shoes 耶稣',
        # 'lebron xvii fp',
        # 'aj 女款夏季鞋',
        # '老北京布鞋',
        # 'vans off white old',
        # 'air fear of god moccasin',
        # 'iphone watch',
        # 'air fear of god shoot around',  # 能识别出 品牌 fear of god 其实是耐克
        # '睡衣女',
        # '冰蓝天使',
        # '奔驰 g100 g 500',
        # '耐克网鞋女',
        # '皇马球衣',
        # 'air pords',
        # 'air max 90 green camo',
        # 'aj1mid烟灰gs',
        # 'airjordan34wh',
        # 'air max 970',
        # '1 07 lx',
        # 'ai虚拟试鞋',
        # '万斯红色',
        # '昨晚下了高铁就跑去练球多刻苦',
        # 'aj520',
        # 'aj6rings',
        # 'yeezy700v1',
        # '耐克网鞋男',
        # 'air jordan 24',
        # 'aj4unc',
        # 'nike脱靴',
        # '男拖',
        # 'yeezy700v1',
        # 'yeezy 350',
        # 'yeezy 700 og',
        # 'lebron17fp ep',
        # 'aj1l',
        # 'aj玫红色女款',
        # 'vans off white old skool',
        # 'aj女款鞋时尚',
        # '中大童运动鞋',
        # 'aj 25',
        # '万斯 板鞋白红',
        # 'supreme the north face',
        '欧文四复活节',
        '川久保玲欧文四复活节',
    ]
    dc.add_word('川久保玲')
    for demo in demo_list:
        # print(demo, dc.cut_query(demo))
        # print(demo, dc.get_max_keywords(demo.split()))
        # print(demo, 'brand', dc.get_brand(demo.split()))
        # print(demo, 'get_series', dc.get_series(demo.split()))
        cu = dc.cut_query(demo)
        # # print(demo, 'parse_proper', cu.brand, cu.series, cu.color, cu.category, cu.word, )
        print(
            f"{demo},brand:{cu.brand},series:{cu.series},color:{cu.color},category:{cu.category},proper: {cu.proper},word: {cu.word}")
        print(cu.cut_list)
        # print(dc.cut(demo))
    # print(dc.sim_en_cn_dict['air jordan'])
    # print(dc.sim_cn_en_dict['鞋'])
    # print(dc.proper_set)
    # print(dc.brand_dict['匡威'])
