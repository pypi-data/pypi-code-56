from __future__ import print_function

import os
import sys

import matplotlib.pyplot as plt
import numpy
import tensorflow as tf
import errandpy
import errandpy.utility as Utility


class Agent(object):

    def __init__(self, train_x, train_y, training_epochs=100, name="Trainer"):
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

        self.training_epochs = training_epochs

        self.train_X = train_x
        self.train_Y = train_y

        self.name = name
        self.showGraph = True
        self.accurate = 0.99
        self.normalized_delta = 1
        self.normalized_min = 1
        """
            Trainerが訓練中改変するパラメータ
        """
        class ResultParam:
            def __init__(self):
                self.variant = False
                self.freezeBoundaryIndex = False
                self.boundaryIndex = 0
                self.boundaryBias = 0
                self.best_a = 0
                self.best_b = 0
                self.best_c = 0
                self.best_d = 0
                self.best_cost = 0
                self.mean_r = 0
                self.errorIndex = 0

        class SettingParam:
            def __init__(self):
                self.enable_tensorboard = errandpy.enable_tensorboard
                self.display_step = errandpy.display_step
                self.learning_rate = 0.000002
                self.beta1 = 0.9
                self.beta2 = 0.999

        """
            学習するための情報が格納されています. 改変する必要がない.
        """
        class CacheParam:

            def __init__(self, agent: Agent):
                self.arrayCount = len(agent.train_X)
                # logfileの変数
                self.logfile_inited = False

                # 最初に定義したキャッシュ
                self.init_boundaryIndex = 0
                self.init_bias = 0
                self.init_a = 0
                self.init_b = 0
                self.init_c = 0
                self.init_d = 0

                self.flag = 0
                self.training = False

        self.settingParam = SettingParam()
        self.resultParam = ResultParam()
        self.cacheParam = CacheParam(self)

# region Error Index and Boundary Index
    def __re_education_y_fit(self, array_x, array_y, a, b, c, d):
        long_y = Utility._f_long(array_x, a, b, c, d)

        result = Agent.get_boundary_index(numpy.asarray(array_y - long_y))
        # clamp the z0
        result = Utility.clamp(0, self.cacheParam.arrayCount - 1, result + self.resultParam.boundaryBias)
        return long_y, result

    @staticmethod
    def get_error_index(fited_y):
        count = len(fited_y)
        std = numpy.std(fited_y[int(count / 2):]) * errandpy.ze_factor
        i = count - 5
        while i > 5:
            i -= 1
            # ave = numpy.average(fited_y[i:i+10])
            if fited_y[i] < -0.01 - std and fited_y[i-5] < -0.01 - std:
                break
        return i-5

    @staticmethod
    def get_boundary_index(fited_y):
        diff_Y = numpy.abs(numpy.diff(fited_y, n=1))
        diff_count = len(diff_Y)
        # plt.plot(diff_Y)
        # plt.show()

        hist_count = 100
        hist, bins = numpy.histogram(diff_Y, bins=hist_count, range=(0, max(diff_Y)))

        # plt.hist(diff_Y, bins=hist_count, range=(0,diff_Y_sorted[1]))
        # plt.show()
        # 　分散の返り値, 1: 閾値index, 2:分散の分子の値
        s_max = (0, -1)

        for th in range(0, hist_count):
            sum1 = numpy.sum(hist[:th])
            sum2 = numpy.sum(hist[th:])

            if sum1 == 0:
                m1 = 0
            else:
                m1 = numpy.sum(i * hist[i] for i in range(0, th)) / sum1

            if sum2 == 0:
                m2 = 0
            else:
                m2 = numpy.sum(i * hist[i] for i in range(th, hist_count)) / sum2

            # m1(傾きが小さい)の分散はm2より少なくならないといけない
            if m1 > m2:
                continue

            s = sum1 * sum2 * (m1 - m2) ** 2

            if s > s_max[1]:
                s_max = (th, s)

        i = int(diff_count / 2)
        while i < diff_count:
            if i >= diff_count - 5:
                diff = diff_Y[diff_count - i]
            else:
                diff = (diff_Y[diff_count - i] + diff_Y[diff_count - i - 3] + diff_Y[diff_count - i - 5]) / 3.0
            # diff = diff_Y[diff_count - i]
            if diff > bins[s_max[0]]:
                # print(diff, bins[s_max[0]])
                i += 1
                break
            else:
                i += 1
        # これは境界での差分値, 小さいことは短距離力も小さい
        if errandpy.s_max_debug:
            print("smax", bins[s_max[0]])
        # greater_than_threshold = [i for i, val in enumerate(diff_Y) if val > bins[s_max[0]]]
        # plt.plot(fited_y)
        # plt.plot(greater_than_threshold, fited_y[greater_than_threshold], linestyle='none', color='r', marker='o')
        # plt.show()
        #                   0.0135
        if bins[s_max[0]] < errandpy.s_max_threshold:
            return 0
        else:
            # print(diff_count - i)
            return diff_count - i
