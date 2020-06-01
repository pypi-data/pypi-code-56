import multiprocessing
import random
from typing import List, Union, Tuple, Dict
import pandas as pd
import logging

from deap import base, tools, creator
from deap.algorithms import varOr
from sklearn.metrics import make_scorer
from sklearn.model_selection import train_test_split, cross_val_score
from atgfe.single_operation_functions import *
import warnings
from scipy.interpolate import interp1d
from functools import partial
from sympy import sympify
import os
from time import time

warnings.filterwarnings('ignore')

logging_format = "%(asctime)s:%(levelname)s: %(message)s "
logging.basicConfig(filename='geneticFeatureEngineerWithBraces.log', level=logging.DEBUG, filemode='w',
                    format=logging_format)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logging_formatter = logging.Formatter(logging_format)
logger = logging.getLogger('GeneticFeatureEngineerWithBraces')
ch.setFormatter(logging_formatter)
logger.addHandler(ch)


class GeneticFeatureEngineer:
    # single_feature_operations: List[str] = ['None', '@np_log({})', '@np_log_10({})', '@np_log_1p({})',
    #                                         '@np_min({})', '@np_exp({})', '@np_mean({})', '@np_std({})',
    #                                         '@np_median({})', '@np_max({})', '@squared({})', '@cube({})',
    #                                         '@np_cos({})', '@np_sin({})', '@np_tan({})', '@np_arcsin({})',
    #                                         '@np_arccos({})', '@np_arctan({})', '@np_sinh({})', '@np_cosh({})',
    #                                         '@np_tanh({})']
    enabled_single_feature_operations: List[str] = ['None', '@np_log({})', '@np_log_10({})',
                                                    '@np_exp({})', '@squared({})', '@cube({})']
    aggregation_operations: List[str] = ['None', 'min', 'max', 'mean', 'median', 'std', 'count']
    # aggregation_operations: List[str] = ['min', 'max', 'mean', 'median', 'std', 'count']
    single_feature_operations: List[str] = ['None']
    features_left_brace: List[str] = ['None', '(']
    features_right_brace: List[str] = ['None', ')']
    features_interaction_operations: List[Union[str, Any]] = ['None', '*', '+', '-', '/']
    best_solution: List[int] = None
    best_score: float = None
    grouping_length = 7
    max_category_value = 1000

    def __init__(self, model, x_train: pd.DataFrame, y_train: pd.DataFrame, numerical_features: List[str],
                 number_of_candidate_features: int,
                 number_of_interacting_features: int,
                 evaluation_metric: Callable[..., Any], minimize_metric: bool = True,
                 categorical_features: List[str] = None,
                 enable_grouping: bool = False,
                 sampling_size: int = None,
                 cv: int = 10,
                 fit_wo_original_columns: bool = False,
                 enable_feature_transformation_operations: bool = False,
                 enable_weights: bool = False,
                 weights_number_of_decimal_places: int = 2,
                 enable_bias: bool = False,
                 max_bias: float = 100.0,
                 shuffle_training_data_every_generation: bool = False,
                 cross_validation_in_objective_func: bool = False,
                 objective_func_cv: int = 3,
                 n_jobs: int = 1,
                 verbose: bool = True):

        if enable_grouping and categorical_features is None:
            raise AttributeError(
                ''' Grouping requires categorical_features.
                 Please pass the categorical_features when creating GeneticFeatureEngineer object.''')

        if not enable_grouping and categorical_features is not None:
            logging.info('Enable grouping in order to use the categorical_features in the feature engineering')

        self.model = model
        self.enable_feature_transformation_operations = enable_feature_transformation_operations
        if self.enable_feature_transformation_operations:
            self.single_feature_operations = self.enabled_single_feature_operations
        if sampling_size is None:
            self.x_train = x_train.copy()
            self.y_train = y_train.copy()
        elif sampling_size > len(x_train):
            self.x_train = x_train.sample(n=sampling_size, random_state=77, replace=True)
            self.y_train = y_train.ix[self.x_train.index.values]
        else:
            self.x_train = x_train.sample(n=sampling_size, random_state=77)
            self.y_train = y_train.ix[self.x_train.index.values]

        self.numerical_features = numerical_features
        self.categorical_features = categorical_features
        self.enable_grouping = enable_grouping
        self.number_of_candidate_features = number_of_candidate_features
        self.number_of_interacting_features = number_of_interacting_features
        self.enable_weights = enable_weights
        self.enable_bias = enable_bias
        self.max_bias = max_bias
        self.weights_number_of_decimal_places = weights_number_of_decimal_places
        self.single_candidate_feature_solution_length = 3 * self.number_of_interacting_features - 1
        # for braces add 2 cells to the solution
        self.single_candidate_feature_solution_length += 2 * self.number_of_interacting_features
        # for grouping
        if self.enable_grouping:
            self.single_candidate_feature_solution_length += self.grouping_length
        # for features' weights
        if self.enable_weights:
            self.single_candidate_feature_solution_length += self.number_of_interacting_features
            if self.enable_grouping:
                self.single_candidate_feature_solution_length += 1
        if self.enable_bias:
            self.single_candidate_feature_solution_length += 1
        self.ga_solution_length = self.single_candidate_feature_solution_length * self.number_of_candidate_features
        self.evaluation_metric = evaluation_metric
        self.minimize_metric = minimize_metric
        self.cv = cv
        self.fit_wo_original_columns = fit_wo_original_columns
        self.shuffle_training_data_every_generation = shuffle_training_data_every_generation
        self.cross_validation_in_objective_func = cross_validation_in_objective_func
        self.objective_func_cv = objective_func_cv
        self.n_jobs = n_jobs
        self.verbose = verbose

        if self.verbose:
            logger.info('New Engineer created with the following parameters:')
            logger.info(
                '\nModel type: {}\nNumerical Features: {}\nNumber of candidate features: {}\nNumber of interacting features: {}\n'
                'Evaluation Metric: {}\nMinimize metric is {}'.format(model.__class__, numerical_features,
                                                                      number_of_candidate_features,
                                                                      number_of_interacting_features,
                                                                      evaluation_metric.__name__,
                                                                      minimize_metric))

    def _chunks(self, list, chunk_size):
        for i in range(0, len(list), chunk_size):
            yield list[i:i + chunk_size]

    def _create_group_expression(self, grouping_solution) -> Dict[str, Any]:
        grouping_expression = {
            'left_brace_value': self.features_left_brace[grouping_solution[0]],
            'grouping_weight': str(round(grouping_solution[1], self.weights_number_of_decimal_places)),
            'categorical_feature': self.categorical_features[grouping_solution[2]],
            'selected_category': grouping_solution[3],
            'aggregation_operation': self.aggregation_operations[grouping_solution[4]],
            'numerical_feature': self.numerical_features[grouping_solution[5]],
            'interaction_operator': self.features_interaction_operations[grouping_solution[6]]
        }

        return grouping_expression

    def _generate_expressions_to_evaluate(self, individual):
        generated_feature_index = 1
        order_of_operations = ['feature_left_brace', 'feature_operation',
                               'feature', 'feature_right_brace',
                               'features_interaction_operator']
        order_of_operations_with_weights = ['feature_left_brace', 'feature_operation',
                                            'feature_weight', 'feature',
                                            'feature_right_brace', 'features_interaction_operator']
        candidate_features_solutions = list(self._chunks(individual, self.single_candidate_feature_solution_length))
        expressions_to_evaluate = []
        groups_to_create: List[Dict[str, Any]] = []
        generated_columns = []
        length_of_operations = len(order_of_operations_with_weights) if self.enable_weights else len(
            order_of_operations)
        for candidate_feature_solution in candidate_features_solutions:
            eval_expression_list = []
            i = 0
            current_operation_index = 0

            if self.enable_grouping:
                grouping_solution = candidate_feature_solution[0:self.grouping_length].copy()
                candidate_feature_solution = candidate_feature_solution[self.grouping_length:].copy()
                group_expression = self._create_group_expression(grouping_solution)
                groups_to_create.append(group_expression)
                if group_expression['interaction_operator'] == 'None':
                    i = len(candidate_feature_solution)

            if self.enable_bias:
                bias = candidate_feature_solution[-1]
                candidate_feature_solution = candidate_feature_solution[:-1].copy()
                eval_expression_list.append(str(bias) + ' + ')

            while i < len(candidate_feature_solution):

                if self.enable_weights:
                    current_operation = order_of_operations_with_weights[current_operation_index]
                    current_operation_index, i = self._evaluate_with_weights(candidate_feature_solution,
                                                                             current_operation,
                                                                             current_operation_index,
                                                                             eval_expression_list, i,
                                                                             order_of_operations_with_weights)
                else:
                    current_operation = order_of_operations[current_operation_index]
                    current_operation_index, i = self._evaluate(candidate_feature_solution, current_operation,
                                                                current_operation_index, eval_expression_list, i,
                                                                order_of_operations)

                if current_operation_index == length_of_operations:
                    current_operation_index = 0

            generated_feature_index += 1
            eval_expression = ' '.join(eval_expression_list)
            generated_column = ''.join(eval_expression_list)

            if '(' in generated_column and ')' in generated_column:
                if generated_column.index('(') == 0 and generated_column.index(')') == len(generated_column) - 1 \
                        and generated_column.count('(') == 1 and generated_column.count(')') == 1:
                    generated_column = generated_column[1:len(generated_column) - 1]
                    eval_expression = eval_expression[1:len(eval_expression) - 1]

            generated_column = self._balance_braces(generated_column)
            eval_expression = self._balance_braces(eval_expression)

            generated_columns.append(generated_column)
            expressions_to_evaluate.append(eval_expression)

        return generated_columns, groups_to_create, expressions_to_evaluate

    def _evaluate_with_weights(self, candidate_feature_solution, current_operation, current_operation_index,
                               eval_expression_list, i,
                               order_of_operations_with_weights):
        if current_operation == order_of_operations_with_weights[0]:
            feature_left_brace = self.features_left_brace[candidate_feature_solution[i]]
            if feature_left_brace != 'None':
                eval_expression_list.append(feature_left_brace)
            i += 1
            current_operation_index += 1
        elif current_operation == order_of_operations_with_weights[1]:
            feature_operation = self.single_feature_operations[candidate_feature_solution[i]]
            feature_weight = str(round(candidate_feature_solution[i + 1], self.weights_number_of_decimal_places))
            feature = self.numerical_features[candidate_feature_solution[i + 2]]

            if feature_operation == 'None':
                feature_with_weight = feature_weight + '*' + feature
                eval_expression_list.append(feature_with_weight)
            else:
                eval_expression_list.append(feature_weight + '*' + feature_operation.format(feature))
            i += 3
            current_operation_index += 3
        elif current_operation == order_of_operations_with_weights[4]:
            feature_right_brace = self.features_right_brace[candidate_feature_solution[i]]
            if feature_right_brace != 'None':
                eval_expression_list.append(feature_right_brace)
            i += 1
            current_operation_index += 1
        else:
            interaction_operation = self.features_interaction_operations[candidate_feature_solution[i]]

            if interaction_operation == 'None':
                i = len(candidate_feature_solution)
            else:
                eval_expression_list.append(interaction_operation)
                current_operation_index += 1
            i += 1
        return current_operation_index, i

    def _evaluate(self, candidate_feature_solution, current_operation, current_operation_index, eval_expression_list, i,
                  order_of_operations):
        if current_operation == order_of_operations[0]:
            feature_left_brace = self.features_left_brace[candidate_feature_solution[i]]
            if feature_left_brace != 'None':
                eval_expression_list.append(feature_left_brace)
            i += 1
            current_operation_index += 1
        elif current_operation == order_of_operations[1]:
            feature_operation = self.single_feature_operations[candidate_feature_solution[i]]
            feature = self.numerical_features[candidate_feature_solution[i + 1]]

            if feature_operation == 'None':
                eval_expression_list.append(feature)
            else:
                eval_expression_list.append(feature_operation.format(feature))
            i += 2
            current_operation_index += 2
        elif current_operation == order_of_operations[3]:
            feature_right_brace = self.features_right_brace[candidate_feature_solution[i]]
            if feature_right_brace != 'None':
                eval_expression_list.append(feature_right_brace)
            i += 1
            current_operation_index += 1
        else:
            interaction_operation = self.features_interaction_operations[candidate_feature_solution[i]]

            if interaction_operation == 'None':
                i = len(candidate_feature_solution)
            else:
                eval_expression_list.append(interaction_operation)
                current_operation_index += 1
            i += 1
        return current_operation_index, i

    def _balance_braces(self, expression):
        left_brace_count = expression.count('(')
        right_brace_count = expression.count(')')
        braces_diff = abs(left_brace_count - right_brace_count)
        if braces_diff != 0:
            if left_brace_count > right_brace_count:
                expression += ')' * braces_diff
            else:
                expression = '(' * braces_diff + expression
        return expression

    def _add_groupby_features_and_update_expressions(self, new_df, generated_columns, groups_to_create,
                                                     expressions_to_evaluate):

        columns_to_drop = []
        new_generated_columns = []
        new_expressions_to_evaluate = []
        i = 0
        while i < len(generated_columns):
            generated_column = generated_columns[i]
            group_to_create = groups_to_create[i]
            expression_to_evaluate = expressions_to_evaluate[i]

            if group_to_create['aggregation_operation'] == 'None':
                new_generated_columns.append(generated_column)
                new_expressions_to_evaluate.append(expression_to_evaluate)
                i += 1
            else:
                left_brace = group_to_create['left_brace_value']
                grouping_weight = group_to_create['grouping_weight']
                categorical_feature = group_to_create['categorical_feature']
                selected_category_value = group_to_create['selected_category']
                aggregation_operation = group_to_create['aggregation_operation']
                numerical_feature = group_to_create['numerical_feature']
                interaction_operator = group_to_create['interaction_operator']
                df_groupby = new_df.groupby(categorical_feature).agg(aggregation_operation)

                if selected_category_value >= 500:
                    category_mapper = interp1d([500, self.max_category_value], [0, len(df_groupby.index.tolist()) - 1])
                    selected_category_index = int(round(float(category_mapper(selected_category_value))))
                    selected_category = df_groupby.index.tolist()[selected_category_index]
                    new_column_name = 'groupBy' + categorical_feature.capitalize() + '' + str(
                        selected_category).capitalize() + 'Take' + aggregation_operation.capitalize() + 'Of' + str(
                        numerical_feature).capitalize()
                    new_df[new_column_name] = df_groupby.loc[selected_category, numerical_feature]
                else:
                    new_column_name = 'groupBy' + categorical_feature.capitalize() + 'Take' + aggregation_operation.capitalize() + 'Of' + str(
                        numerical_feature).capitalize()
                    new_df[new_column_name] = new_df.apply(
                        lambda row: df_groupby.loc[row[categorical_feature], numerical_feature], axis=1)

                if expression_to_evaluate != '':
                    columns_to_drop.append(new_column_name)

                if interaction_operator != 'None':
                    new_generated_column = new_column_name + interaction_operator + generated_column
                    new_expression_to_evaluate = new_column_name + interaction_operator + expression_to_evaluate
                    if self.enable_weights:
                        new_generated_column = grouping_weight + '*' + new_generated_column
                        new_expression_to_evaluate = grouping_weight + '*' + new_expression_to_evaluate
                    if left_brace != 'None':
                        new_generated_column = self._balance_braces(left_brace + new_generated_column)
                        new_expression_to_evaluate = self._balance_braces(left_brace + new_expression_to_evaluate)
                    new_generated_columns.append(new_generated_column)
                    new_expressions_to_evaluate.append(new_expression_to_evaluate)
            i += 1
        return new_df, columns_to_drop, new_generated_columns, new_expressions_to_evaluate

    def _create_data_frame_with_candidate_features(self, data_frame: pd.DataFrame, individual) -> Tuple[Any, List[str]]:
        generated_columns, groups_to_create, expressions_to_evaluate = self._generate_expressions_to_evaluate(
            individual)
        new_df: pd.DataFrame = data_frame.copy()

        if self.enable_grouping:
            new_df, groupBy_columns_to_drop, generated_columns, expressions_to_evaluate = self._add_groupby_features_and_update_expressions(
                new_df, generated_columns, groups_to_create, expressions_to_evaluate)
            new_df = self._evaluate_expression(expressions_to_evaluate, generated_columns, new_df)
            new_df = new_df.drop(columns=groupBy_columns_to_drop, axis=1)

        else:
            new_df = self._evaluate_expression(expressions_to_evaluate, generated_columns, new_df)

        new_df = new_df.replace([np.inf, -np.inf], np.nan).dropna(axis=1, how="any")

        new_naming_dict = self._rename_new_columns(new_df)

        new_df = new_df.rename(new_naming_dict, axis=1)

        return new_df, expressions_to_evaluate

    def _evaluate_expression(self, expressions_to_evaluate, generated_columns, new_df):
        for generated_column, expression_to_evaluate in zip(generated_columns, expressions_to_evaluate):
            if len(expression_to_evaluate) > 0:
                try:
                    new_df[generated_column] = new_df.eval(expression_to_evaluate)
                except TypeError:
                    new_df[generated_column] = new_df.eval(expression_to_evaluate, engine='python')
        return new_df

    def _objective_function(self, individual, gen=8) -> Union[Tuple[Any], Tuple[np.float64]]:
        try:
            new_x_train, _ = self._create_data_frame_with_candidate_features(self.x_train, individual)

            if len(new_x_train.columns) == 0:
                if self.minimize_metric:
                    return np.float_(1e10),
                else:
                    return np.float_(-1e10),

            if self.fit_wo_original_columns:
                new_x_train = new_x_train.drop(self.numerical_features, axis=1)

            new_y_train = self.y_train.loc[:].copy()

            if self.cross_validation_in_objective_func:
                evaluation_metric_scorer = make_scorer(self.evaluation_metric, greater_is_better=True)
                scores = cross_val_score(estimator=self.model, X=new_x_train, y=new_y_train, cv=self.objective_func_cv,
                                         scoring=evaluation_metric_scorer, n_jobs=-1)
                mean_score = scores.mean()
                return mean_score,
            else:
                opt_x_train, opt_x_test, opt_y_train, opt_y_test = train_test_split(new_x_train, new_y_train,
                                                                                    test_size=0.3, random_state=gen)

                self.model.fit(opt_x_train, opt_y_train)
                y_pred = self.model.predict(opt_x_test)
                score = self.evaluation_metric(opt_y_test, y_pred)
                return score,
        except Exception as e:
            # logger.info(e)
            if self.minimize_metric:
                if 'EOF in multi-line statement' in str(e):
                    return np.float_(1e13),
                elif 'list' in str(e):
                    return np.float_(1e12),
                elif 'syntax' in str(e):
                    return np.float_(1e11),
                else:
                    return np.float_(1e9),
            else:
                if 'EOF in multi-line statement' in str(e):
                    return np.float_(-1e13),
                elif 'list' in str(e):
                    return np.float_(-1e12),
                elif 'syntax' in str(e):
                    return np.float_(-1e11),
                else:
                    return np.float_(-1e9),

    def _cross_validation_function(self, individual, generation) -> Tuple[Any, Any]:
        try:
            new_x_train, _ = self._create_data_frame_with_candidate_features(self.x_train, individual)

            if self.fit_wo_original_columns:
                new_x_train = new_x_train.drop(self.numerical_features, axis=1)

            new_y_train = self.y_train.loc[:].copy()

            evaluation_metric_scorer = make_scorer(self.evaluation_metric, greater_is_better=True)
            scores = cross_val_score(estimator=self.model, X=new_x_train, y=new_y_train, cv=self.cv,
                                     scoring=evaluation_metric_scorer, n_jobs=-1)
            mean_score = scores.mean()

            return mean_score, new_x_train.columns.tolist()
        except Exception as e:
            logger.exception(e)
            if self.minimize_metric:
                if 'EOF in multi-line statement' in str(e):
                    return np.float_(1e11), []
                else:
                    return np.float_(1e9), []
            else:
                if 'EOF in multi-line statement' in str(e):
                    return np.float_(-1e11), []
                else:
                    return np.float_(-1e9), []

    def _create_optimization_toolbox(self):
        toolbox = base.Toolbox()

        list_of_grouping_attributes = ['grouping_feature_left_brace',
                                       'grouping_weight',
                                       'grouping_feature_categorical_feature',
                                       'grouping_feature_selected_category',
                                       'grouping_feature_aggregation_operation',
                                       'grouping_feature_numerical_feature',
                                       'grouping_feature_interaction_operator']

        list_of_attributes_in_order = ['feature_{}_left_brace',
                                       'feature_{}_operation',
                                       'feature_{}',
                                       'feature_{}_right_brace',
                                       'feature_{}_interaction_operator']

        if self.enable_weights:
            list_of_attributes_in_order = ['feature_{}_left_brace',
                                           'feature_{}_operation',
                                           'feature_{}_weight',
                                           'feature_{}',
                                           'feature_{}_right_brace',
                                           'feature_{}_interaction_operator']

        list_of_attributes_to_register = []
        list_of_attributes_registered = []
        solution_index_offset = 0
        if self.enable_grouping:
            solution_index_offset = self.grouping_length
            self.register_grouping_attributes(list_of_attributes_registered, list_of_grouping_attributes, toolbox)

        attribute_index = 0
        feature_index = 1

        single_candidate_feature_solution_length = self.single_candidate_feature_solution_length

        if self.enable_bias:
            single_candidate_feature_solution_length -= 1
        for i in range(solution_index_offset, single_candidate_feature_solution_length):
            attribute_to_register = list_of_attributes_in_order[attribute_index].format(feature_index)
            attribute_index += 1

            list_of_attributes_to_register.append(attribute_to_register)

            if attribute_index == len(list_of_attributes_in_order):
                attribute_index = 0
                feature_index += 1

        for attribute_to_register in list_of_attributes_to_register:

            if '_operation' in attribute_to_register:
                toolbox.register(attribute_to_register, random.randint, 0, len(self.single_feature_operations) - 1)
            elif '_interaction_operator' in attribute_to_register:
                toolbox.register(attribute_to_register, random.randint, 0,
                                 len(self.features_interaction_operations) - 1)
            elif '_left_brace' in attribute_to_register:
                toolbox.register(attribute_to_register, random.randint, 0,
                                 len(self.features_left_brace) - 1)
            elif '_right_brace' in attribute_to_register:
                toolbox.register(attribute_to_register, random.randint, 0,
                                 len(self.features_right_brace) - 1)
            elif '_weight' in attribute_to_register:
                toolbox.register(attribute_to_register, random.uniform, 0, 1)
            else:
                toolbox.register(attribute_to_register, random.randint, 0, len(self.numerical_features) - 1)

            list_of_attributes_registered.append(getattr(toolbox, attribute_to_register))

        if self.enable_bias:
            attribute_to_register = 'expression_bias'
            toolbox.register(attribute_to_register, random.uniform, -1 * self.max_bias, self.max_bias)
            list_of_attributes_registered.append(getattr(toolbox, attribute_to_register))

        toolbox.register("individual", tools.initCycle, creator.Individual, tuple(list_of_attributes_registered),
                         n=self.number_of_candidate_features)
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)

        if self.shuffle_training_data_every_generation:
            toolbox.register("evaluate", self._objective_function, gen=8)
        else:
            toolbox.register("evaluate", self._objective_function)
        toolbox.register("cross_validation", self._cross_validation_function)
        toolbox.register("mate", tools.cxTwoPoints)
        toolbox.register("mutate", tools.mutFlipBit, indpb=0.08)
        toolbox.register("select", tools.selTournament, tournsize=20)

        if self.n_jobs > 1:
            number_of_cpus = self.n_jobs

            if self.n_jobs == -1:
                number_of_cpus = multiprocessing.cpu_count()

            pool = multiprocessing.Pool(processes=number_of_cpus)
            toolbox.register("map", pool.map)

        return toolbox

    def register_grouping_attributes(self, list_of_attributes_to_register, list_of_grouping_attributes, toolbox):
        for grouping_attribute in list_of_grouping_attributes:
            if '_left_brace' in grouping_attribute:
                toolbox.register(grouping_attribute, random.randint, 0,
                                 len(self.features_left_brace) - 1)
            elif '_categorical_feature' in grouping_attribute:
                toolbox.register(grouping_attribute, random.randint, 0,
                                 len(self.categorical_features) - 1)
            elif '_selected_category' in grouping_attribute:
                toolbox.register(grouping_attribute, random.randint, 0, self.max_category_value)
            elif '_aggregation_operation' in grouping_attribute:
                toolbox.register(grouping_attribute, random.randint, 0,
                                 len(self.aggregation_operations) - 1)
            elif '_interaction_operator' in grouping_attribute:
                toolbox.register(grouping_attribute, random.randint, 0,
                                 len(self.features_interaction_operations) - 1)
            elif '_weight' in grouping_attribute:
                toolbox.register(grouping_attribute, random.uniform, 0, 1)
            else:
                toolbox.register(grouping_attribute, random.randint, 0, len(self.numerical_features) - 1)

            list_of_attributes_to_register.append(getattr(toolbox, grouping_attribute))

    def fit(self, number_of_generations: int = 100, mu: int = 10, lambda_: int = 100,
            crossover_probability: float = 0.5,
            mutation_probability: float = 0.2, early_stopping_patience: int = 5, random_state: int = 77):

        os.environ['PYTHONHASHSEED'] = str(random_state)
        np.random.seed(random_state)
        random.seed(random_state)

        if self.minimize_metric:
            creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
            creator.create("Individual", list, fitness=creator.FitnessMin)
        else:
            creator.create("FitnessMax", base.Fitness, weights=(1.0,))
            creator.create("Individual", list, fitness=creator.FitnessMax)

        toolbox = self._create_optimization_toolbox()

        self.hof = tools.HallOfFame(1)

        stats_fit = tools.Statistics(lambda ind: ind.fitness.values)
        stats = tools.MultiStatistics(fitness=stats_fit)
        stats.register("avg", np.mean)
        stats.register("std", np.std)
        stats.register("min", np.min)
        stats.register("max", np.max)

        logbook = tools.Logbook()
        logbook.header = ['gen', 'nevals'] + (stats.fields if stats else [])

        CXPB, MUTPB = crossover_probability, mutation_probability
        MU, LAMBDA = mu, lambda_
        assert LAMBDA >= MU, "lambda must be greater or equal to mu."
        pop = toolbox.population(n=MU)

        best_validation_solution = None
        current_best_validation_solution = None
        best_validation_score = None
        current_best_validation_score = None
        best_validation_equality_counter = 0
        max_best_validation_equality_counter = early_stopping_patience

        if self.verbose:
            print("Start of evolution")

        invalid_ind = [ind for ind in pop if not ind.fitness.valid]

        if self.shuffle_training_data_every_generation:
            fitnesses = toolbox.map(partial(toolbox.evaluate, gen=0), invalid_ind)
        else:
            fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)

        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        if self.hof is not None:
            self.hof.update(pop)

        record = stats.compile(pop) if stats else {}
        logbook.record(gen=0,
                       time_in_seconds=np.nan,
                       nevals=len(invalid_ind),
                       gen_val_score=np.nan,
                       best_val_score=np.nan,
                       **record)
        if self.verbose:
            print(logbook.stream)

        # Begin the generational process
        for gen in range(1, number_of_generations + 1):
            gen_start = time()
            os.environ['PYTHONHASHSEED'] = str(random_state)
            np.random.seed(random_state)
            random.seed(random_state)
            # Vary the population
            offspring = varOr(pop, toolbox, LAMBDA, CXPB, MUTPB)

            # Evaluate the individuals with an invalid fitness
            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            if self.shuffle_training_data_every_generation:
                fitnesses = toolbox.map(partial(toolbox.evaluate, gen=gen), invalid_ind)
            else:
                fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit

            # Update the hall of fame with the generated individuals
            if self.hof is not None:
                self.hof.update(offspring)

            current_best_validation_solution = tools.selBest(pop, 1)[0]
            current_best_validation_score, all_columns = toolbox.cross_validation(current_best_validation_solution, gen)
            if best_validation_solution is not None:
                if (current_best_validation_score < best_validation_score and self.minimize_metric) or (
                        current_best_validation_score > best_validation_score and not self.minimize_metric):
                    best_validation_solution = current_best_validation_solution.copy()
                    best_validation_score = current_best_validation_score
                    best_validation_equality_counter = 0
                elif (current_best_validation_score >= best_validation_score and self.minimize_metric) or (
                        current_best_validation_score <= best_validation_score and not self.minimize_metric):
                    best_validation_equality_counter += 1

                if best_validation_equality_counter >= max_best_validation_equality_counter:
                    break
            else:
                best_validation_solution = current_best_validation_solution.copy()
                best_validation_score = current_best_validation_score

            # Select the next generation population
            pop[:] = toolbox.select(offspring, MU)

            gen_stop = time()
            # Append the current generation statistics to the logbook
            record = stats.compile(pop) if stats else {}
            logbook.record(gen=gen,
                           time_in_seconds=(gen_stop - gen_start),
                           nevals=len(invalid_ind),
                           gen_val_score=current_best_validation_score,
                           best_val_score=best_validation_score,
                           **record)
            if self.verbose:
                print(logbook.stream)

        if self.verbose:
            best_validation_score, all_columns = toolbox.cross_validation(best_validation_solution,
                                                                          generation=number_of_generations)
            print("-- End of (successful) evolution --")
            print(f"Best validation score: {best_validation_score}")
            print('All columns: {}'.format(all_columns))

        self.best_solution = best_validation_solution.copy()
        self.best_score = best_validation_score

    def transform(self, df: pd.DataFrame, solution=None):
        if solution:
            return self._create_data_frame_with_candidate_features(df, solution)[0]
        if self.best_solution is None:
            raise ValueError('You need to use the fit function first in order to find best solution.')
        return self._create_data_frame_with_candidate_features(df, self.best_solution)[0]

    def _rename_new_columns(self, new_df: pd.DataFrame):
        old_columns_names = new_df.columns.tolist()
        naming_dict = {}

        for old_columns_name in old_columns_names:
            new_name = old_columns_name
            new_name = new_name.replace('self.', '')
            new_name = new_name.replace('@', '')
            new_name = new_name.replace('np_', '')
            naming_dict[old_columns_name] = self._simplify_expression(new_name)

        return naming_dict

    def _simplify_expression(self, expression: str) -> str:
        return str(sympify(expression))

    def get_enabled_transformation_operations(self):
        transformation_operations = [operation.replace('@', '').replace('({})', '') for operation in
                                     self.single_feature_operations]
        return transformation_operations

    def add_transformation_operation(self, operation, function):
        if not self.enable_feature_transformation_operations:
            print('''enable_feature_transformation_operations is set to False 
                     but the newly added operation ({}) will be used in generating the features.'''.format(operation))
        pfunc = partial(function)
        pfunc.__name__ = operation
        pfunc.__doc__ = function.__doc__
        if hasattr(function, "__dict__") and not isinstance(function, type):
            pfunc.__dict__.update(function.__dict__.copy())

        setattr(self, operation, pfunc)

        operation = '@self.' + operation + '({})'
        self.single_feature_operations.append(operation)

    def remove_transformation_operation(self, operations):
        if type(operations) == str:
            operations = '@' + operations + '({})'
            if operations in self.single_feature_operations:
                self.single_feature_operations.remove(operations)
        elif type(operations) == list:
            for operation in operations:
                operation = '@' + operation + '({})'
                if operation in self.single_feature_operations:
                    self.single_feature_operations.remove(operation)
        else:
            logging.error('operations should be a string or a list of strings.')
