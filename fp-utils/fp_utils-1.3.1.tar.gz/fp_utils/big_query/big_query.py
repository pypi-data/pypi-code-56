from google.oauth2 import service_account #Service Account
import pandas_gbq #Pandas GBQ.
from google.cloud import bigquery #To connect to BigQuery.
import os
import boto3
from ast import literal_eval
import pandas as pd
import datetime


def read_big_query(query, project, creds_path):
    '''
    query (str): SQL query
    project (str): Then name of the Big Query project
    creds_path (str): Path to service account json file (_eg. 'creds/google_creds.json'_)

    returns: Pandas dataframe with query data.
    '''

    #Authenticate
    credentials = service_account.Credentials.from_service_account_file(creds_path)
    pandas_gbq.context.credentials = credentials

    #Read in dataframe.
    data_frame = pandas_gbq.read_gbq(
        query,
        project_id=project,
        dialect='standard')

    return data_frame

#Write DF to Big Query
def df_to_big_query(dataframe, project, dataset, table, creds_path):
    '''
    dataframe (pandas dataframe): The data that you want uploaded to Big Query.
    project (str): The name of the Big Query project.
    dataset (str): The name of the Big Query dataset.
    table (str): The name of the Big Query table.
    creds_path (str): Path to the service account json file (_eg. 'creds/google_creds.json'_)

    returns: Nothing (Might want to change this).
    '''

    client = bigquery.Client.from_service_account_json(creds_path, project=project)

    query = (f'SELECT * FROM `{dataset}.{table}`')
    query_job = client.query(query)
    big_query_table = query_job.result()
    table_ = big_query_table

    dataset_ref = client.dataset(dataset)
    dataset = bigquery.Dataset(dataset_ref)
    table_ref = dataset.table(table)
    table = bigquery.Table(table_ref)
    tschema = big_query_table.schema
    # convert dataframe to a list
    data = dataframe.values
    # convert list to dictionary
    macro = []
    for entry in data:
        micro = {}
        for i,item in enumerate(entry):
            micro[tschema[i].name] = item
        macro.append(micro.copy())

    errors = client.insert_rows(table,macro,selected_fields=tschema)
    return errors

class BigQuery():
    def df_to_big_query(self,dataframe, project, dataset, table, **kwargs):
        '''
        *dataframe (pandas dataframe): The data that you want uploaded to Big Query.
        *project (str): The name of the Big Query project.
        *dataset (str): The name of the Big Query dataset.
        *table (str): The name of the Big Query table.
        creds_path=(str): Path to the service account json file (_eg. 'creds/google_creds.json'_)
        remove_duplicates=(bool): If true, request will only submit values that are unique and not currently in the big query database
        creds_from_service_account_info=(bool): If true, credentials will be acquired through amazon s3 bucket and will require the following environment variables: ['AWS_ACCESS_KEY_ID'],['AWS_SECRET_ACCESS_KEY'],['AWS_BUCKET'],['AWS_GOOGLE_APPLICATION_CREDENTIALS_FILE']
        replace_table=(bool): If true, request will erase all values from database and replace with new values found in the dataframe sent in the to_gbq function

        returns: 'Success' if database successfully update
        '''

        remove_duplicates, creds_from_service_account_info, database_action = BigQuery.__check_df_to_big_query_kwargs(self,kwargs)

        if creds_from_service_account_info:
            service_account_json = BigQuery.__get_credentials_from_s3(self)
            credentials = service_account.Credentials.from_service_account_info(service_account_json)
            client = bigquery.client.Client(project,credentials=credentials)
        else:
            credentials = service_account.Credentials.from_service_account_file(kwargs['creds_path'])
            client = bigquery.client.Client(project,credentials=credentials)

        dataset_table = f'{dataset}.{table}'
        query = (f'SELECT * FROM `{dataset_table}`')
        query_job = client.query(query)
        bq_data = query_job.result()
        tschemas = bq_data.schema
        schema = [{'name':tschema.name, 'type':tschema.field_type} for tschema in tschemas]

        bq_array = [row.values() for row in bq_data]
        bq_columns = [column['name'] for column in schema]

        bigquery_dataframe = pd.DataFrame(bq_array,columns=bq_columns)
        # pandas_gbq.context.credentials = credentials
        # bigquery_dataframe = pandas_gbq.read_gbq(query, project_id=project, dialect='standard')

        if database_action == 'append' and remove_duplicates == True:
            bigquery_dataframe = bigquery_dataframe.append(bigquery_dataframe)
            dataframe = dataframe.append(bigquery_dataframe)
            dataframe = dataframe.drop_duplicates(keep=False)

        pandas_gbq.context.credentials = credentials
        dataframe.to_gbq(project_id=project,destination_table=dataset_table,credentials=credentials,if_exists=database_action,table_schema=schema)

        return 'Success'


    # --------------------------------- Private BigQuery Class Functions ---------------------------------
    # ----------------------------------------------------------------------------------------------------


    def __get_credentials_from_s3(self):
        s3 = boto3.resource('s3',
                            aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                            aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY']
                            )
        obj = s3.Object(os.environ['AWS_BUCKET'],os.environ['AWS_GOOGLE_APPLICATION_CREDENTIALS_FILE'])
        body = obj.get()['Body'].read()
        service_account_json = literal_eval(body.decode('utf8'))
        return service_account_json

    def __check_df_to_big_query_kwargs(self,kwargs):
        if 'creds_path' not in kwargs.keys() and 'creds_from_service_account_info' not in kwargs.keys():
            raise ArgumentError('Must either pass in argument creds_path with valid path to service account file or argument creds_from_service_account_info=True')
        if 'remove_duplicates' in kwargs.keys():
            if kwargs['remove_duplicates']:
                remove_duplicates = True
            else:
                remove_duplicates = False
        else:
            remove_duplicates = False
        if 'creds_from_service_account_info' in kwargs.keys():
            if kwargs['creds_from_service_account_info']:
                creds_from_service_account_info = True
            else:
                creds_from_service_account_info = False
        else:
            creds_from_service_account_info = False
        if 'replace_table' in kwargs.keys():
            if kwargs['replace_table']:
                database_action='replace'
            else:
                database_action='append'
        else:
            database_action='append'

        return remove_duplicates, creds_from_service_account_info, database_action

class ArgumentError(Exception):
    pass
