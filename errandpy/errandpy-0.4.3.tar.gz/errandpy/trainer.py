from __future__ import print_function

import gc
import time
import numpy

import errandpy
import errandpy.utility as Utility

from errandpy.agent import Agent


class Trainer(object):

    def __init__(self, train_X, train_Y, should_normalize=True, normalized_min=0, normalized_delta=0):

        self.name = ""

        self.train_X = numpy.asarray(train_X, numpy.float32)
        self.train_Y = numpy.asarray(train_Y, numpy.float32)

        # boundary biasを変えるstep
        self.biasStep = 10

        # 実験データのノイズの多さから設定する, 例えばノイジーのデータならaccurateを落としたほうが計算が幸せになる
        # でもaccurateを落とすとfittingの質が悪くなるかも
        self.accurate = 0.99
        # boundary indexがどれぐらいずれでも平気?
        self.boundary_index_step_accurate = 50
        #
        self.all_fit_flag = 0

        self.judge_threshold = 0.01

        # 分散が計算されるときのカウンター, 計算回数が収束できるような値がいい
        # 例えばagentのdisplay_step = 5のとき5回をカウントしたら25回で収束できるから5で設定している
        self.testCounter = errandpy.first_stage_counter
        self.masterCounter = errandpy.second_stage_counter

        self.early_stop_val = errandpy.v_th
        self.t_LR = errandpy.t_LR

        class CacheParam:

            def __init__(self, trainer):
                if should_normalize:
                    result = Utility.normalized(trainer.train_Y, bias=-1)
                    # yの正規化とパラメータ
                    self.train_Y_normalized = result[0]
                    self.normalized_min = result[1]
                    self.normalized_delta = result[2]
                else:
                    self.train_Y_normalized = trainer.train_Y
                    self.normalized_min = normalized_min
                    self.normalized_delta = normalized_delta
                self.arrayCount = len(trainer.train_Y)
                self.diff_train_Y_normalized = numpy.diff(self.train_Y_normalized)
                self.update_time = 0
                self.best_update_time = 0

        self.cacheParam = CacheParam(self)

    def boundaryLerp(self, z_b, z_e):
        if z_e >= z_b:
            return int(z_b)
        else:
            return int(z_e + (z_b - z_e) * self.t_LR)

    def onFittingTestFinish(self, args):
        print("Fitting Test finished")
        print("best result: a:", args[3], "b:", args[4], "c:", args[5], "d:", args[6], "cost", args[2], "z0_index:",
              args[7], "ze_index", args[8])

    def onMasterTestFinish(self, args):
        print("Master finished")
        print("best result: a:", args[3], "b:", args[4], "c:", args[5], "d:", args[6], "cost", args[2], "z0_index:",
              args[7], "ze_index", args[8])

    def start_master_fitting(self, index, showGraph=True, expectCost=9999):

        cost_list = numpy.zeros(self.masterCounter)

        def onProcessUpdate(args):
            cost_list[self.cacheParam.update_time % self.masterCounter] = args[2]
            self.cacheParam.update_time += 1

            # 十分な回数を学習させる, costはtestfittingのcostより少ないはず
            if self.cacheParam.update_time >= self.masterCounter + 1 or args[2] <= expectCost:
                # 最適な学習パラメータの変動が少ない場合, 学習中止かboundary index変えるを判断
                # print(numpy.var(cost_list))
                if numpy.var(cost_list) < self.early_stop_val:
                    agent.cacheParam.training = False

        agent = Agent(self.train_X, self.cacheParam.train_Y_normalized, name="Master@"+self.name, training_epochs=2000)
        agent.normalized_delta = self.cacheParam.normalized_delta
        agent.normalized_min = self.cacheParam.normalized_min
        agent.settingParam.learning_rate = errandpy.second_stage_learning_rate
        agent.showGraph = showGraph
        args = agent.start_fitting(None, None, None, None, index, True, callback=onProcessUpdate, ignore_error_index=True)

        time.sleep(1)
        self.onMasterTestFinish(args)

        del agent
        gc.collect()
        return args

    def start_fitting(self, expected_cost, showGraph=True, boundary_bias=0):

        cost_list = numpy.zeros(self.testCounter)
        best_cost_list = numpy.zeros(self.testCounter)
        """
            agentのパラメータ更新するときTrainerに知らせる
          0      [self.resultParam.boundaryBias,
          1      self.resultParam.variant,
          2      self.resultParam.best_cost,
          3      self.resultParam.best_a,
          4      self.resultParam.best_b,
          5      self.resultParam.best_c,
          6      self.resultParam.best_d,
          7      self.resultParam.boundaryIndex,
          8      self.resultParam.errorIndex]
          渡されるargsは最適なパラメータではなく現在のパラメータ
        """
        def onProcessUpdate(args):
            cost_list[self.cacheParam.update_time % self.testCounter] = agent.resultParam.best_cost
            self.cacheParam.update_time += 1

            # 十分な回数を学習させる
            if self.cacheParam.update_time >= self.testCounter + 1:
                # 最適な学習パラメータの変動が少ない場合, 学習中止かboundary index変えるを判断
                # print(numpy.var(cost_list) / args[2])
                if numpy.var(cost_list) < self.judge_threshold:
                    best_cost_list[self.cacheParam.best_update_time % self.testCounter] = agent.resultParam.best_cost
                    self.cacheParam.best_update_time += 1

                    self.cacheParam.update_time = 0

                    fited_Y = (self.cacheParam.train_Y_normalized - Utility._f_long(self.train_X, args[3], args[4],
                                                                                    args[5], args[6]))
                    error_index = Agent.get_error_index(fited_Y)

                    step = self.__should_bias_warp(fited_Y, args[7], error_index)
                    if step != 0:
                        agent.resultParam.boundaryBias += step
                        print("@" + self.name, " (0)add boundary bias: ", step)
                    # costが期待されるコストより小さな時終了させる
                    elif (agent.resultParam.best_cost < expected_cost or (numpy.var(best_cost_list) < 0.00001)
                            and self.cacheParam.best_update_time > self.testCounter) \
                            and numpy.sum(fited_Y[:args[7]]) < 0.1 * args[7]\
                            and numpy.abs(agent.resultParam.boundaryIndex - args[7]) < 100:
                        print("end, cost:", agent.resultParam.best_cost, "var:", numpy.var(best_cost_list))
                        agent.cacheParam.training = False

                    # boundary indexをずらすことを試みる, 右にずらすか左にずらすかの2通りの場合がある
                    # 実際の判断基準は下の関数を参照する
                    else:

                        if self.__should_bias_forward(fited_Y, args[7], error_index, self.train_X[1]-self.train_X[0]):
                            agent.resultParam.boundaryBias += self.biasStep
                            print("@" + self.name, " (1)add boundary bias: ", self.biasStep)
                        elif self.__should_bias_backward(fited_Y, args[7], error_index, self.train_X[1]-self.train_X[0]):
                            agent.resultParam.boundaryBias -= self.biasStep
                            print("@" + self.name, " (2)add boundary bias: ", -self.biasStep)
                        else:
                            pass

        agent = Agent(self.train_X, self.cacheParam.train_Y_normalized, name="Test@"+self.name, training_epochs=500)

        agent.normalized_delta = self.cacheParam.normalized_delta
        agent.normalized_min = self.cacheParam.normalized_min
        agent.settingParam.learning_rate = errandpy.first_stage_learning_rate
        agent.cacheParam.flag = self.all_fit_flag
        agent.showGraph = showGraph
        args = agent.start_fitting(None, None, None, None, boundary_bias, False, callback=onProcessUpdate)

        time.sleep(1)
        self.onFittingTestFinish(args)

        del agent
        gc.collect()
        return args


    @staticmethod
    def __get_boundary_index(train_X, a, b, c, d, train_Y_normalized):
        fited_Y = train_Y_normalized - Utility._f_long(train_X, a, b, c, d)
        return Agent.get_boundary_index(fited_Y)

    def __should_bias_forward(self, fit_y, boundary_index, error_index, delta):
        if 0 < boundary_index - error_index < self.biasStep:
            return False

        int_fb = numpy.sum(fit_y[boundary_index:])
        # int_fe = numpy.sum(fit_y[error_index+self.biasStep:]) * delta
        # var_fb = numpy.var(fit_y[error_index:] * 100)

        # print("int_fb: ", int_fb)
        # print("int_fe: ", int_fe)
        # print("forward")

        if boundary_index < error_index:
            # boundary indexが短距離力に寄りすぎ
            if int_fb < 0:
                return True
            # boundary index以降で斥力成分は大きい
            # if int_fe - int_fb > 1 - self.accurate:
            #     return True
        else:
            # boundary index以降の場所は平らになっていない
            value = numpy.sum(fit_y[boundary_index:boundary_index + self.biasStep]) * delta
            # print("v", value)
            if value < self.accurate - 1:
                return True

        return False

    def __should_bias_backward(self, fit_y, boundary_index, error_index, delta):
        if 0 < boundary_index - error_index < self.biasStep:
            return False

        # int_fb = numpy.sum(fit_y[boundary_index:]) * delta
        # int_fe = numpy.sum(fit_y[error_index:]) * delta
        # print("backward")
        if boundary_index > error_index + self.biasStep:
            # boundary index前の場所は平らになっているのか
            value = numpy.sum(fit_y[boundary_index - self.biasStep:boundary_index])
            # print("v", value)
            if 0 < value:
                return True
            # elif int_fe - int_fb > 1 - self.accurate:
            #     return True

        return False

    def __should_bias_warp(self, fit_y, boundary_index, error_index):
        if boundary_index - error_index > errandpy.z0_ze_range:
            return int((error_index - boundary_index) * 0.5)

        # sum = numpy.sum(fit_y[:boundary_index])
        # max_index = numpy.argmax(fit_y[error_index:])

        # print("sum:", sum, numpy.sum(fit_y[boundary_index:]))
        # boundary indexの後ろ斥力が出ている さらにboundary indexの計算は誤っている(error indexより小さい)
        # if sum > (1 - self.accurate) * boundary_index + 1 \
        #         and boundary_index < error_index - self.boundary_index_step_accurate:
        #     # print("boundary reset")
        #     if numpy.sum(fit_y[boundary_index:]) < (self.accurate - 1) * (error_index - boundary_index) - 1:
        #         return self.boundaryLerp(error_index, boundary_index) - boundary_index
        #     else:
        #         return int(-boundary_index / 2)

        # elif numpy.var(fit_y[boundary_index:]) < numpy.square(1 - self.accurate):
        #     i = boundary_index
        #     while i-5 >= 0:
        #         # 99%の正確率を目標にしよう
        #         # if numpy.abs(fit_y[i-5]-fit_y[boundary_index]) <= 1 - self.accurate:
        #         if numpy.abs(numpy.average(fit_y[i - 5: i + 5]) - fit_y[boundary_index]) <= 1 - self.accurate:
        #             i -= 5
        #         else:
        #             break
        #
        #     step = i - boundary_index
        #     # print("step:", step)
        #     # boundary indexが後ろすぎる時矯正する
        #     if step < -self.boundary_index_step_accurate:
        #         return step

        return 0