# endregion

# region Utility Equation

    @staticmethod
    def normalized(array):
        return Utility.normalized(array, 1, -1)

    @staticmethod
    def activation(x, a, b, c, d):
        if errandpy.useLegacyModel:
            mul = tf.multiply(x, c)
            add = tf.add(mul, tf.constant(1.0))
        else:
            add = tf.add(x, c)

        pow = tf.pow(add, d)
        div = tf.divide(b, pow)
        return tf.subtract(a, div)

    @staticmethod
    def huber_loss(labels, predictions, delta=0.02):
        residual = tf.abs(predictions - labels)
        condition = tf.less(residual, delta)
        small_res = 0.5 * tf.square(residual)
        large_res = delta * residual - 0.5 * tf.square(delta)
        return tf.where(condition, small_res, large_res, name="boundary_fit")

    @staticmethod
    def errorIndexMap(arrayCount):
        x = numpy.linspace(0, 1, arrayCount)
        y = 1 - (1 - x)**3
        # plt.plot(x, y)
        # plt.show()

# endregion

# region File IO

    @staticmethod
    def safe_mkdir(path):
        """ Create a directory if there isn't one already. """
        try:
            os.mkdir(path)
        except OSError:
            pass

    def write_log(self, content):
        if not self.cacheParam.logfile_inited:
            # if not os.path.exists('./Outputs/'):
            #     os.mkdir('./Outputs/')
            Agent.safe_mkdir('./Outputs/')
            file = open('./Outputs/' + self.name + ".log", 'w')
            self.cacheParam.logfile_inited = True
        else:
            file = open('./Outputs/' + self.name + ".log", 'a')

        file.write(content)
        file.write('\n')
        file.close()

    def draw_plt(self, a, b, c, d, bound, ze):
        Utility.draw_plt(self.train_X, self.train_Y, a, b, c, d, bound, self.name, ze)
