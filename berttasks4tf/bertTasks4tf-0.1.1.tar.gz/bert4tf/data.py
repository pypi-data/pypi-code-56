#!/usr/bin/python
# coding:utf8
"""
@author: Cong Yu
@time: 2020-05-16 20:56
"""
import collections
import pandas as pd
import tensorflow as tf
import numpy as np
from bert4tf import tokenization
from sklearn.utils import shuffle


def _truncate_seq_pair(tokens_a, tokens_b, max_length):
    """Truncates a sequence pair in place to the maximum length."""

    # This is a simple heuristic which will always truncate the longer sequence
    # one token at a time. This makes more sense than truncating an equal percent
    # of tokens from each, since if one sequence is very short then each token
    # that's truncated likely contains more information than a longer sequence.
    while True:
        total_length = len(tokens_a) + len(tokens_b)
        if total_length <= max_length:
            break
        if len(tokens_a) > len(tokens_b):
            tokens_a.pop()
        else:
            tokens_b.pop()


class DataProcessor:
    def __init__(self, vocab_file, label_list, train_file=None, dev_file=None, train_tf_file=None, dev_tf_file=None,
                 max_seq_length=128):
        # bert 的词汇表
        self.vocab_file = vocab_file
        # bert 分词器
        self.tokenizer = tokenization.FullTokenizer(vocab_file=self.vocab_file)
        # 原始训练文件位置
        self.train_file = train_file
        # 原始验证文件位置
        self.dev_file = dev_file
        # 训练文件位置(tf)
        self.train_tf_file = train_tf_file
        # 验证文件位置(tf)
        self.dev_tf_file = dev_tf_file
        # 最大长度
        self.max_seq_length = max_seq_length
        # y 标签列表
        self.label_list = label_list
        # 标签-id
        self.label2id = {str(_): i for i, _ in enumerate(self.label_list)}
        # id-标签
        self.id2label = [k for k, v in self.label2id.items()]

    def process_one_example(self, text_a, text_b=None, max_seq_len=128):
        """
            处理 单个样本
        """
        tokens_a = self.tokenizer.tokenize(text_a)
        tokens_b = None
        if text_b:
            tokens_b = self.tokenizer.tokenize(text_b)

        if tokens_b:
            # Modifies `tokens_a` and `tokens_b` in place so that the total
            # length is less than the specified length.
            # Account for [CLS], [SEP], [SEP] with "- 3"
            _truncate_seq_pair(tokens_a, tokens_b, max_seq_len - 3)
        else:
            # Account for [CLS] and [SEP] with "- 2"
            if len(tokens_a) > max_seq_len - 2:
                tokens_a = tokens_a[0:(max_seq_len - 2)]
        tokens = []
        segment_ids = []
        tokens.append("[CLS]")
        segment_ids.append(0)
        for token in tokens_a:
            tokens.append(token)
            segment_ids.append(0)
        tokens.append("[SEP]")
        segment_ids.append(0)

        if tokens_b:
            for token in tokens_b:
                tokens.append(token)
                segment_ids.append(1)
            tokens.append("[SEP]")
            segment_ids.append(1)

        input_ids = self.tokenizer.convert_tokens_to_ids(tokens)

        # The mask has 1 for real tokens and 0 for padding tokens. Only real
        # tokens are attended to.
        input_mask = [1] * len(input_ids)

        # Zero-pad up to the sequence length.
        while len(input_ids) < max_seq_len:
            input_ids.append(0)
            input_mask.append(0)
            segment_ids.append(0)

        assert len(input_ids) == max_seq_len
        assert len(input_mask) == max_seq_len
        assert len(segment_ids) == max_seq_len

        feature = (input_ids, input_mask, segment_ids)
        return feature

    def process_one_example_sequence(self, text, label, max_seq_len=128):
        """
        bert 序列标注 开始结束 都是 补零 "0"，即 0 对应是无意义的 序列标注 ，序列标注的标签即 第一个 默认为 "O" 标签
        """
        text_ist = list(text)
        label_list = list(label)
        tokens = []
        labels = []
        for i, word in enumerate(text_ist):
            token = self.tokenizer.tokenize(word)
            # 为了对其，空格等 bert 不可见字符使用 [unused1] 替代，是的 字级别对其
            if len(token) == 0:
                token = ["[unused1]"]
            tokens.extend(token)
            label_1 = label_list[i]
            for m in range(len(token)):
                if m == 0:
                    labels.append(label_1)
                else:
                    print("some unknown token...", token)
                    labels.append(labels[0])
        # tokens = tokenizer.tokenize(example.text)  -2 的原因是因为序列需要加一个句首和句尾标志
        if len(tokens) >= max_seq_len - 1:
            tokens = tokens[0:(max_seq_len - 2)]
            labels = labels[0:(max_seq_len - 2)]
        n_tokens = []
        segment_ids = []
        label_ids = []
        n_tokens.append("[CLS]")  # 句子开始设置CLS 标志
        segment_ids.append(0)
        # [CLS] [SEP] 可以为 他们构建标签，或者 统一到某个标签，反正他们是不变的，基本不参加训练 即：x-l 永远不变
        label_ids.append(0)  # label2id["[CLS]"]
        for i, token in enumerate(tokens):
            n_tokens.append(token)
            segment_ids.append(0)
            label_ids.append(self.label2id[labels[i]])
        n_tokens.append("[SEP]")
        segment_ids.append(0)
        # append("O") or append("[SEP]") not sure!
        label_ids.append(0)  # label2id["[SEP]"]
        input_ids = self.tokenizer.convert_tokens_to_ids(n_tokens)
        input_mask = [1] * len(input_ids)
        while len(input_ids) < max_seq_len:
            input_ids.append(0)
            input_mask.append(0)
            segment_ids.append(0)
            label_ids.append(0)
            n_tokens.append("**NULL**")
        assert len(input_ids) == max_seq_len
        assert len(input_mask) == max_seq_len
        assert len(segment_ids) == max_seq_len
        assert len(label_ids) == max_seq_len
        feature = (input_ids, input_mask, segment_ids, label_ids)
        return feature

    def prepare_multi_label_tf_record_data(self, is_pair=False, train_or_dev="train", split=";"):
        """
            处理多标签分类模型， 是否是 句子对模式， 默认 是 csv 格式的训练数据
            句子对时：
                0=text_a
                1=text_b
                2=label(默认一致使用英文 ';' 进行分割多标签)
            单句子时：
                0=text
                1=label(默认一致使用英文 ';' 进行分割多标签)
        """

        def create_int_feature(values):
            f = tf.train.Feature(int64_list=tf.train.Int64List(value=list(values)))
            return f

        # 处理训练集，或者验证集
        origin_path = self.train_file if train_or_dev == "train" else self.dev_file
        tf_file = self.train_tf_file if train_or_dev == "train" else self.dev_tf_file
        print(origin_path, tf_file)
        df = pd.read_csv(origin_path, index_col=0)
        df = shuffle(df)
        writer = tf.python_io.TFRecordWriter(tf_file)
        count = 0
        for index, row in df.iterrows():
            # label = label2id[row["topic"].strip()]
            text_a = str(row[0])
            if is_pair:
                text_b = str(row[1])
                column_name_y = 2
            else:
                text_b = None
                column_name_y = 1
            feature = self.process_one_example(text_a, text_b, max_seq_len=self.max_seq_length)
            # 多标签任务
            label = np.zeros(len(self.label_list), dtype=np.int64)
            if str(row[column_name_y]) != "nan" and str(row[column_name_y]) != "":
                label_index = []
                i = row[column_name_y]
                for _ in i.split(split):
                    if self.label2id.get(_, None) is not None:
                        label_index.append(self.label2id.get(_))
                    else:
                        print(_)
                label[label_index] = 1

            features = collections.OrderedDict()
            features["input_ids"] = create_int_feature(feature[0])
            features["input_mask"] = create_int_feature(feature[1])
            features["segment_ids"] = create_int_feature(feature[2])
            features["label_ids"] = create_int_feature(label)
            count += 1
            if count < 5:
                print("*** Example ***")
                print("input_ids: %s" % " ".join([str(x) for x in feature[0]]))
                print("input_mask: %s" % " ".join([str(x) for x in feature[1]]))
                print("segment_ids: %s" % " ".join([str(x) for x in feature[2]]))
                print("label: %s (id = %s)" % (row[column_name_y], str(label)))
            tf_example = tf.train.Example(features=tf.train.Features(feature=features))
            writer.write(tf_example.SerializeToString())

            if count % 1000 == 0:
                print(count)
        writer.close()
        print("example count:", count)
        return count

    def prepare_multi_class_tf_record_data(self, is_pair=False, train_or_dev="train"):
        """
            处理多标签分类模型， 是否是 句子对模式， 默认 是 csv 格式的训练数据
            句子对时：
                0=text_a
                1=text_b
                2=label()
            单句子时：
                0=text
                1=label()
        """

        def create_int_feature(values):
            f = tf.train.Feature(int64_list=tf.train.Int64List(value=list(values)))
            return f

        # 处理训练集，或者验证集
        origin_path = self.train_file if train_or_dev == "train" else self.dev_file
        tf_file = self.train_tf_file if train_or_dev == "train" else self.dev_tf_file
        print(origin_path, tf_file)
        df = pd.read_csv(origin_path, index_col=0)
        df = shuffle(df)
        writer = tf.python_io.TFRecordWriter(tf_file)
        count = 0
        for index, row in df.iterrows():
            # label = label2id[row["topic"].strip()]
            text_a = str(row[0])
            if is_pair:
                text_b = str(row[1])
                column_name_y = 2
            else:
                text_b = None
                column_name_y = 1
            feature = self.process_one_example(text_a, text_b, max_seq_len=self.max_seq_length)
            # 多分类任务
            label_id = self.label2id.get(str(row[column_name_y]), None)
            if label_id is None:
                print(text_a, text_b, str(row[column_name_y]))
                continue
            label = [label_id]
            features = collections.OrderedDict()
            features["input_ids"] = create_int_feature(feature[0])
            features["input_mask"] = create_int_feature(feature[1])
            features["segment_ids"] = create_int_feature(feature[2])
            features["label_ids"] = create_int_feature(label)
            count += 1
            if count < 5:
                print("*** Example ***")
                print("input_ids: %s" % " ".join([str(x) for x in feature[0]]))
                print("input_mask: %s" % " ".join([str(x) for x in feature[1]]))
                print("segment_ids: %s" % " ".join([str(x) for x in feature[2]]))
                print("label: %s (id = %s)" % (row[column_name_y], str(label)))
            tf_example = tf.train.Example(features=tf.train.Features(feature=features))
            writer.write(tf_example.SerializeToString())
            if count % 1000 == 0:
                print(count)
        writer.close()
        print("example count:", count)
        return count

    def prepare_sequence_label_tf_record_data(self, train_or_dev="train"):
        """
            处理多标签分类模型， 默认 是 csv 格式的训练数据
            0=text(允许有空格，适应 英文序列标注， 如英文人名)
            1=label(序列标注，使用 空格进行分割)
        """

        def create_int_feature(values):
            f = tf.train.Feature(int64_list=tf.train.Int64List(value=list(values)))
            return f

        # 处理训练集，或者验证集
        origin_path = self.train_file if train_or_dev == "train" else self.dev_file
        tf_file = self.train_tf_file if train_or_dev == "train" else self.dev_tf_file
        print(origin_path, tf_file)
        df = pd.read_csv(origin_path, index_col=0)
        df = shuffle(df)
        writer = tf.python_io.TFRecordWriter(tf_file)
        count = 0
        for index, row in df.iterrows():
            text = str(row[0]).strip()
            column_name_y = 1
            label = str(row[column_name_y]).strip().split(" ")
            if len(text) != len(label):
                print(text, label)
                continue
            feature = self.process_one_example_sequence(text, label, max_seq_len=self.max_seq_length)
            features = collections.OrderedDict()
            features["input_ids"] = create_int_feature(feature[0])
            features["input_mask"] = create_int_feature(feature[1])
            features["segment_ids"] = create_int_feature(feature[2])
            features["label_ids"] = create_int_feature(feature[3])
            count += 1
            if count < 5:
                print("*** Example ***")
                print("input_ids: %s" % " ".join([str(x) for x in feature[0]]))
                print("input_mask: %s" % " ".join([str(x) for x in feature[1]]))
                print("segment_ids: %s" % " ".join([str(x) for x in feature[2]]))
                print("label: %s (id = %s)" % (row[column_name_y], str(label)))
            tf_example = tf.train.Example(features=tf.train.Features(feature=features))
            writer.write(tf_example.SerializeToString())
            if count % 1000 == 0:
                print(count)
        writer.close()
        print("example count:", count)
        return count
