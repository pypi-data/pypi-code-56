"""Package ItemResponseCalc implements Bayesian analysis of
subjective responses to items in a questionnaire,
using Item Response Theory (IRT) applied with
the Graded Response Model (Samejima, 1997; Fox, 2010).

This package is only intended for the analysis of data with ORDINAL responses,
e.g., the IOI-HA questionnaire for users' satisfaction with their hearing aids.

The IRT Graded Response Model treats subjects' responses
as determined by the outcome of a latent individual trait variable,
i.e., similar to the latent internal "sensation"
variable assumed to determine responses in psycho-physical experiments.
This package uses a logistic distribution for the latent variables.

Each questionnaire item corresponds to exactly ONE individual trait variable,
but each trait variable may determine the subject's responses to several items.

Therefore, for a questionnaire with I separate items,
the model can learn D <= I trait variables, based on the observed responses.
The model learning procedure automatically determines how many
different trait variables are needed to 'explain' the recorded data.

NOTE: In most modules of this package,
the ordinal response to the i-th item is encoded as
an integer in {0, 1,..., L_i-1},
where L_i = the number of ordinal response levels for the i-th item.
Any value outside this range is interpreted as a missing response.

However, in the input data files,
the recorded responses are usually encoded as integers in {1, 2,..., L_i},
with missing values encoded as zero.
This notation is used in module item_response_data.
and in some results presentations where response levels are identified.


*** Usage

Copy the template script `run_irt.py` to your working directory, rename it, and
edit the copy as suggested in the template, to specify
    - your experimental layout,
    - your input data file(s),
    - a directory where all output result files will be stored.

*** Main Modules

item_response_data:
    Interface to one or several data sets containing individual responses
    from respondents recruited from one or several different population(s).
    See this module for information about input files and data formats.

item_response_model:
    The core of the Bayesian IRT model adapted to all observed data.

item_scale:
    Classes representing the item-specific model parameters,
    defining the connection between traits to ordinal responses, for each item.

item_respondents:
    Classes representing individual- and population-specific models
    defining trait distributions for each individual and each population.

ir_display:
    Functions and classes to display all analysis results as figures and tables.
    
table_reader:
    Defines class Table for input data in several accepted file formats.
    The present version can read tabulated data from sources of type
    xlsx, csv, sql, sqlite3.

Analysis results are saved as figures and tables in the selected result directory.
After running an analysis, the logging output briefly explains
the analysis results presented in figures and tables.

*** References
Arne Leijon and Harvey Dillon and Louise Hickson
and Martin Kinkel and Sophia E Kramer and Peter Nordquist (2020):
    Analysis of Data from the International Outcome Inventory for Hearing Aids (IOI-HA)
    using Bayesian Item Response Theory.
    Manuscript in preparation.

J.-P. Fox (2010). *Bayesian Item Response Modeling: Theory and Applications*.
    Statistics for Social and Behavioral Sciences. Springer.
G. N. Masters (1982). A Rasch model for partial credit scoring.
    *Psychometrika*, 47(2):149–174.
F. Samejima (1997). Graded response model.
    In W. J. v. D. Linden and R. K. Hambleton, eds.,
    *Handbook of Modern Item Response Theory*, p. 85–100. Springer, New York.


*** Version History

2019-08-24, first functional version with automatic selection of trait dimensionality.
2020-06-08, first version uploaded to PyPi, tested with several IOI-HA data sets.
"""

__name__ = 'ItemResponseCalc'
__version__ = '0.5.0'
__all__ = ['__version__', 'run_irt', 'show_irt']


