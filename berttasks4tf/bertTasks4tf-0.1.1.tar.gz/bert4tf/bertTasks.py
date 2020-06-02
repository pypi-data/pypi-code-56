#!/usr/bin/python
# coding:utf8
"""
@author: Cong Yu
@time: 2020-05-16 21:16
"""
import os
import time
import math
import numpy as np
import tensorflow as tf
from bert4tf import modeling
from bert4tf import optimization
from bert4tf.config import TrainConfig
from bert4tf.data import DataProcessor
from sklearn.metrics import classification_report


def load_bert_config(path):
    """
    bert 模型配置文件
    """
    return modeling.BertConfig.from_json_file(path)


class BertMultiLabel:
    def __init__(self, config: TrainConfig, data_processor: DataProcessor):
        self.train_config = config
        self.data_processor = data_processor
        self.bert_config = load_bert_config(self.train_config.bert_config_path)
        pass

    def create_model(self, input_ids, input_mask, segment_ids, labels, use_one_hot_embeddings=False, is_training=True):
        """Creates a classification model."""
        model = modeling.BertModel(
            config=self.bert_config,
            is_training=is_training,
            input_ids=input_ids,
            input_mask=input_mask,
            token_type_ids=segment_ids,
            use_one_hot_embeddings=use_one_hot_embeddings)

        # In the demo, we are doing a simple classification task on the entire
        # segment.
        #
        # If you want to use the token-level output, use model.get_sequence_output()
        # instead.
        output_layer = model.get_pooled_output()

        hidden_size = output_layer.shape[-1].value
        print(output_layer.shape)

        output_weights = tf.get_variable(
            "output_weights", [self.train_config.num_labels, hidden_size],
            initializer=tf.truncated_normal_initializer(stddev=0.02))

        output_bias = tf.get_variable(
            "output_bias", [self.train_config.num_labels], initializer=tf.zeros_initializer())

        with tf.variable_scope("loss"):
            if is_training:
                output_layer = tf.nn.dropout(output_layer, keep_prob=self.train_config.keep_prob)

            # 改为多标签的损失
            logits = tf.matmul(output_layer, output_weights, transpose_b=True)
            logits = tf.nn.bias_add(logits, output_bias)
            if not self.train_config.use_focal_loss:
                logits = tf.nn.sigmoid(logits)  # logits 已经sigmoid处理

                predictions = tf.cast((logits > 0.5), tf.int64, name="predictions")
                print(predictions.shape)
                # 多标签损失
                losses = tf.nn.sigmoid_cross_entropy_with_logits(logits=logits, labels=tf.cast(labels, tf.float32))
                loss = tf.reduce_mean(losses)

                return loss, logits, predictions
            else:
                labels = tf.cast(labels, tf.float32)
                probs = tf.sigmoid(logits)
                predictions = tf.cast((probs > 0.5), tf.int64, name="predictions")
                print(predictions.shape)
                ce_loss = tf.nn.sigmoid_cross_entropy_with_logits(labels=labels, logits=logits)
                alpha_t = tf.ones_like(logits) * self.train_config.alpha
                alpha_t = tf.where(labels > 0, alpha_t, 1.0 - alpha_t)
                probs_t = tf.where(labels > 0, probs, 1.0 - probs)
                focal_matrix = alpha_t * tf.pow((1.0 - probs_t), self.train_config.gamma)
                loss = focal_matrix * ce_loss
                loss = tf.reduce_mean(loss)
                return loss, probs, predictions

    def get_input_data(self, train_or_dev="train"):
        if train_or_dev == "train":
            input_file = self.train_config.train_file
            is_training = True
            batch_size = self.train_config.train_batch_size
        else:
            input_file = self.train_config.dev_file
            is_training = False
            batch_size = self.train_config.dev_batch_size

        def parser(record):
            name_to_features = {
                "input_ids": tf.FixedLenFeature([self.train_config.max_seq_length], tf.int64),
                "input_mask": tf.FixedLenFeature([self.train_config.max_seq_length], tf.int64),
                "segment_ids": tf.FixedLenFeature([self.train_config.max_seq_length], tf.int64),
                "label_ids": tf.FixedLenFeature([self.train_config.num_labels], tf.int64),
            }

            example = tf.parse_single_example(record, features=name_to_features)
            input_ids_ = example["input_ids"]
            input_mask_ = example["input_mask"]
            segment_ids_ = example["segment_ids"]
            labels_ = example["label_ids"]
            return input_ids_, input_mask_, segment_ids_, labels_

        data_set = tf.data.TFRecordDataset(input_file)
        if is_training:
            data_set = data_set.map(parser).batch(batch_size).shuffle(buffer_size=3000)
        else:
            data_set = data_set.map(parser).batch(batch_size)
        iterator = data_set.make_one_shot_iterator()
        input_ids, input_mask, segment_ids, labels = iterator.get_next()
        return input_ids, input_mask, segment_ids, labels

    def train(self):
        """
        训练多标签 模型
        """
        tf.logging.set_verbosity(tf.logging.INFO)
        tf.gfile.MakeDirs(self.train_config.save_path)

        train_examples_len = self.train_config.train_examples_len
        dev_examples_len = self.train_config.dev_examples_len
        learning_rate = self.train_config.learning_rate
        eval_per_step = self.train_config.eval_per_step
        num_labels = self.train_config.num_labels

        batch_size = self.train_config.train_batch_size
        dev_batch_size = self.train_config.dev_batch_size

        num_train_steps = math.ceil(train_examples_len / batch_size)
        num_dev_steps = math.ceil(dev_examples_len / dev_batch_size)

        num_train_epochs = self.train_config.num_train_epochs
        num_warm_up_steps = math.ceil(num_train_steps * num_train_epochs * self.train_config.warm_up_proportion)

        print(f"num_train_steps:{num_train_steps},num_dev_steps:{num_dev_steps},num_warm_up_steps:{num_warm_up_steps}")
        seq_len = self.train_config.max_seq_length
        init_checkpoint = self.train_config.init_checkpoint
        model_path = os.path.join(self.train_config.save_path, 'bert.ckpt')

        print("print start compile the bert model...")

        with tf.Graph().as_default():
            gpu_config = tf.ConfigProto()
            gpu_config.gpu_options.allow_growth = True
            # 定义输入输出
            input_ids = tf.placeholder(tf.int64, shape=[None, seq_len], name='input_ids')
            input_mask = tf.placeholder(tf.int64, shape=[None, seq_len], name='input_mask')
            segment_ids = tf.placeholder(tf.int64, shape=[None, seq_len], name='segment_ids')
            labels = tf.placeholder(tf.int64, shape=[None, num_labels], name='labels')
            keep_prob = tf.placeholder(tf.float32, name='keep_prob')

            (total_loss, logits, probabilities) = self.create_model(input_ids, input_mask, segment_ids, labels)
            train_op = optimization.create_optimizer(total_loss, learning_rate, num_train_steps * num_train_epochs,
                                                     num_warm_up_steps, False)
            print("print start train the bert model(multi label)...")

            init_global = tf.global_variables_initializer()
            saver = tf.train.Saver(
                [v for v in tf.global_variables() if 'adam_v' not in v.name and 'adam_m' not in v.name],
                max_to_keep=2)  # 保存最后top3模型
            with tf.Session(config=gpu_config) as sess:
                sess.run(init_global)
                print("start load the pre-trained model")

                if init_checkpoint:
                    tvars = tf.trainable_variables()
                    print("trainable_variables", len(tvars))
                    (_, initialized_variable_names) = modeling.get_assignment_map_from_checkpoint(tvars,
                                                                                                  init_checkpoint)
                    print("initialized_variable_names:", len(initialized_variable_names))
                    saver_ = tf.train.Saver([v for v in tvars if v.name in initialized_variable_names])
                    saver_.restore(sess, init_checkpoint)
                    tvars = tf.global_variables()
                    initialized_vars = [v for v in tvars if v.name in initialized_variable_names]
                    not_initialized_vars = [v for v in tvars if v.name not in initialized_variable_names]
                    tf.logging.info('--all size %s; not initialized size %s' % (len(tvars), len(not_initialized_vars)))
                    if len(not_initialized_vars):
                        sess.run(tf.variables_initializer(not_initialized_vars))
                    for v in initialized_vars:
                        print('--initialized: %s, shape = %s' % (v.name, v.shape))
                    for v in not_initialized_vars:
                        print('--not initialized: %s, shape = %s' % (v.name, v.shape))
                else:
                    sess.run(tf.global_variables_initializer())
                print("********* bert_multi_label_train start *********")

                # tf.summary.FileWriter("output/",sess.graph)
                def train_step(ids, mask, segment, y_, step_):
                    feed = {input_ids: ids,
                            input_mask: mask,
                            segment_ids: segment,
                            labels: y_,
                            keep_prob: 0.9}
                    _, out_loss_, __, p_ = sess.run([train_op, total_loss, logits, probabilities], feed_dict=feed)
                    acc = np.sum(np.equal(p_, y_)) / np.multiply(p_.shape[0], p_.shape[1])
                    print("step :{}, lr:{}, loss :{}, acc :{}".format(step_, _[1], out_loss_, acc))
                    return out_loss_, p_, y_

                def dev_step(ids, mask, segment, y_):
                    feed = {input_ids: ids,
                            input_mask: mask,
                            segment_ids: segment,
                            labels: y_,
                            keep_prob: 1.0
                            }
                    out_loss_, _, p_ = sess.run([total_loss, logits, probabilities], feed_dict=feed)
                    acc = np.sum(np.equal(p_, y_)) / np.multiply(p_.shape[0], p_.shape[1])
                    print("loss :{}, acc :{}".format(out_loss_, acc))
                    return out_loss_, p_, y_

                min_total_loss_dev = 999999
                step = 0
                for epoch in range(num_train_epochs):
                    iii = ("epoch-" + str(epoch)).center(20)
                    _ = f"{iii:*^100s}"
                    print(_)
                    # 读取训练数据
                    total_loss_train = 0
                    total_pre_train = []
                    total_true_train = []
                    input_ids2, input_mask2, segment_ids2, labels2 = self.get_input_data("train")
                    for i in range(num_train_steps):
                        step += 1
                        ids_train, mask_train, segment_train, y_train = sess.run(
                            [input_ids2, input_mask2, segment_ids2, labels2])
                        out_loss, pre, y = train_step(ids_train, mask_train, segment_train, y_train, step)
                        total_loss_train += out_loss
                        total_pre_train.extend(pre)
                        total_true_train.extend(y)

                        if step % eval_per_step == 0 and step >= self.train_config.eval_start_step:
                            total_loss_dev = 0
                            dev_input_ids2, dev_input_mask2, dev_segment_ids2, dev_labels2 = self.get_input_data("dev")
                            total_pre_dev = []
                            total_true_dev = []
                            for j in range(num_dev_steps):  # 一个 epoch 的 轮数
                                ids_dev, mask_dev, segment_dev, y_dev = sess.run(
                                    [dev_input_ids2, dev_input_mask2, dev_segment_ids2, dev_labels2])
                                out_loss, pre, y = dev_step(ids_dev, mask_dev, segment_dev, y_dev)
                                total_loss_dev += out_loss
                                total_pre_dev.extend(pre)
                                total_true_dev.extend(y_dev)
                            #
                            print("dev result report:")
                            print(len(total_true_dev))
                            for kk in range(self.train_config.num_labels):
                                print(self.train_config.label_list[kk])
                                print(classification_report(np.array(total_true_dev)[:, kk],
                                                            np.array(total_pre_dev)[:, kk],
                                                            digits=4))

                            if total_loss_dev < min_total_loss_dev:
                                print(f"save model:\t{min_total_loss_dev}\t>{total_loss_dev}")
                                min_total_loss_dev = total_loss_dev

                                saver.save(sess, model_path, global_step=step)
                        elif step < self.train_config.eval_start_step and step % self.train_config.auto_save == 0:
                            print("auto save model")
                            saver.save(sess, model_path, global_step=step)
                    print("total_loss_train:{}".format(total_loss_train))
                    print(len(total_true_train))
                    for ii in range(self.train_config.num_labels):
                        print(self.train_config.label_list[ii])
                        print(classification_report(np.array(total_true_train)[:, ii], np.array(total_pre_train)[:, ii],
                                                    digits=4))
            sess.close()

        print("remove dropout in predict")
        tf.reset_default_graph()
        input_ids = tf.placeholder(tf.int64, shape=[None, seq_len], name='input_ids')
        input_mask = tf.placeholder(tf.int64, shape=[None, seq_len], name='input_mask')
        segment_ids = tf.placeholder(tf.int64, shape=[None, seq_len], name='segment_ids')
        labels = tf.placeholder(tf.int64, shape=[None, num_labels], name='labels')
        keep_prob = tf.placeholder(tf.float32, name='keep_prob')

        (_, _, _) = self.create_model(input_ids, input_mask, segment_ids, labels, is_training=False)
        init_global = tf.global_variables_initializer()
        saver = tf.train.Saver(tf.global_variables(), max_to_keep=1)

        try:
            checkpoint = tf.train.get_checkpoint_state(self.train_config.save_path)
            input_checkpoint = checkpoint.model_checkpoint_path
            print("[INFO] input_checkpoint:", input_checkpoint)
        except Exception as e:
            input_checkpoint = self.train_config.save_path
            print("[INFO] Model folder", self.train_config.save_path, repr(e))

        with tf.Session(config=gpu_config) as sess:
            sess.run(init_global)
            saver.restore(sess, input_checkpoint)
            saver.save(sess, model_path)
        sess.close()

    def load_model(self, model_path):
        """
        加载训练好的模型文件
        :param model_path:
        :return:
        """
        model_path = tf.train.latest_checkpoint(model_path)
        self.graph = tf.Graph()
        with self.graph.as_default():
            gpu_config = tf.ConfigProto()
            gpu_config.gpu_options.allow_growth = True
            self.sess = tf.Session(config=gpu_config)

            self.input_ids_p = tf.placeholder(tf.int32, [None, self.train_config.max_seq_length], name="input_ids")
            self.input_mask_p = tf.placeholder(tf.int32, [None, self.train_config.max_seq_length], name="input_mask")
            self.segment_ids_p = tf.placeholder(tf.int32, [None, self.train_config.max_seq_length], name="segment_ids")
            self.labels = tf.placeholder(tf.int64, shape=[None, self.train_config.num_labels], name='labels')
            self.keep_prob = tf.placeholder(tf.float32, name='keep_prob')

            (_, self.logits, _) = self.create_model(self.input_ids_p, self.input_mask_p, self.segment_ids_p,
                                                    self.labels, is_training=False)

            tvars = tf.trainable_variables()
            (_, initialized_variable_names) = modeling.get_assignment_map_from_checkpoint(tvars, model_path)
            init_vars = [v for v in tf.global_variables() if v.name in initialized_variable_names]
            init_vars_name = [v.name for v in init_vars]
            saver = tf.train.Saver(init_vars, max_to_keep=1)
            saver.restore(self.sess, model_path)
            tvars = tf.global_variables()
            not_initialized_vars = [v for v in tvars if v.name not in init_vars_name]
            print('all size %s; not initialized size %s' % (len(tvars), len(not_initialized_vars)))
            print('all size %s; not initialized size %s' % (len(tvars), len(not_initialized_vars)))
            for v in not_initialized_vars:
                print(f'not initialized: {v.name}')
                print(f'not initialized: {v.name}')
            if len(not_initialized_vars):
                self.sess.run(tf.variables_initializer(not_initialized_vars))

    def predict(self, text_a, text_b=None, p=0.5):
        features = []
        feature = self.data_processor.process_one_example(text_a, text_b,
                                                          max_seq_len=self.data_processor.max_seq_length)
        features.append(feature)

        with self.graph.as_default():
            feed = {self.input_ids_p: [feature[0] for feature in features],
                    self.input_mask_p: [feature[1] for feature in features],
                    self.segment_ids_p: [feature[2] for feature in features],
                    self.keep_prob: 1.0
                    }
            [logits] = self.sess.run([self.logits], feed)
            result = []
            for index, _ in enumerate(list(logits[0])):
                if _ > p:
                    label = self.data_processor.id2label[index]
                    prob = float(_)
                    result.append({"label": label, "prob": prob})
            return result


