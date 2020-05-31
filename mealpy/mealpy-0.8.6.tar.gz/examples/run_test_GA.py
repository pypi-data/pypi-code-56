#!/usr/bin/env python
# ------------------------------------------------------------------------------------------------------%
# Created by "Thieu Nguyen" at 22:08, 22/05/2020                                                        %
#                                                                                                       %
#       Email:      nguyenthieu2102@gmail.com                                                           %
#       Homepage:   https://www.researchgate.net/profile/Thieu_Nguyen6                                  %
#       Github:     https://github.com/thieunguyen5991                                                  %
#-------------------------------------------------------------------------------------------------------%

from mealpy.evolutionary_based.GA import BaseGA
from opfunu.cec_basic.cec2014_nobias import *

## Setting parameters
objective_func = F1
problem_size = 100
domain_range = [-100, 100]
log = True

epoch = 100
pop_size = 50

md1 = BaseGA(objective_func, problem_size, domain_range, log, epoch, pop_size)
best_pos1, best_fit1, list_loss1 = md1._train__()
print(best_fit1)