#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#

"""
trainer
"""

from absl import app, logging, flags


FLAGS = flags.FLAGS


def calc_step_rate(mode, min_lr, max_lr, stop_step, update_step):
    if mode == 1:
        step_rate = (max_lr - min_lr) / (stop_step / update_step)
    elif mode == 2:
        step_rate = (max_lr / min_lr) ** (update_step / (stop_step * 1.0))
    else:
        step_rate = 0
    return step_rate


def set_lr_customized_schedule():
    """
    lr scheduling mode
        - no valid
        - set summary step to be 1
    """
    app.flags.FLAGS.data_per_valid = 0
    app.flags.FLAGS.steps_per_summary = 1

    logging.warning(
        '  -lr schedule mode: {} min lr: {} max lr: {} in {} steps per {} steps'.format(FLAGS.lr_schedule_mode,
                                                                                        FLAGS.learning_rate,
                                                                                        FLAGS.lr_schedule_max,
                                                                                        FLAGS.stop_steps,
                                                                                        FLAGS.lr_schedule_update_step))
    logging.warning('      step rate {}'.format(calc_step_rate(FLAGS.lr_schedule_mode,
                                                               FLAGS.learning_rate,
                                                               FLAGS.lr_schedule_max,
                                                               FLAGS.stop_steps,
                                                               FLAGS.lr_schedule_update_step)))
    logging.warning('      data_per_valid set to {}'.format(FLAGS.data_per_valid))
    logging.warning('      steps_per_summary set to {}'.format(FLAGS.steps_per_summary))


def check_fidelity():
    """
    check flags fidelity and issue warning if there is potential conflict in flag settings
    """
    pass


def set_usage_model():
    logging.warning('*' * 25 + 'Setting Usage Model' + '*' * 25)

    if flags.FLAGS.lr_schedule_mode != 0:
        set_lr_customized_schedule()

    check_fidelity()

    logging.warning('*' * 23 + 'Done Setting Usage Model' + '*' * 22)
