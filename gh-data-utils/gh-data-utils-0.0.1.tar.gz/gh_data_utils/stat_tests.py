import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.anova import AnovaRM

def _descriptive_stats(data, description, dimensions):

    if description == None:
        description = 'Statistical Tests for Group Comparisons'
    print(f"{description}\n\n")

    for dim in dimensions:
        dim_mean = data[dim].mean().round(3)
        print(f"Mean for group {dim}: {dim_mean}")


def _ind_anova(data, dimensions):
    test_groups = []

    for dim in dimensions:
        dim_mean = data[dim].mean().round(3)
        test_groups.append(data[data[dim].notnull()][dim].tolist())

    results = stats.f_oneway(*test_groups)
    t = results.statistic.round(3)
    p = results.pvalue.round(3)

    w, wp = stats.kruskal(*test_groups)

    print(f"\n\nOne-Way ANOVA Results: \n\nt = {t}\np = {p}")
    print(f"\n\nKruskal Test Results: \n\nw = {w}\np = {wp}")


def _rep_anova(data, dimensions, groups, index):
    test_groups = []

    for dim in dimensions:
        dim_mean = data[dim].mean().round(3)
        test_groups.append(data[data[dim].notnull()][dim].tolist())

    anova_df = pd.melt(data, id_vars=index, value_vars=dimensions)

    aovrm = AnovaRM(
        anova_df, depvar = 'value',
        within=[groups], subject=index)
    results = aovrm.fit()

    x, p = stats.friedmanchisquare(*test_groups)
    print(f"\n\n{results}")
    print(f"\n\nFriedman Chi-Square Test Results: \n\nx = {x}\np = {p}")


def _ind_ttest(data, dimensions):
    results = stats.ttest_ind(data[dimensions[0]], data[dimensions[1]])
    t = results.statistic.round(3)
    p = results.pvalue.round(3)

    w, wp = stats.mannwhitneyu(data[dimensions[0]], data[dimensions[1]])

    print(f"\n\nIndependent Samples T-Test Results: \n\nt = {t}\np = {p}")
    print(f"\n\nMann-Whitney Test Results: \n\nw = {w}\np = {wp}")


def _rep_ttest(data, dimensions):
    results = stats.ttest_rel(data[dimensions[0]], data[dimensions[1]])
    t = results.statistic.round(3)
    p = results.pvalue.round(3)

    w, wp = stats.wilcoxon(data[dimensions[0]], data[dimensions[1]])

    print(f"\n\nRepeated Measures T-Test Results: \n\nt = {t}\np = {p}")
    print(f"\n\nWilcoxon Signed Rank Test Results: \n\nw = {w}\np = {wp}")


def _compare_two_groups(data, dimensions, description, comparison = 'ind'):

    _descriptive_stats(data = data, dimensions = dimensions, description = description)

    test_data = data.dropna()

    if comparison == 'ind':
        _ind_ttest(data = test_data, dimensions = dimensions)
    if comparison == 'rep':
        _rep_ttest(data = test_data, dimensions = dimensions)


def _compare_multiple_groups(
        data, dimensions, description, groups, index, comparison = 'ind'):

    test_data = data.dropna()

    _descriptive_stats(data = test_data, dimensions = dimensions, description = description)

    if comparison == 'ind':
        _ind_anova(data = test_data, dimensions = dimensions)
    if comparison == 'rep':
        _rep_anova(data = test_data, dimensions = dimensions, groups = groups, index = index)


def run_stat_test(
        data, groups, data_col, index, dimensions=None,
        comparison='ind', description=None):
    """
    Conduct a parametric and non-parametric statistical test for two or more groups. The type of test based on number of groups is determined automatically.

    Parameters
    ----------
    data: DataFrame, required
        Dataframe used to generate charts. Data should be in a tidy format (see: https://vita.had.co.nz/papers/tidy-data.pdf).
    groups: column, required
        The name of the column in data by which you are grouping results.
    data_col: column, required
      The name of the column in DataFrame with continuous data to compare by group.
    index: column, required
        The Dataframe column to use as an index when shaping data for a specific test. This should be your unit of comparison (i.e., user, day, event, etc).
    dimensions: list, optional, default None
        A subset of groups to use in statistical comparisons. If this isn't specified, dimensions for statistical tests will be inferred from a list of distinct values in "groups"
    comparison: {'ind', 'rep'}, default 'ind'
        The type of experimental design (independent or repeated measures).
    description: string, optional, default = ''
        A description of the statistical test to include at the top of the summary of results. Defaults to None, and uses the standard output from each test.
    """
    
    if comparison not in ('ind', 'rep'):
        raise ValueError('Comparison should be ind for independent samples or rep for repeated measures.')

    data_pivot = pd.pivot_table(
        data, index=index, columns=groups,
        values=data_col)
    data_pivot.reset_index(inplace=True)

    if dimensions == None:
      dimensions = [x for x in data_pivot.columns if index not in x]

    if len(dimensions) < 2:
        raise ValueError('Group comparisons require at least two groups.')

    if len(dimensions) == 2:
        _compare_two_groups(
            data = data_pivot, dimensions = dimensions,
            description = description, comparison = comparison)

    elif len(dimensions) > 2:
        _compare_multiple_groups(
            data = data_pivot, dimensions = dimensions, index = index,
            description = description, groups = groups, comparison = comparison)
