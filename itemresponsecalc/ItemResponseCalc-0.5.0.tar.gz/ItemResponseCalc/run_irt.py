"""Main template script to analyze ordinal response data using Item Response Theory.
This template should be copied and edited by the user for the desired application.

Arne Leijon, 2020-05-30, template example based on IOI-HA data analysis
2020-06-06, standalone version for ItemResponseCalc package
"""

# -------- __main__ check to prevent multiprocessor sub-tasks to re-run this script
if __name__ == '__main__':

    import numpy as np
    import pickle
    from pathlib import Path
    import datetime as dt
    import logging

    from ItemResponseCalc import ir_logging
    from ItemResponseCalc.item_response_data import Questionnaire
    from ItemResponseCalc.item_response_data import ItemResponseDataSet
    from ItemResponseCalc.item_response_data import item_response_table
    from ItemResponseCalc.table_reader import Table, Tables
    # Tables used to join data in teo or more files into one group
    from ItemResponseCalc.item_response_model import OrdinalItemResponseModel
    from ItemResponseCalc.ir_display import ItemResponseDisplaySet

    # ----------------------------------------------- ItemResponseModel parameters:
    max_n_traits = 4
    # = max number of traits to explain total set of item responses
    # = 1, if the test instrument is known to measure a uni-dimensional trait

    # n_scale_samples = 50
    # -> sampled set of scale threshold vectors
    n_scale_samples = 1
    # -> MAP-estimated single scale threshold vector
    n_subject_samples = 20
    # = number of sampled trait(s) for each respondent

    # NOTE: computation time is proportional to
    # n_subjects * n_scale_samples * n_subject_samples
    # n_scale_samples = 1 may give similar result as sampled scale model

    TEST_DOWNSAMPLE = 1
    # -> no down-sampling -> all records included
    # TEST_DOWNSAMPLE = 10
    # -> use smaller data subset only for faster initial test run

    # ------------------------------------------------------------------------
    TOP_PATH = Path.home() / 'Documents/LeijonKTH/heartech/HA-QualityRegistry'
    TOP_PATH = TOP_PATH / 'IRT-IOI-HA'
    # Change this example to top-dir for everything to be read or written here

    ioiha_data_path = TOP_PATH / 'IOI-HA-data'
    # path to actual item data files OTHER THAN data in sql server

    result_dir = TOP_PATH / 'IOI-HA-results'
    # path where results will be saved, for several runs if needed

    ioiha_file = ioiha_data_path / 'IOI-HA-English.txt'
    # text file containing the questions and response alternatives
    # If not available, a Questionnaire object must be created manually
    # as suggested below.

    # ------------------------------------------------------------------------
    timefmt = '{0.year}-{0.month:02}-{0.day:02}-{0.hour:02}{0.minute:02}'
    result_run = timefmt.format(dt.datetime.now())
    # -> name of sub-folder in result_dir

    save_dir = result_dir / result_run
    save_dir.mkdir(parents=True, exist_ok=True)
    # sub-path for results of this particular run

    model_file = 'irt-model.pkl'
    # = name of saved model in save_dir

    log_file = 'run_irt_log.txt'
    # = name of log file saved in same sub-folder
    # -------------------------------------------------------------------------

    # ------------------------------------- setup logging:
    ir_logging.setup(save_dir / log_file)
    logger = logging.getLogger(__name__)

    # -------------------------- common help functions for data input:
    def accept_record(r):
        """Inclusion criterion for accepting a record,
        to be called after any other data recoding in each input Table object.
        :param r: list with responses in ONE record read from file,
            encoded as integer values
        :return: boolean == True if record is acceptable
        """
        n_missing = sum(r_i is None or r_i < 1 or r_i > 5
                        for r_i in r)
        return n_missing <= 3

    def recode_missing_as_0(row):
        """Replace missing data by zero, as required by analysis.
        Table readers encode missing data as value = None
        :param row: list with responses in ONE record read from file
        :return: None, row elements recoded in place
        """
        for i in range(len(row)):
            if row[i] is None or row[i] < 1:  # or row[i] > 5: only for IOI-HA
                row[i] = 0
    # --------------------------------------------

    if TEST_DOWNSAMPLE > 1:
        logging.info(f'*** Test with down-sampling {TEST_DOWNSAMPLE}')

    # ------------------------------- Define questionnaire instrument
    # create a Questionnaire object to specify
    # number of items and response alternatives
    q_items = Questionnaire.load(ioiha_file)  # load from text file

    # if the text file is not available, create q_items manually, e.g.:
    # r_levels = [5, 5, 5, 5, 5, 5, 5]
    # # = list with number of response levels, one element for each item
    # # Example: all seven IOI-HA items have 5 response levels
    # q_items = Questionnaire(item_response_levels=r_levels)

    # ------------------------------- Define included data sets:
    data_groups = dict()  # space for all included groups

    # Example: Include two xlsx files from Hickson, Australia:
    # Responses have already been coded as integers 1,..., 5 in the file
    au1_file = ioiha_data_path / 'Hickson' / 'Short_Eartrak AUS.xlsx'
    logger.info(f'AU-H-10: Using {au1_file}')

    au1 = item_response_table(au1_file,
                              fields=[f'Q0{i}' for i in range(1, 8)],  # labels in header row
                              field_types=int,
                              missing_values=['.', ' '],
                              header_row=1,
                              sample_factor=TEST_DOWNSAMPLE,
                              recode_fcns=recode_missing_as_0,
                              accept_row=accept_record)
    data_groups['AU-H-10'] = au1

    au2_file = ioiha_data_path / 'Hickson' / 'Eartrakdata_10_May_08.xlsx'
    logger.info(f'AU-H-10e: Using {au2_file}')

    au2 = item_response_table(au2_file,
                              fields=[f'Q0{i}' for i in range(1, 8)],
                              field_types=int,
                              missing_values=['.', ' '],
                              header_row=1,
                              sample_factor=TEST_DOWNSAMPLE,
                              recode_fcns=recode_missing_as_0,
                              accept_row=accept_record)
    data_groups['AU-H-10e'] = au2

    # Include two csv files from S Kramer:

    nle_file = ioiha_data_path / 'Kramer' / 'moeder_final - kopieforArne.csv'
    logger.info(f'NL-02: Using {nle_file}')

    nle1 = item_response_table(file_path=nle_file,
                               fmt='csv',
                               fields=[f'ioi_v{i}' for i in range(1, 8)],
                               field_types=int,
                               missing_values=[9.0, ''],
                               sample_factor=TEST_DOWNSAMPLE,
                               recode_fcns=recode_missing_as_0,
                               accept_row=accept_record)

    # -------------------------------------------
    def recode_fields14(row):
        """IOI-HA items 1 and 4 coded as 0-4 in NLSH-Kramer-T2IOI-HA.csv
        must be recoded as values 1-5,
        BEFORE recoding missing-data as zero.
        """
        for i in [1, 4]:
            if row[i - 1] is not None:
                row[i - 1] += 1
    # --------------------------------------------

    nle2_file = ioiha_data_path / 'Kramer' / 'NLSH-Kramer-T2IOI-HA.csv'
    logger.info(f'NL-16: Using {nle2_file}')

    nle2 = item_response_table(file_path=nle2_file,
                               fmt='csv',
                               sample_factor=TEST_DOWNSAMPLE,
                               fields=[f'T2IOIHA{i + 1}' for i in range(7)],
                               missing_values=[9999999.0],
                               field_types=int,
                               recode_fcns=[recode_fields14,
                                            recode_missing_as_0],
                               # recode_fcns are called in given order
                               accept_row=accept_record)
    # Example: join both data files into ONE group:
    data_groups['NL-02-16'] = Tables(nle1, nle2)

    # *** Example: include data for one year from an SQL database:

    # from ItemResponseCalc.table_reader_sql import Table
    # = special Table reader for SQL access

    # haq_config = dict(user='user_id',
    #                   password='********',
    #                   host='127.0.0.1',  # IP address of SQL server
    #                   port='1111',  # access port to SQL server
    #                   database='hbdb',  # name of database on SQL server
    #                   connect_timeout=10  # seconds wait in case no access
    #                   )
    # = access arguments for SQL database

    # table = 'prescriptions'  # name of desired table in the database
    #
    # where = ("respondent = 1 " +
    #          "AND (Q2 = 1 OR Q2 = 2) " +
    #          "AND date BETWEEN %s AND %s"
    #          )
    # # = WHERE section of SELECT statement for SQL database
    # # with following two dates as arguments:
    # year_2019 = (dt.date(2019, 1, 1), dt.date(2019, 6, 30))

    # data_groups['SE-19'] = Table(table_id=table,
    #                              connect_kwargs=haq_config,  # SQL access
    #                              select_where=where,
    #                              select_args=year_2019,
    #                              fields=[f'Q{i}' for i in range(3, 10)],
    #                              # = IOI-HA field labels in database
    #                              recode_fcns=recode_missing_as_0,
    #                              accept_row=accept_record,
    #                              sample_factor=TEST_DOWNSAMPLE * 10)

    # --------------------------- Collect all groups into ONE DataSet object:

    ids = ItemResponseDataSet(questionnaire=Questionnaire.load(ioiha_file),
                              groups=data_groups)
    # NOT YET actually reading any data
    # In case of read error, it will show here:
    logging.info('Item Response Data collected = \n' + repr(ids))

    total_count = np.array([np.sum(c_i) for c_i in ids.item_response_count])
    logging.info('Total Response Counts: ' + np.array2string(total_count))

    # --------------------------- Create ItemResponseModel from data:

    irm = OrdinalItemResponseModel.initialize(ids,
                                              n_traits=max_n_traits,
                                              n_scale_samples=n_scale_samples,
                                              n_subject_samples=n_subject_samples,
                                              trait_scale=3.)  # *** = default

    logging.info(f'Learning model with max {irm.n_traits} traits'
                 + f' for {irm.n_groups} groups'
                 + f' with {irm.n_subjects} subject records in total')
    logging.info(f'The model uses {n_scale_samples} scale samples'
                 + f' and {n_subject_samples} samples for each subject')

    LL = irm.learn(max_hours=30)
    # *** It may take MANY hours, try setting shorter time limit first
    # When learning is complete, it will finish before the time limit
    # If learning was complete, the LL values should reach a plateau level

    logging.info(f'Learned model with {irm.n_groups} groups'
                 + f' with {irm.n_subjects} subjects in total')
    LL = np.array(LL)
    logging.info('Log Likelihood: ' + np.array2string(LL, precision=1))
    # if learning was complete, it should finish before the time limit,
    # and the LL values should should reach a nearly constant level

    # ------------------ save model for later input to show_irt script
    with (save_dir / model_file).open('wb') as f:
        pickle.dump(irm, f)

    logging.info(f'Result saved in {save_dir}')

    logging.info('Learned model = \n' + repr(irm))

    # ------------------------------------- Display Model Results:
    # The display can also be done by separate script show_irt.py

    # ------------------------------------- Trait Covariance before standardization
    # only informative, may be commented out
    c = irm.precision_within.mean_inv
    logging.info('Predictive Trait Covariance Within Populations =\n'
                 + np.array2string(c, precision=3, suppress_small=True))

    c = irm.precision_among.mean_inv
    logging.info('Predictive Trait Variance Among Populations= '
                 + np.array2string(c, precision=3, suppress_small=True))

    # ------------------------------------- Global Predictive Covariance
    c = irm.predictive_individual_cov()
    logging.info('Predictive Global Trait Cov (before standardization) =\n'
                 + np.array2string(c, precision=3, suppress_small=True))

    # -------------------------------------  prune and standardize:
    irm.prune()  # keep only traits that were really needed to model the data

    irm.standardize()  # re-scale all parameters for unity global trait variance

    c = irm.predictive_individual_cov()
    logging.info('Pruned and Standardized Predictive Global Trait Cov =\n'
                 + np.array2string(c, precision=3, suppress_small=True))
    s = np.sqrt(np.diag(c))
    logging.info('Predictive St.Dev. after Standardization = '
                 + np.array2string(s, precision=3))

    # ------------------------------------- display with standardized scale
    # mapping_item used to transform trait scale back to ONE item rating scale
    ir_display = ItemResponseDisplaySet.show(irm,
                                             mapping_item=-1,  # last questionnaire item
                                             figure_format='pdf',  # OR eps, png,...
                                             table_format='latex',  # OR tab
                                             )
    ir_display.save(save_dir)

    # ------------------------------------- Within-group trait correlation
    if irm.n_traits > 1:
        cov_within = irm.precision_within.mean_inv
        logging.info('Predictive Trait Covariance Within Populations:\n' +
                     np.array2string(cov_within, precision=3))
        s = np.sqrt(np.diag(cov_within))
        c = cov_within / s
        c /= s[:, np.newaxis]
        # = normalized correlation matrix, also tabulated in ir_display:
        logging.info('Predictive Trait Correlation Within Populations:\n' +
                     np.array2string(c, precision=3))

        # ------------------------------------- PCA of within-group covariance

        (eig_val, eig_vec) = np.linalg.eigh(cov_within)
        logging.debug('Cov eig_val= ' +
                      np.array2string(eig_val, precision=3))
        logging.debug('Cov eig_vec=\n' +
                      np.array2string(eig_vec, precision=3))
        eig_val_cum = np.cumsum(eig_val[::-1]) / np.sum(eig_val)
        logging.info(f'One, Two, etc Principal Trait Factors: ' +
                     ', '.join(f'{ev:.1%}'
                               for ev in eig_val_cum) +
                     ', of Variance within Populations')

    logging.shutdown()
