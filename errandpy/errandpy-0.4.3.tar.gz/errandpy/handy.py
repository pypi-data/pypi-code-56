import gc, numpy


def tell_me_z0(x, y, **kwargs):
    from errandpy.trainer import Trainer
    x, y = __order_xy(x, y)
    trainer = Trainer(x, y)
    if "name" in kwargs:
        trainer.name = kwargs["name"]
    else:
        trainer.name = "handy_analyze"
    if "early_stop_val" in kwargs:
        trainer.early_stop_val = float(kwargs["early_stop_val"])

    if "learning_rate" in kwargs:
        trainer.learning_rate = float(kwargs["learning_rate"])

    if "accurate" in kwargs:
        trainer.accurate = float(kwargs["accurate"])

    show_graph = True
    if "show_graph" in kwargs:
        show_graph = kwargs["show_graph"]

    # trainer.boundary_index_step_accurate = 30

    trainer.all_fit_flag = -1

    arg = trainer.start_fitting(expected_cost=0.0, showGraph=show_graph, boundary_bias=0)
    boundary_index = arg[7]
    error_index = arg[8]
    z0 = trainer.boundaryLerp(boundary_index, error_index)

    del trainer, x, y
    gc.collect()
    return z0, [arg[3], arg[4], arg[5], arg[6]]


def extract_short_range(x, y, z0=None, **kwargs):
    if z0 is None:
        z0 = tell_me_z0(x, y, **kwargs)[0]

    from errandpy.trainer import Trainer
    x, y = __order_xy(x, y)
    trainer = Trainer(x, y)
    if "name" in kwargs:
        trainer.name = kwargs["name"]
    else:
        trainer.name = "handy_analyze"
    if "early_stop_val" in kwargs:
        trainer.early_stop_val = float(kwargs["early_stop_val"])

    if "learning_rate" in kwargs:
        trainer.learning_rate = float(kwargs["learning_rate"])

    if "accurate" in kwargs:
        trainer.accurate = float(kwargs["accurate"])

    if "judge_threshold" in kwargs:
        trainer.judge_threshold = float(kwargs["judge_threshold"])

    show_graph = True
    if "show_graph" in kwargs:
        show_graph = kwargs["show_graph"]
    """
        return [self.resultParam.boundaryBias, self.resultParam.variant, self.resultParam.best_cost,
            self.resultParam.best_a, self.resultParam.best_b,
            self.resultParam.best_c, self.resultParam.best_d,
            self.resultParam.boundaryIndex, self.resultParam.errorIndex]
    """
    arg = trainer.start_master_fitting(z0, showGraph=show_graph)
    print("finished! log file saved in ./Outputs/" + "Master@" + trainer.name + ".log")

    dict = {}
    dict["a"] = arg[3]
    dict["b"] = arg[4]
    dict["c"] = arg[5]
    dict["d"] = arg[6]
    dict["z0"] = arg[7]
    dict["ze"] = arg[8]
    del trainer, x, y
    gc.collect()
    return dict


def __order_xy(x, y):
    if x[0] - x[1] > 0:
        return numpy.flipud(x), numpy.flipud(y)
    return x, y
