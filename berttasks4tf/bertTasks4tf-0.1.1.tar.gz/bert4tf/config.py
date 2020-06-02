#!/usr/bin/python
# coding:utf8
"""
@author: Cong Yu
@time: 2020-05-16 21:27
"""


class TrainConfig:
    def __init__(self, bert_config_path,
                 label_list,
                 init_checkpoint=None,
                 train_file=None,
                 dev_file=None,
                 train_examples_len=None,
                 dev_examples_len=None,
                 keep_prob=0.9,
                 max_seq_length=128,
                 train_batch_size=64,
                 dev_batch_size=64,
                 num_train_epochs=3,
                 eval_start_step=5000,
                 eval_per_step=200,
                 auto_save=1000,
                 learning_rate=5e-5,
                 warm_up_proportion=0.1,
                 save_path="./model/",
                 use_focal_loss=False,
                 alpha=0.25,
                 gamma=2,
                 ):
        # bert 配置文件
        self.bert_config_path = bert_config_path
        # bert 预训练模型位置
        self.init_checkpoint = init_checkpoint
        # keep_prob = 0.9 , drop out 保留的比例
        self.keep_prob = keep_prob  #

        # 训练文件（tf_record）
        self.train_file = train_file
        # 验证文件（tf_record）
        self.dev_file = dev_file
        # 训练 batch_size
        self.train_batch_size = train_batch_size  # 32
        # 验证 batch_size
        self.dev_batch_size = dev_batch_size  # 32
        # 训练样本个数
        self.train_examples_len = train_examples_len
        # 验证样本个数
        self.dev_examples_len = dev_examples_len

        # 最大长度
        self.max_seq_length = max_seq_length  # 128
        # 标签l列表
        self.label_list = label_list
        # 标签个数
        self.num_labels = len(label_list)
        # 训练迭代步数
        self.num_train_epochs = num_train_epochs
        # 从多少步起 开始评估
        self.eval_start_step = eval_start_step
        # 没过多少步 进行评估
        self.eval_per_step = eval_per_step
        # 没过多少步，自动保持模型（截止到评估）
        self.auto_save = auto_save
        # 学习率
        self.learning_rate = learning_rate
        # 慢热学习的比例
        self.warm_up_proportion = warm_up_proportion
        # 模型保持路径
        self.save_path = save_path
        # 是否使用 focal_loss
        self.use_focal_loss = use_focal_loss
        # focal_loss: alpha
        self.alpha = alpha
        # focal_loss: gamma
        self.gamma = gamma
