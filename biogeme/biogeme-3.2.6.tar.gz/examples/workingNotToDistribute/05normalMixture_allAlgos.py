"""File 05normalMixture_allAlgos.py

:author: Michel Bierlaire, EPFL
:date: Sat Sep  7 18:23:01 2019

 Example of a mixture of logit models, using Monte-Carlo integration.
 Three alternatives: Train, Car and Swissmetro
 SP data
"""
#
# Too constraining
# pylint: disable=invalid-name,
#
# Biogeme uses variables not explicitly defined in the script
# pylint: disable=undefined-variable

import pandas as pd
import biogeme.optimization as opt
import biogeme.database as db
import biogeme.biogeme as bio
import biogeme.models as models
import biogeme.messaging as msg
from biogeme.expressions import Beta, DefineVariable, bioDraws, log, MonteCarlo

# Read the data
df = pd.read_csv('swissmetro.dat', '\t')
database = db.Database('swissmetro', df)

# The Pandas data structure is available as database.data. Use all the
# Pandas functions to investigate the database. For example:
#print(database.data.describe())

# The following statement allows you to use the names of the variable
# as Python variable.
globals().update(database.variables)

# Removing some observations can be done directly using pandas.
#remove = (((database.data.PURPOSE != 1) &
#           (database.data.PURPOSE != 3)) |
#          (database.data.CHOICE == 0))
#database.data.drop(database.data[remove].index,inplace=True)

# Here we use the "biogeme" way for backward compatibility
exclude = ((PURPOSE != 1) * (PURPOSE != 3) + (CHOICE == 0)) > 0
database.remove(exclude)

# Parameters to be estimated
ASC_CAR = Beta('ASC_CAR', 0, None, None, 0)
ASC_TRAIN = Beta('ASC_TRAIN', 0, None, None, 0)
ASC_SM = Beta('ASC_SM', 0, None, None, 1)
B_COST = Beta('B_COST', 0, None, None, 0)

# Define a random parameter, normally distributed, designed to be used
# for Monte-Carlo simulation
B_TIME = Beta('B_TIME', 0, None, None, 0)

# It is advised not to use 0 as starting value for the following parameter.
B_TIME_S = Beta('B_TIME_S', 1, None, None, 0)
B_TIME_RND = B_TIME + B_TIME_S * bioDraws('B_TIME_RND', 'NORMAL')

# Definition of new variables
SM_COST = SM_CO * (GA == 0)
TRAIN_COST = TRAIN_CO * (GA == 0)

# Definition of new variables: adding columns to the database
CAR_AV_SP = DefineVariable('CAR_AV_SP', CAR_AV * (SP != 0), database)
TRAIN_AV_SP = DefineVariable('TRAIN_AV_SP', TRAIN_AV * (SP != 0), database)
TRAIN_TT_SCALED = DefineVariable('TRAIN_TT_SCALED', TRAIN_TT / 100.0, database)
TRAIN_COST_SCALED = DefineVariable('TRAIN_COST_SCALED', TRAIN_COST / 100, database)
SM_TT_SCALED = DefineVariable('SM_TT_SCALED', SM_TT / 100.0, database)
SM_COST_SCALED = DefineVariable('SM_COST_SCALED', SM_COST / 100, database)
CAR_TT_SCALED = DefineVariable('CAR_TT_SCALED', CAR_TT / 100, database)
CAR_CO_SCALED = DefineVariable('CAR_CO_SCALED', CAR_CO / 100, database)

# Definition of the utility functions
V1 = ASC_TRAIN + \
     B_TIME_RND * TRAIN_TT_SCALED + \
     B_COST * TRAIN_COST_SCALED
V2 = ASC_SM + \
     B_TIME_RND * SM_TT_SCALED + \
     B_COST * SM_COST_SCALED
V3 = ASC_CAR + \
     B_TIME_RND * CAR_TT_SCALED + \
     B_COST * CAR_CO_SCALED

# Associate utility functions with the numbering of alternatives
V = {1: V1,
     2: V2,
     3: V3}

# Associate the availability conditions with the alternatives
av = {1: TRAIN_AV_SP,
      2: SM_AV,
      3: CAR_AV_SP}

# Conditional to B_TIME_RND, we have a logit model (called the kernel)
prob = models.logit(V, av, CHOICE)

# We integrate over B_TIME_RND using Monte-Carlo
logprob = log(MonteCarlo(prob))

# Define level of verbosity
logger = msg.bioMessage()
#logger.setSilent()
#logger.setWarning()
logger.setGeneral()
#logger.setDetailed()

# Create the Biogeme object
biogeme = bio.BIOGEME(database, logprob, numberOfDraws=1000)