# endregion

    def start_fitting(self, init_a, init_b, init_c, init_d, boundary_bias=0,
                      freeze_boundaryIndex=False, callback=None, ignore_error_index=False):
        print("Start Fitting")
        self.write_log("normalize_min: " + str(self.normalized_min))
        self.write_log("normalize_delta: " + str(self.normalized_delta))

        self.cacheParam.training = True

        self.resultParam.freezeBoundaryIndex = freeze_boundaryIndex
        self.resultParam.boundaryBias = boundary_bias
        self.cacheParam.init_bias = boundary_bias
        if init_a is None:
            """""
                a,b,c,dはNoneで渡されるときa,b,c,dの処置
            """""
            # aのパラメータの制約条件
            _sample_count = len(self.train_Y)
            _ave_count = int(_sample_count / 20)

            init_a = errandpy.init_a
            init_b = errandpy.init_b
            init_c = errandpy.init_c
            init_d = errandpy.init_d
            self.cacheParam.init_boundaryIndex = 0
        else:
            """""
                キャッシュパラメータの更新
            """""
            self.cacheParam.init_a = init_a
            self.cacheParam.init_b = init_b
            self.cacheParam.init_c = init_c
            self.cacheParam.init_d = init_d

            re_YFit = self.__re_education_y_fit(self.train_X, self.train_Y, init_a, init_b, init_c, init_d)
            self.cacheParam.init_boundaryIndex = re_YFit[1]

        print(self.name + "@Set Learning Rate ", self.settingParam.learning_rate)
        print("Set Boundary Bias", self.resultParam.boundaryBias)
        print("Init Boundary Index", self.cacheParam.init_boundaryIndex)
        print("Set A Init ", init_a)
        print("Set B Init ", init_b)
        print("Set C Init ", init_c)
        print("Set D Init ", init_d)

        """""
        Training環境の構築
        """""
        X_b = tf.placeholder(tf.float32, name="x_b")
        Y_b = tf.placeholder(tf.float32, name="y_b")
        X_e = tf.placeholder(tf.float32, name="x_e")
        Y_e = tf.placeholder(tf.float32, name="y_e")
        BoundaryIndex = tf.placeholder(tf.float32, name="z0")

        a = tf.Variable(float(init_a), name="A")
        b = tf.Variable(float(init_b), name="B")
        c = tf.Variable(float(init_c), name="C")
        d = tf.Variable(float(init_d), name="D")

        valueCount = tf.constant(float(self.cacheParam.arrayCount), name="value_count")

        with tf.name_scope("model"):
            activation_b = Agent.activation(X_b, a, b, c, d)
            activation_e = Agent.activation(X_e, a, b, c, d)

        with tf.name_scope("loss_function"):
            boundaryWeight = tf.multiply(tf.divide(valueCount, tf.subtract(valueCount, BoundaryIndex)), 2, name="weight_b")
            # errorWeight

            if ignore_error_index:
                cost_Y_b = tf.abs(activation_b - Y_b, name="boundary_fit")
            else:
                cost_Y_b = self.huber_loss(activation_b, Y_b, self.accurate)
            #
            cost_Y_e = tf.abs(activation_e - Y_e, name="error_fit")

            """
                ここのコスト関数はboundary_indexとerror_indexよりshapeは常に変化している
                重み関数も同じく更新しないといけない
            """
            cost_optimize = tf.add(tf.reduce_sum(cost_Y_e),
                                   tf.reduce_sum(tf.multiply(cost_Y_b, boundaryWeight)))

        with tf.name_scope("AdamOptimizer"):
            optimizer = tf.train.AdamOptimizer(learning_rate=self.settingParam.learning_rate,
                                               beta1=self.settingParam.beta1,
                                               beta2=self.settingParam.beta2).minimize(cost_optimize)

        with tf.name_scope("Limiter"):
            limiter_d = tf.assign(d, tf.clip_by_value(d, errandpy.d_limiter[0], errandpy.d_limiter[1]))

        self.resultParam.best_cost = sys.float_info.max

        if self.settingParam.enable_tensorboard:
            tf.summary.scalar("cost", cost_optimize)
            tf.summary.scalar("a", a)
            tf.summary.scalar("b", b)
            tf.summary.scalar("c", c)
            tf.summary.scalar("d", d)
            summary_optimize = tf.summary.merge_all()

        with tf.Session() as sess:
            sess.run(tf.global_variables_initializer())
            if self.settingParam.enable_tensorboard:
                writer = tf.summary.FileWriter('./graphs/' + self.name, sess.graph)

            for epoch in range(self.training_epochs):

                re_YFit = self.__re_education_y_fit(self.train_X, self.train_Y, sess.run(a),
                                                    sess.run(b), sess.run(c), sess.run(d))

                if self.resultParam.freezeBoundaryIndex:
                    BI = Utility.clamp(0, self.cacheParam.arrayCount - 1, self.resultParam.boundaryBias)
                elif self.cacheParam.flag < 0:
                    BI = self.resultParam.boundaryBias
                    self.cacheParam.flag += 1
                else:
                    BI = re_YFit[1]
                    # print("BI: ", BI)
                    # print("Bias: ", self.resultParam.boundaryBias)

                if ignore_error_index:
                    error_index = self.cacheParam.arrayCount - 1
                else:
                    shortRange_YFit = self.train_Y - re_YFit[0]
                    error_index = self.get_error_index(shortRange_YFit)

                for i in range(0, self.cacheParam.arrayCount):
                    sess.run(optimizer, feed_dict={
                        X_b: self.train_X[BI:], Y_b: self.train_Y[BI:], BoundaryIndex: BI,
                        X_e: self.train_X[error_index:], Y_e: self.train_Y[error_index:]})

                    sess.run(limiter_d)

                if self.settingParam.enable_tensorboard:
                    cost, summery = sess.run([cost_optimize, summary_optimize],
                                             feed_dict={X_b: self.train_X[BI:], Y_b: self.train_Y[BI:],
                                                        BoundaryIndex: BI,
                                                        X_e: self.train_X[error_index:],
                                                        Y_e: self.train_Y[error_index:]})

                    writer.add_summary(summery, epoch)
                else:
                    cost = sess.run(cost_optimize,
                                    feed_dict={X_b: self.train_X[BI:], Y_b: self.train_Y[BI:], BoundaryIndex: BI,
                                               X_e: self.train_X[error_index:],
                                               Y_e: self.train_Y[error_index:]})

                mean_r = Utility.mean_r(self.train_X[BI:], self.train_Y[BI:],
                                     sess.run(a), sess.run(b), sess.run(c), sess.run(d))
                if self.settingParam.enable_tensorboard:
                    summery1 = tf.Summary()
                    summery1.value.add(tag="mean_r", simple_value=mean_r)
                    writer.add_summary(summery1, epoch)
                """
                    表示とファイルの書き込み
                """
                if epoch % self.settingParam.display_step == 0:

                    if numpy.isnan(cost):
                        print("Warning: Too large learning rate, Restarting fitting with smaller learning rate")
                        self.settingParam.learning_rate /= 2.
                        self.cacheParam.logfile_inited = True
                        return self.start_fitting(init_a, init_b, init_c, init_d, boundary_bias, freeze_boundaryIndex,
                                                  callback)

                    log = self.name + "@Epoch: " + str(epoch + 1) + " " + "cost= " + str(cost) + " " + "a= " + str(
                        sess.run(a)) + " " + "b= " + str(sess.run(b)) + " " + "c= " + str(sess.run(c)) + " " + "d= " \
                          + str(sess.run(d)) + " " + "z_0= " + str(BI) + " " + "z_e= " \
                          + str(error_index) + " " + "bias= " + str(self.resultParam.boundaryBias)

                    self.write_log(log)
                    print(log)
                    if self.showGraph:
                        self.draw_plt(sess.run(a), sess.run(b), sess.run(c), sess.run(d), BI, error_index)
                        plt.draw()
                        plt.pause(0.01)

                    if callback is not None:
                        callback([self.resultParam.boundaryBias, self.resultParam.variant, cost,
                                  sess.run(a), sess.run(b), sess.run(c), sess.run(d), BI])

                """
                    一番良いa,b,c,dの記録
                """
                if cost < self.resultParam.best_cost or mean_r >= self.resultParam.mean_r:
                    self.resultParam.best_cost = cost
                    self.resultParam.boundaryIndex = BI
                    self.resultParam.best_a = sess.run(a)
                    self.resultParam.best_b = sess.run(b)
                    self.resultParam.best_c = sess.run(c)
                    self.resultParam.best_d = sess.run(d)
                    self.resultParam.mean_r = mean_r
                    self.resultParam.errorIndex = error_index

                """
                    最後の処理
                """
                if epoch == self.training_epochs - 1 or not self.cacheParam.training:
                    best_a = self.resultParam.best_a
                    best_b = self.resultParam.best_b
                    best_d = self.resultParam.best_d
                    best_c = self.resultParam.best_c
                    self.write_log("Optimization Finished!")
                    self.write_log(
                        "cost= " + str(self.resultParam.best_cost) + " " + "a= " + str(best_a) + " " + "b= " + str(
                            best_b) + " " + "c= " + str(best_c) + " " + "d= " + str(best_d) + " " + "z0_index= " +
                        str(self.resultParam.boundaryIndex) + " " + "ze_index= " + str(self.resultParam.errorIndex))

                    self.draw_plt(best_a, best_b, best_c, best_d, self.resultParam.boundaryIndex, None)
                    import os.path
                    root, ext = os.path.splitext(self.name)
                    if ext != "":
                        plt.savefig("Outputs/" + self.name + ".png")
                    else:
                        plt.savefig("Outputs/" + self.name)

                    break

        if self.settingParam.enable_tensorboard:
            writer.close()
        sess.close()
        plt.close()
        return [self.resultParam.boundaryBias, self.resultParam.variant, self.resultParam.best_cost,
                float((self.resultParam.best_a + 1) * self.normalized_delta + self.normalized_min),
                float(self.resultParam.best_b * self.normalized_delta), self.resultParam.best_c, self.resultParam.best_d,
                self.resultParam.boundaryIndex, self.resultParam.errorIndex]
