"""
change the global setting here
"""

useLegacyModel = True

ze_factor = 3

# region trainer Setting
t_LR = 0

v_th = 10**-6

first_stage_learning_rate = 10**-4

second_stage_learning_rate = 10**-6

first_stage_counter = 3

second_stage_counter = 5

# endregion

# region agent Setting
s_max_threshold = 0.0

s_max_debug = False

display_step = 5

enable_tensorboard = False

d_limiter = (0.5, 1.5)

init_a = 0
init_b = 1
init_c = 1
init_d = 1

z0_ze_range = 50

# endregion