class BertMultiClass:
    def __init__(self, config: TrainConfig, data_processor: DataProcessor):
        self.train_config = config
        self.data_processor = data_processor
        self.bert_config = load_bert_config(self.train_config.bert_config_path)
        pass

    def create_model(self, input_ids, input_mask, segment_ids, labels, use_one_hot_embeddings=False, is_training=True):
        """Creates a classification model."""
        model = modeling.BertModel(
            config=self.bert_config,
            is_training=is_training,
            input_ids=input_ids,
            input_mask=input_mask,
            token_type_ids=segment_ids,
            use_one_hot_embeddings=use_one_hot_embeddings)

        # In the demo, we are doing a simple classification task on the entire
        # segment.
        #
        # If you want to use the token-level output, use model.get_sequence_output()
        # instead.
        output_layer = model.get_pooled_output()

        hidden_size = output_layer.shape[-1].value
        print(output_layer.shape)

        output_weights = tf.get_variable(
            "output_weights", [self.train_config.num_labels, hidden_size],
            initializer=tf.truncated_normal_initializer(stddev=0.02))

        output_bias = tf.get_variable(
            "output_bias", [self.train_config.num_labels], initializer=tf.zeros_initializer())

        with tf.variable_scope("loss"):
            if is_training:
                output_layer = tf.nn.dropout(output_layer, keep_prob=self.train_config.keep_prob)

            # 改为多标签的损失
            logits = tf.matmul(output_layer, output_weights, transpose_b=True)
            logits = tf.nn.bias_add(logits, output_bias)
            # probabilities = tf.nn.softmax(logits, axis=-1)
            probabilities = tf.nn.softmax(logits)
            log_prob_s = tf.nn.log_softmax(logits, axis=-1)

            one_hot_labels = tf.one_hot(labels, depth=self.train_config.num_labels, dtype=tf.float32)

            per_example_loss = -tf.reduce_sum(one_hot_labels * log_prob_s, axis=-1)
            loss = tf.reduce_mean(per_example_loss)

            return loss, logits, probabilities

    def get_input_data(self, train_or_dev="train"):
        if train_or_dev == "train":
            input_file = self.train_config.train_file
            is_training = True
            batch_size = self.train_config.train_batch_size
        else:
            input_file = self.train_config.dev_file
            is_training = False
            batch_size = self.train_config.dev_batch_size

        def parser(record):
            name_to_features = {
                "input_ids": tf.FixedLenFeature([self.train_config.max_seq_length], tf.int64),
                "input_mask": tf.FixedLenFeature([self.train_config.max_seq_length], tf.int64),
                "segment_ids": tf.FixedLenFeature([self.train_config.max_seq_length], tf.int64),
                "label_ids": tf.FixedLenFeature([], tf.int64),
            }

            example = tf.parse_single_example(record, features=name_to_features)
            input_ids_ = example["input_ids"]
            input_mask_ = example["input_mask"]
            segment_ids_ = example["segment_ids"]
            labels_ = example["label_ids"]
            return input_ids_, input_mask_, segment_ids_, labels_

        data_set = tf.data.TFRecordDataset(input_file)
        if is_training:
            data_set = data_set.map(parser).batch(batch_size).shuffle(buffer_size=3000)
        else:
            data_set = data_set.map(parser).batch(batch_size)
        iterator = data_set.make_one_shot_iterator()
        input_ids, input_mask, segment_ids, labels = iterator.get_next()
        return input_ids, input_mask, segment_ids, labels

    def train(self):
        """
        训练多标签 模型
        """
        tf.logging.set_verbosity(tf.logging.INFO)
        tf.gfile.MakeDirs(self.train_config.save_path)

        train_examples_len = self.train_config.train_examples_len
        dev_examples_len = self.train_config.dev_examples_len
        learning_rate = self.train_config.learning_rate
        eval_per_step = self.train_config.eval_per_step
        num_labels = self.train_config.num_labels

        batch_size = self.train_config.train_batch_size
        dev_batch_size = self.train_config.dev_batch_size

        num_train_steps = math.ceil(train_examples_len / batch_size)
        num_dev_steps = math.ceil(dev_examples_len / dev_batch_size)

        num_train_epochs = self.train_config.num_train_epochs
        num_warm_up_steps = math.ceil(num_train_steps * num_train_epochs * self.train_config.warm_up_proportion)

        print(f"num_train_steps:{num_train_steps},num_dev_steps:{num_dev_steps},num_warm_up_steps:{num_warm_up_steps}")
        seq_len = self.train_config.max_seq_length
        init_checkpoint = self.train_config.init_checkpoint
        model_path = os.path.join(self.train_config.save_path, 'bert.ckpt')

        print("print start compile the bert model...")

        with tf.Graph().as_default():
            gpu_config = tf.ConfigProto()
            gpu_config.gpu_options.allow_growth = True
            # 定义输入输出
            input_ids = tf.placeholder(tf.int64, shape=[None, seq_len], name='input_ids')
            input_mask = tf.placeholder(tf.int64, shape=[None, seq_len], name='input_mask')
            segment_ids = tf.placeholder(tf.int64, shape=[None, seq_len], name='segment_ids')
            labels = tf.placeholder(tf.int64, shape=[None, ], name='labels')
            keep_prob = tf.placeholder(tf.float32, name='keep_prob')

            (total_loss, logits, probabilities) = self.create_model(input_ids, input_mask, segment_ids, labels)
            train_op = optimization.create_optimizer(total_loss, learning_rate, num_train_steps * num_train_epochs,
                                                     num_warm_up_steps, False)
            print("print start train the bert model(multi class)...")

            init_global = tf.global_variables_initializer()
            saver = tf.train.Saver(
                [v for v in tf.global_variables() if 'adam_v' not in v.name and 'adam_m' not in v.name],
                max_to_keep=2)  # 保存最后top3模型
            with tf.Session(config=gpu_config) as sess:
                sess.run(init_global)
                print("start load the pre-trained model")

                if init_checkpoint:
                    tvars = tf.trainable_variables()
                    print("trainable_variables", len(tvars))
                    (_, initialized_variable_names) = modeling.get_assignment_map_from_checkpoint(tvars,
                                                                                                  init_checkpoint)
                    print("initialized_variable_names:", len(initialized_variable_names))
                    saver_ = tf.train.Saver([v for v in tvars if v.name in initialized_variable_names])
                    saver_.restore(sess, init_checkpoint)
                    tvars = tf.global_variables()
                    initialized_vars = [v for v in tvars if v.name in initialized_variable_names]
                    not_initialized_vars = [v for v in tvars if v.name not in initialized_variable_names]
                    tf.logging.info('--all size %s; not initialized size %s' % (len(tvars), len(not_initialized_vars)))
                    if len(not_initialized_vars):
                        sess.run(tf.variables_initializer(not_initialized_vars))
                    for v in initialized_vars:
                        print('--initialized: %s, shape = %s' % (v.name, v.shape))
                    for v in not_initialized_vars:
                        print('--not initialized: %s, shape = %s' % (v.name, v.shape))
                else:
                    sess.run(tf.global_variables_initializer())
                print("********* bert_multi_class_train start *********")

                def train_step(ids, mask, segment, y_, step_):
                    feed = {input_ids: ids,
                            input_mask: mask,
                            segment_ids: segment,
                            labels: y_,
                            keep_prob: 0.9}
                    _, out_loss_, out_logits, p_ = sess.run([train_op, total_loss, logits, probabilities],
                                                            feed_dict=feed)
                    pre = np.argmax(p_, axis=-1)
                    acc = np.sum(np.equal(pre, y_)) / len(pre)
                    print("step :{}, lr:{}, loss :{}, acc :{}".format(step_, _[1], out_loss_, acc))
                    return out_loss_, pre, y_

                def dev_step(ids, mask, segment, y_):
                    feed = {input_ids: ids,
                            input_mask: mask,
                            segment_ids: segment,
                            labels: y_,
                            keep_prob: 1.0
                            }
                    out_loss_, out_logits, p_ = sess.run([total_loss, logits, probabilities], feed_dict=feed)
                    pre = np.argmax(p_, axis=-1)
                    acc = np.sum(np.equal(pre, y_)) / len(pre)
                    print("loss :{}, acc :{}".format(out_loss_, acc))
                    return out_loss_, pre, y_

                min_total_loss_dev = 999999
                step = 0
                for epoch in range(num_train_epochs):
                    iii = ("epoch-" + str(epoch)).center(20)
                    _ = f"{iii:*^100s}"
                    print(_)
                    # 读取训练数据
                    total_loss_train = 0
                    total_pre_train = []
                    total_true_train = []
                    input_ids2, input_mask2, segment_ids2, labels2 = self.get_input_data("train")
                    for i in range(num_train_steps):
                        step += 1
                        ids_train, mask_train, segment_train, y_train = sess.run(
                            [input_ids2, input_mask2, segment_ids2, labels2])
                        out_loss, pre, y = train_step(ids_train, mask_train, segment_train, y_train, step)
                        total_loss_train += out_loss
                        total_pre_train.extend(pre)
                        total_true_train.extend(y)

                        if step % eval_per_step == 0 and step >= self.train_config.eval_start_step:
                            total_loss_dev = 0
                            dev_input_ids2, dev_input_mask2, dev_segment_ids2, dev_labels2 = self.get_input_data("dev")
                            total_pre_dev = []
                            total_true_dev = []
                            for j in range(num_dev_steps):  # 一个 epoch 的 轮数
                                ids_dev, mask_dev, segment_dev, y_dev = sess.run(
                                    [dev_input_ids2, dev_input_mask2, dev_segment_ids2, dev_labels2])
                                out_loss, pre, y = dev_step(ids_dev, mask_dev, segment_dev, y_dev)
                                total_loss_dev += out_loss
                                total_pre_dev.extend(pre)
                                total_true_dev.extend(y_dev)
                            #
                            print("dev result report:")
                            print(classification_report(total_true_dev, total_pre_dev, digits=4))

                            if total_loss_dev < min_total_loss_dev:
                                print(f"save model:\t{min_total_loss_dev}\t>{total_loss_dev}")
                                min_total_loss_dev = total_loss_dev

                                saver.save(sess, model_path, global_step=step)
                        elif step < self.train_config.eval_start_step and step % self.train_config.auto_save == 0:
                            print("auto save model")
                            saver.save(sess, model_path, global_step=step)
                    print("total_loss_train:{}".format(total_loss_train))
                    print(len(total_true_train))
                    print(classification_report(total_true_train, total_pre_train, digits=4))

                sess.close()

        print("remove dropout in predict")
        tf.reset_default_graph()
        input_ids = tf.placeholder(tf.int64, shape=[None, seq_len], name='input_ids')
        input_mask = tf.placeholder(tf.int64, shape=[None, seq_len], name='input_mask')
        segment_ids = tf.placeholder(tf.int64, shape=[None, seq_len], name='segment_ids')
        labels = tf.placeholder(tf.int64, shape=[None, ], name='labels')
        keep_prob = tf.placeholder(tf.float32, name='keep_prob')

        (_, _, _) = self.create_model(input_ids, input_mask, segment_ids, labels, is_training=False)
        init_global = tf.global_variables_initializer()
        saver = tf.train.Saver(tf.global_variables(), max_to_keep=1)

        try:
            checkpoint = tf.train.get_checkpoint_state(self.train_config.save_path)
            input_checkpoint = checkpoint.model_checkpoint_path
            print("[INFO] input_checkpoint:", input_checkpoint)
        except Exception as e:
            input_checkpoint = self.train_config.save_path
            print("[INFO] Model folder", self.train_config.save_path, repr(e))

        with tf.Session(config=gpu_config) as sess:
            sess.run(init_global)
            saver.restore(sess, input_checkpoint)
            saver.save(sess, model_path)
        sess.close()

    def load_model(self, model_path):
        """
        加载训练好的模型文件
        :param model_path:
        :return:
        """
        model_path = tf.train.latest_checkpoint(model_path)
        self.graph = tf.Graph()
        with self.graph.as_default():
            gpu_config = tf.ConfigProto()
            gpu_config.gpu_options.allow_growth = True
            self.sess = tf.Session(config=gpu_config)

            self.input_ids_p = tf.placeholder(tf.int32, [None, self.train_config.max_seq_length], name="input_ids")
            self.input_mask_p = tf.placeholder(tf.int32, [None, self.train_config.max_seq_length], name="input_mask")
            self.segment_ids_p = tf.placeholder(tf.int32, [None, self.train_config.max_seq_length], name="segment_ids")
            self.labels = tf.placeholder(tf.int64, shape=[None, ], name='labels')
            self.keep_prob = tf.placeholder(tf.float32, name='keep_prob')

            (_, _, self.probabilities) = self.create_model(self.input_ids_p, self.input_mask_p, self.segment_ids_p,
                                                           self.labels, is_training=False)

            tvars = tf.trainable_variables()
            (_, initialized_variable_names) = modeling.get_assignment_map_from_checkpoint(tvars, model_path)
            init_vars = [v for v in tf.global_variables() if v.name in initialized_variable_names]
            init_vars_name = [v.name for v in init_vars]
            saver = tf.train.Saver(init_vars, max_to_keep=1)
            saver.restore(self.sess, model_path)
            tvars = tf.global_variables()
            not_initialized_vars = [v for v in tvars if v.name not in init_vars_name]
            print('all size %s; not initialized size %s' % (len(tvars), len(not_initialized_vars)))
            print('all size %s; not initialized size %s' % (len(tvars), len(not_initialized_vars)))
            for v in not_initialized_vars:
                print(f'not initialized: {v.name}')
                print(f'not initialized: {v.name}')
            if len(not_initialized_vars):
                self.sess.run(tf.variables_initializer(not_initialized_vars))

    def predict(self, text_a, text_b=None):
        features = []
        feature = self.data_processor.process_one_example(text_a, text_b,
                                                          max_seq_len=self.data_processor.max_seq_length)
        features.append(feature)

        with self.graph.as_default():
            feed = {self.input_ids_p: [feature[0] for feature in features],
                    self.input_mask_p: [feature[1] for feature in features],
                    self.segment_ids_p: [feature[2] for feature in features],
                    self.keep_prob: 1.0
                    }
            [probabilities] = self.sess.run([self.probabilities], feed)
            max_index = int(np.argmax(probabilities[0]))
            label = self.data_processor.id2label[max_index]
            prob = float(probabilities[0][max_index])
            return {"label": label, "prob": prob}