algos = {'CFSQP                   ': None,
         'scipy                   ': opt.scipy,
         'Line search             ': opt.newtonLineSearchForBiogeme,
         'Trust region (dogleg)   ': opt.newtonTrustRegionForBiogeme,
         'Trust region (cg)       ': opt.newtonTrustRegionForBiogeme,
         'LS-BFGS                 ': opt.bfgsLineSearchForBiogeme,
         'TR-BFGS                 ': opt.bfgsTrustRegionForBiogeme,
         'Simple bounds Newton fCG': opt.simpleBoundsNewtonAlgorithmForBiogeme,
         'Simple bounds BFGS fCG  ': opt.simpleBoundsNewtonAlgorithmForBiogeme,
         'Simple bounds hybrid fCG': opt.simpleBoundsNewtonAlgorithmForBiogeme,
         'Simple bounds Newton iCG': opt.simpleBoundsNewtonAlgorithmForBiogeme,
         'Simple bounds BFGS iCG  ': opt.simpleBoundsNewtonAlgorithmForBiogeme,
         'Simple bounds hybrid iCG': opt.simpleBoundsNewtonAlgorithmForBiogeme,
}

algos = {'Simple bounds Newton iCG': opt.simpleBoundsNewtonAlgorithmForBiogeme,
         'Simple bounds BFGS iCG  ': opt.simpleBoundsNewtonAlgorithmForBiogeme,
         'Simple bounds hybrid iCG': opt.simpleBoundsNewtonAlgorithmForBiogeme}
algoParameters = {'Trust region (dogleg)   ': {'dogleg':True},
                  'Trust region (cg)       ': {'dogleg':False},
                  'Simple bounds Newton fCG': {'proportionAnalyticalHessian': 1.0,
                                               'infeasibleConjugateGradient': False},
                  'Simple bounds BFGS fCG  ': {'proportionAnalyticalHessian': 0.0,
                                               'infeasibleConjugateGradient': False},
                  'Simple bounds hybrid fCG': {'proportionAnalyticalHessian': 0.5,
                                               'infeasibleConjugateGradient': False},
                  'Simple bounds Newton iCG': {'proportionAnalyticalHessian': 1.0,
                                               'infeasibleConjugateGradient': True},
                  'Simple bounds BFGS iCG  ': {'proportionAnalyticalHessian': 0.0,
                                               'infeasibleConjugateGradient': True},
                  'Simple bounds hybrid iCG': {'proportionAnalyticalHessian': 0.5,
                                               'infeasibleConjugateGradient': True}}

results = {}
msg = ''
for name, algo in algos.items():
    biogeme.modelName = f'05normalMixture_allAlgos_{name}'.strip()
    p = algoParameters.get(name)
    results[name] = biogeme.estimate(algorithm=algo, algoParameters=p)
    g = results[name].data.g
    msg += (f'{name}\t{results[name].data.logLike:.2f}\t'
            f'{results[name].data.gradientNorm:.2g}\t'
            f'{results[name].data.optimizationMessages["Optimization time"]}'
            f'\t{results[name].data.optimizationMessages["Cause of termination"]}\n')

print("Algorithm\t\tloglike\t\tnormg\ttime\t\tdiagnostic")
print("+++++++++\t\t+++++++\t\t+++++\t++++\t\t++++++++++")
print(msg)

"""
Here are the results. Note that the draws are identical for all runs. Still, the algorithms 
may converge to different solutions. Some algorithms obtain a solution with 
B_TIME_S = 1.66 (LL = -5214.34), 
and some obtain a solution with 
B_TIME_S = -1.64 (LL = -5217.076). 
Both are local optima of the likelihood function. As the draws are not exactly symmetric, 
these solutions have different values for the objective functions. If the number of draws is
increased, the two local solutions will (asymptotically) become identical. 

CFSQP                	-5214.34	0.00018	0:10:43.594313	b'Normal termination. Obj: 6.05545e-06 Const: 6.05545e-06'
scipy                	-5214.34	0.0003	0:02:39.790707	b'CONVERGENCE: NORM_OF_PROJECTED_GRADIENT_<=_PGTOL'
Line search          	-5217.08	0.0032	0:08:36.067822	Relative gradient = 7.268074670231605e-07 <= 6.06273418136464e-06
Trust region (dogleg)	-5217.08	0.006	0:02:27.189087	Relative gradient = 1.0041613389547025e-06 <= 6.06273418136464e-06
Trust region (cg)    	-5217.08	0.0072	0:03:09.579132	Relative gradient = 1.5515597679655953e-06 <= 6.06273418136464e-06
LS-BFGS              	-5214.34	0.017	0:09:30.871396	Relative gradient = 2.9271095714001536e-06 <= 6.06273418136464e-06
TR-BFGS              	-5214.34	0.019	0:09:29.817330	Relative gradient = 3.1559171978073267e-06 <= 6.06273418136464e-06
Simple bounds Newton 	-5214.34	0.029	0:03:05.095508	Relative gradient = 5.814388473410812e-06 <= 6.06273418136464e-06
Simple bounds BFGS   	-5214.34	0.029	0:03:08.572039	Relative gradient = 5.814388473410812e-06 <= 6.06273418136464e-06
Simple bounds hybrid 	-5214.34	0.029	0:03:02.268156	Relative gradient = 5.814388473410812e-06 <= 6.06273418136464e-06
"""