class BertSequenceLabel:
    def __init__(self, config: TrainConfig, data_processor: DataProcessor):
        self.train_config = config
        self.data_processor = data_processor
        self.bert_config = load_bert_config(self.train_config.bert_config_path)
        pass

    def create_model(self, input_ids, input_mask, segment_ids, labels, use_one_hot_embeddings=False, is_training=True):
        """Creates a sequence label model."""
        model = modeling.BertModel(
            config=self.bert_config,
            is_training=is_training,
            input_ids=input_ids,
            input_mask=input_mask,
            token_type_ids=segment_ids,
            use_one_hot_embeddings=use_one_hot_embeddings)

        output_layer = model.get_sequence_output()
        hidden_size = output_layer.shape[-1].value
        seq_length = output_layer.shape[-2].value
        print(output_layer.shape)

        output_weight = tf.get_variable(
            "output_weights", [self.train_config.num_labels, hidden_size],
            initializer=tf.truncated_normal_initializer(stddev=0.02)
        )
        output_bias = tf.get_variable(
            "output_bias", [self.train_config.num_labels], initializer=tf.zeros_initializer()
        )
        with tf.variable_scope("loss"):
            if is_training:
                output_layer = tf.nn.dropout(output_layer, keep_prob=0.9)

            output_layer = tf.reshape(output_layer, [-1, hidden_size])
            logits = tf.matmul(output_layer, output_weight, transpose_b=True)
            logits = tf.reshape(logits, [-1, seq_length, self.train_config.num_labels])

            logits = tf.nn.bias_add(logits, output_bias)
            logits = tf.reshape(logits, shape=(-1, seq_length, self.train_config.num_labels))

            input_m = tf.count_nonzero(input_mask, -1)

            log_likelihood, transition_matrix = tf.contrib.crf.crf_log_likelihood(logits, labels, input_m)

            loss = tf.reduce_mean(-log_likelihood)
            # inference
            v_sequence, v_score = tf.contrib.crf.crf_decode(logits, transition_matrix, input_m)
            # 不计算 padding 的 acc
            equals = tf.reduce_sum(
                tf.cast(tf.equal(tf.cast(v_sequence, tf.int64), labels), tf.float32) * tf.cast(input_mask, tf.float32))
            acc = equals / tf.cast(tf.reduce_sum(input_mask), tf.float32)
            return loss, acc, logits, v_sequence

    def get_input_data(self, train_or_dev="train"):
        if train_or_dev == "train":
            input_file = self.train_config.train_file
            is_training = True
            batch_size = self.train_config.train_batch_size
        else:
            input_file = self.train_config.dev_file
            is_training = False
            batch_size = self.train_config.dev_batch_size

        def parser(record):
            name_to_features = {
                "input_ids": tf.FixedLenFeature([self.train_config.max_seq_length], tf.int64),
                "input_mask": tf.FixedLenFeature([self.train_config.max_seq_length], tf.int64),
                "segment_ids": tf.FixedLenFeature([self.train_config.max_seq_length], tf.int64),
                "label_ids": tf.FixedLenFeature([self.train_config.max_seq_length], tf.int64),
            }

            example = tf.parse_single_example(record, features=name_to_features)
            input_ids_ = example["input_ids"]
            input_mask_ = example["input_mask"]
            segment_ids_ = example["segment_ids"]
            labels_ = example["label_ids"]
            return input_ids_, input_mask_, segment_ids_, labels_

        data_set = tf.data.TFRecordDataset(input_file)
        if is_training:
            data_set = data_set.map(parser).batch(batch_size).shuffle(buffer_size=3000)
        else:
            data_set = data_set.map(parser).batch(batch_size)
        iterator = data_set.make_one_shot_iterator()
        input_ids, input_mask, segment_ids, labels = iterator.get_next()
        return input_ids, input_mask, segment_ids, labels

    def train(self):
        """
        训练多标签 模型
        """
        tf.logging.set_verbosity(tf.logging.INFO)
        tf.gfile.MakeDirs(self.train_config.save_path)

        train_examples_len = self.train_config.train_examples_len
        dev_examples_len = self.train_config.dev_examples_len
        learning_rate = self.train_config.learning_rate
        eval_per_step = self.train_config.eval_per_step
        num_labels = self.train_config.num_labels

        batch_size = self.train_config.train_batch_size
        dev_batch_size = self.train_config.dev_batch_size

        num_train_steps = math.ceil(train_examples_len / batch_size)
        num_dev_steps = math.ceil(dev_examples_len / dev_batch_size)

        num_train_epochs = self.train_config.num_train_epochs
        num_warm_up_steps = math.ceil(num_train_steps * num_train_epochs * self.train_config.warm_up_proportion)

        print(f"num_train_steps:{num_train_steps},num_dev_steps:{num_dev_steps},num_warm_up_steps:{num_warm_up_steps}")
        seq_len = self.train_config.max_seq_length
        init_checkpoint = self.train_config.init_checkpoint
        model_path = os.path.join(self.train_config.save_path, 'bert.ckpt')

        print("print start compile the bert model...")
        with tf.Graph().as_default():
            gpu_config = tf.ConfigProto()
            gpu_config.gpu_options.allow_growth = True
            # 定义输入输出
            input_ids = tf.placeholder(tf.int64, shape=[None, seq_len], name='input_ids')
            input_mask = tf.placeholder(tf.int64, shape=[None, seq_len], name='input_mask')
            segment_ids = tf.placeholder(tf.int64, shape=[None, seq_len], name='segment_ids')
            labels = tf.placeholder(tf.int64, shape=[None, seq_len], name='labels')
            keep_prob = tf.placeholder(tf.float32, name='keep_prob')

            (total_loss, acc, logits, probabilities) = self.create_model(input_ids, input_mask, segment_ids, labels)
            train_op = optimization.create_optimizer(total_loss, learning_rate, num_train_steps * num_train_epochs,
                                                     num_warm_up_steps, False)
            print("print start train the bert model(sequence label)...")

            init_global = tf.global_variables_initializer()
            saver = tf.train.Saver(
                [v for v in tf.global_variables() if 'adam_v' not in v.name and 'adam_m' not in v.name],
                max_to_keep=2)  # 保存最后top3模型
            with tf.Session(config=gpu_config) as sess:
                sess.run(init_global)
                print("start load the pre-trained model")

                if init_checkpoint:
                    tvars = tf.trainable_variables()
                    print("trainable_variables", len(tvars))
                    (_, initialized_variable_names) = modeling.get_assignment_map_from_checkpoint(tvars,
                                                                                                  init_checkpoint)
                    print("initialized_variable_names:", len(initialized_variable_names))
                    saver_ = tf.train.Saver([v for v in tvars if v.name in initialized_variable_names])
                    saver_.restore(sess, init_checkpoint)
                    tvars = tf.global_variables()
                    initialized_vars = [v for v in tvars if v.name in initialized_variable_names]
                    not_initialized_vars = [v for v in tvars if v.name not in initialized_variable_names]
                    tf.logging.info('--all size %s; not initialized size %s' % (len(tvars), len(not_initialized_vars)))
                    if len(not_initialized_vars):
                        sess.run(tf.variables_initializer(not_initialized_vars))
                    for v in initialized_vars:
                        print('--initialized: %s, shape = %s' % (v.name, v.shape))
                    for v in not_initialized_vars:
                        print('--not initialized: %s, shape = %s' % (v.name, v.shape))
                else:
                    sess.run(tf.global_variables_initializer())
                print("********* bert_sequence_train start *********")

                def train_step(ids, mask, segment, y_, step_):
                    feed = {input_ids: ids,
                            input_mask: mask,
                            segment_ids: segment,
                            labels: y_,
                            keep_prob: 0.9}
                    _, out_loss_, acc_, p_ = sess.run([train_op, total_loss, acc, probabilities], feed_dict=feed)
                    print("step :{}, lr:{}, loss :{}, acc :{}".format(step_, _[1], out_loss_, acc_))
                    return out_loss_, p_, y_

                def dev_step(ids, mask, segment, y_):
                    feed = {input_ids: ids,
                            input_mask: mask,
                            segment_ids: segment,
                            labels: y_,
                            keep_prob: 1.0
                            }
                    out_loss_, acc_, p_ = sess.run([total_loss, acc, probabilities], feed_dict=feed)
                    print("loss :{}, acc :{}".format(out_loss_, acc_))
                    return out_loss_, p_, y_

                min_total_loss_dev = 999999
                step = 0
                for epoch in range(num_train_epochs):
                    iii = ("epoch-" + str(epoch)).center(20)
                    _ = f"{iii:*^100s}"
                    print(_)
                    # 读取训练数据
                    total_loss_train = 0
                    # total_pre_train = []
                    # total_true_train = []
                    input_ids2, input_mask2, segment_ids2, labels2 = self.get_input_data("train")
                    for i in range(num_train_steps):
                        step += 1
                        ids_train, mask_train, segment_train, y_train = sess.run(
                            [input_ids2, input_mask2, segment_ids2, labels2])
                        out_loss, pre, y = train_step(ids_train, mask_train, segment_train, y_train, step)
                        total_loss_train += out_loss
                        # total_pre_train.extend(pre)
                        # total_true_train.extend(y)

                        if step % eval_per_step == 0 and step >= self.train_config.eval_start_step:
                            total_loss_dev = 0
                            dev_input_ids2, dev_input_mask2, dev_segment_ids2, dev_labels2 = self.get_input_data("dev")
                            # total_pre_dev = []
                            # total_true_dev = []
                            for j in range(num_dev_steps):  # 一个 epoch 的 轮数
                                ids_dev, mask_dev, segment_dev, y_dev = sess.run(
                                    [dev_input_ids2, dev_input_mask2, dev_segment_ids2, dev_labels2])
                                out_loss, pre, y = dev_step(ids_dev, mask_dev, segment_dev, y_dev)
                                total_loss_dev += out_loss
                                # total_pre_dev.extend(pre)
                                # total_true_dev.extend(y_dev)
                            #
                            print("dev result report:")
                            print("total_loss_dev:{}".format(total_loss_dev))
                            # print(classification_report(total_true_dev, total_pre_dev, digits=4))

                            if total_loss_dev < min_total_loss_dev:
                                print(f"save model:\t{min_total_loss_dev}\t>{total_loss_dev}")
                                min_total_loss_dev = total_loss_dev

                                saver.save(sess, model_path, global_step=step)
                        elif step < self.train_config.eval_start_step and step % self.train_config.auto_save == 0:
                            print("auto save model")
                            saver.save(sess, model_path, global_step=step)
                    print("total_loss_train:{}".format(total_loss_train))
                    # print(len(total_true_train))
                    # print(classification_report(total_true_train, total_pre_train, digits=4))

            sess.close()

        print("remove dropout in predict")
        tf.reset_default_graph()
        input_ids = tf.placeholder(tf.int64, shape=[None, seq_len], name='input_ids')
        input_mask = tf.placeholder(tf.int64, shape=[None, seq_len], name='input_mask')
        segment_ids = tf.placeholder(tf.int64, shape=[None, seq_len], name='segment_ids')
        labels = tf.placeholder(tf.int64, shape=[None, seq_len], name='labels')
        keep_prob = tf.placeholder(tf.float32, name='keep_prob')

        (_, _, _, _) = self.create_model(input_ids, input_mask, segment_ids, labels, is_training=False)
        init_global = tf.global_variables_initializer()
        saver = tf.train.Saver(tf.global_variables(), max_to_keep=1)

        try:
            checkpoint = tf.train.get_checkpoint_state(self.train_config.save_path)
            input_checkpoint = checkpoint.model_checkpoint_path
            print("[INFO] input_checkpoint:", input_checkpoint)
        except Exception as e:
            input_checkpoint = self.train_config.save_path
            print("[INFO] Model folder", self.train_config.save_path, repr(e))

        with tf.Session(config=gpu_config) as sess:
            sess.run(init_global)
            saver.restore(sess, input_checkpoint)
            saver.save(sess, model_path)
        sess.close()

    def load_model(self, model_path):
        """
        加载训练好的模型文件
        :param model_path:
        :return:
        """
        model_path = tf.train.latest_checkpoint(model_path)
        self.graph = tf.Graph()
        with self.graph.as_default():
            gpu_config = tf.ConfigProto()
            gpu_config.gpu_options.allow_growth = True
            self.sess = tf.Session(config=gpu_config)

            self.input_ids_p = tf.placeholder(tf.int32, [None, self.train_config.max_seq_length], name="input_ids")
            self.input_mask_p = tf.placeholder(tf.int32, [None, self.train_config.max_seq_length], name="input_mask")
            self.segment_ids_p = tf.placeholder(tf.int32, [None, self.train_config.max_seq_length], name="segment_ids")
            self.labels = tf.placeholder(tf.int64, shape=[None, self.train_config.max_seq_length], name='labels')
            self.keep_prob = tf.placeholder(tf.float32, name='keep_prob')

            (_, _, _, self.probabilities) = self.create_model(self.input_ids_p, self.input_mask_p, self.segment_ids_p,
                                                              self.labels, is_training=False)

            tvars = tf.trainable_variables()
            (_, initialized_variable_names) = modeling.get_assignment_map_from_checkpoint(tvars, model_path)
            init_vars = [v for v in tf.global_variables() if v.name in initialized_variable_names]
            init_vars_name = [v.name for v in init_vars]
            saver = tf.train.Saver(init_vars, max_to_keep=1)
            saver.restore(self.sess, model_path)
            tvars = tf.global_variables()
            not_initialized_vars = [v for v in tvars if v.name not in init_vars_name]
            print('all size %s; not initialized size %s' % (len(tvars), len(not_initialized_vars)))
            print('all size %s; not initialized size %s' % (len(tvars), len(not_initialized_vars)))
            for v in not_initialized_vars:
                print(f'not initialized: {v.name}')
                print(f'not initialized: {v.name}')
            if len(not_initialized_vars):
                self.sess.run(tf.variables_initializer(not_initialized_vars))

    def predict_sequence_label(self, text):
        """
        输出 每个 字符对应的标签， 这里不做 decoder（不同标注格式，处理不一样）
        """
        seq_len = self.data_processor.max_seq_length
        features = []
        feature = self.data_processor.process_one_example_sequence(text, len(text) * ["O"], max_seq_len=seq_len)
        features.append(feature)

        with self.graph.as_default():
            feed = {self.input_ids_p: [feature[0] for feature in features],
                    self.input_mask_p: [feature[1] for feature in features],
                    self.segment_ids_p: [feature[2] for feature in features],
                    self.keep_prob: 1.0
                    }
            [probabilities] = self.sess.run([self.probabilities], feed)

            result = []
            for v in probabilities[0][1:len(text) + 1]:
                result.append(self.data_processor.id2label[int(v)])
            return result

    def predict_sequence_label_batch(self, texts):
        seq_len = self.data_processor.max_seq_length
        features = []
        for text in texts:
            feature = self.data_processor.process_one_example_sequence(text, len(text) * ["O"], max_seq_len=seq_len)
            features.append(feature)

        with self.graph.as_default():
            feed = {self.input_ids_p: [feature[0] for feature in features],
                    self.input_mask_p: [feature[1] for feature in features],
                    self.segment_ids_p: [feature[2] for feature in features],
                    self.keep_prob: 1.0
                    }
            [probabilities] = self.sess.run([self.probabilities], feed)
            results = []
            for i in range(len(texts)):
                result = []
                for v in probabilities[i][1:len(texts[i]) + 1]:
                    result.append(self.data_processor.id2label[int(v)])
                results.append(result)
            return results
