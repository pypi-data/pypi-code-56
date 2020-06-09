import pandas as pd
import s3fs
import os
import boto3
from pandas_profiling import ProfileReport

''' 
The DataIO Class can be instantiaded with AWS keys for download data
'''

class DataIO:
    r''' 
    Parameters
        ----------
        aws_access_key_id : str, default None
            Is the AWS Access Id provided AWS
        aws_secret_access_key : str, default None
            Is the AWS Access Key provided AWS
        datalake : str, default None
            Is the datalake to use for download the data using the DataIO methods classes
        prefix_s3 : str, default 's3://'
            Is the prefix used by AWS S3 for connecting with datalakes
        local_path : str, default '/tmp/'
            Is the address of the temporal folder of the server which is running the process.

    :return: The class return a object class that could invoke the differents methods
    :rtype: object 

    Examples
    --------
    >>> import datup as dt
    >>> _object = dt.DataIO("aws_key_id","aws_key")
    '''

    def __init__(self,aws_access_key_id,aws_secret_access_key, datalake, prefix_s3="s3://", local_path="/tmp/"):
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.datalake = datalake
        self.aws_credentials_s3fs = s3fs.core.S3FileSystem(anon=False, key=aws_access_key_id, secret=aws_secret_access_key)
        self.aws_credentials_s3 = boto3.resource('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
        self.prefix_s3 = prefix_s3 
        self.local_path = local_path   

    def download_csv(
        self,
        stage=None, 
        filename=None,
        datecols=False, 
        sep=",", 
        encoding="ISO-8859-1",
        infer_datetime_format=True,
        low_memory=False,
        indexcol=None,
        ts_csv = False,
        freq=None
    ):
        r"""
        Return a dataframe downloaded from a specified datalake.
        This function takes the aws credentials from DataIO class and use it for download 
        the required data.

        Parameters
        ----------
        stage : str, default None
            It is the set of folders after the datalake to the file that is required to download 
        filename : str, default None
            Is the name of the filename to download without csv suffix
        datecols: bool or list of int or names or list of lists or dict, default False
            Took it from Pandas read_csv parse_dates description
            The behavior is as follows:
                * boolean. If True -> try parsing the index.
                * list of int or names. e.g. If [1, 2, 3] -> try parsing columns 1, 2, 3 each as a separate date column.
                * list of lists. e.g. If [[1, 3]] -> combine columns 1 and 3 and parse as a single date column.
                * dict, e.g. {‘foo’ : [1, 3]} -> parse columns 1, 3 as date and call result ‘foo’
                If a column or index cannot be represented as an array of datetimes, say because of an unparseable value
                or a mixture of timezones, the column or index will be returned unaltered as an object data type. For
                non-standard datetime parsing, use pd.to_datetime after pd.read_csv. To parse an index or column with
                a mixture of timezones, specify date_parser to be a partially-applied pandas.to_datetime() with
                utc=True. See Parsing a CSV with mixed timezones for more.
                Note: A fast-path exists for iso8601-formatted dates.
        sep: str, default ‘,’
            Took it from Pandas read_csv sep description
            Delimiter to use. If sep is None, the C engine cannot automatically detect the separator, but the Python
            parsing engine can, meaning the latter will be used and automatically detect the separator by Python’s
            builtin sniffer tool, csv.Sniffer. In addition, separators longer than 1 character and different from '\s+'
            will be interpreted as regular expressions and will also force the use of the Python parsing engine. Note
            that regex delimiters are prone to ignoring quoted data. Regex example: '\r\t'.
        encoding: str, default ‘ISO-8859-1’
            Took it from Pandas read_csv encoding description
            Encoding to use for UTF when reading/writing (ex. ‘utf-8’).
        infer_datetime_format: bool, default True
            Took it from Pandas read_csv infer_datetime_format description
            If True and parse_dates is enabled, pandas will attempt to infer the format of the datetime strings in the
            columns, and if it can be inferred, switch to a faster method of parsing them. In some cases this can
            increase the parsing speed by 5-10x.
        low_memory: bool, default True
            Took it from Pandas read_csv low_memory description
            Internally process the file in chunks, resulting in lower memory use while parsing, but possibly mixed
            type inference. To ensure no mixed types either set False, or specify the type with the dtype parameter.
            Note that the entire file is read into a single DataFrame regardless, use the chunksize or iterator
            parameter to return the data in chunks. (Only valid with C parser).
        indexcol : int, str, sequence of int / str, or False, default None
                Took it from Pandas read_csv index_col description
                Column(s) to use as the row labels of the DataFrame, either given as string name or column index. If a
                sequence of int / str is given, a MultiIndex is used. 
                Note: index_col=False can be used to force pandas to not use the first column as the index, e.g. when
                you have a malformed file with delimiters at the end of each line.
        ts_csv : bool, default False
            If ts_csv is True then activates the ts_csv downloaded. If True, indexcol and freq, both must
            be different to None
        freq : str, default W-MON
            Is the frequency of getting data.

        Returns
        -------
        :rtype: DataFrame
        :return: A DataFrame is return as two-dimensional data structure
        
        Examples
        --------
        >>> object.download_csv(stage='stage',filename='filename') 
        """

        try:
            complete_path = str(os.path.join(self.prefix_s3, self.datalake,stage,filename+".csv")).replace("\\","/")
            if ts_csv and indexcol is not None and freq is not None:
                df = pd.read_csv(
                    self.aws_credentials_s3fs.open(complete_path),
                    sep=sep, 
                    encoding=encoding,
                    infer_datetime_format=infer_datetime_format,
                    low_memory=low_memory, 
                    index_col=indexcol
                )
                df.index = pd.to_datetime(df.index)
                df.index.freq=freq
            elif ts_csv and indexcol is None and freq is not None:
                print("Is necessary an indexcol value")
            elif ts_csv and indexcol is not None and freq is None:
                print("Is necessary a freq value")            
            else:                
                df = pd.read_csv(
                    self.aws_credentials_s3fs.open(complete_path),
                    sep = sep,
                    encoding= encoding, 
                    infer_datetime_format = infer_datetime_format,
                    low_memory=low_memory, 
                    parse_dates=datecols
                )        
        except FileNotFoundError as error:      
            print(f'Exception found:{error}')  
            raise
        return df

    def download_csvm(self,uris):
        r"""
        Return a set of dataframes downloaded from a specified datalake in a list.
        This function takes the aws credentials from DataIO class and use it for download 
        the required data through download_csv method.

        Parameters
        ----------
        uris : dict
            Is the dictionary with all parameters necessary for the download_csv method
        
        Returns
        -------
        :rtype: List of DataFrames
        :return: A list of DataFrames are returned
        :rtype: List of DataFrames Names
        :return: A list of DataFrames Names are return in string type
        
        Examples
        --------
        >>> uris = {
                "uri_1":{
                    "stage":"stage",
                    "filename":"filename",
                    "datecols":False,
                    "sep":";",
                    "encoding":"ISO-8859-1"
                },
                "uri_2":{
                    "stage":"stage",
                    "filename":"filename",
                    "datecols":False,
                    "sep":";",
                    "encoding":"ISO-8859-1"
                }
            }
        >>> df, df_names =object.download_csvm(uris=uris)  # doctest: +SKIP        
        """

        try:
            dataframes = []
            dataframes_names = []
            for k,v in uris.items():  
                exec("df_{} = self.download_csv(stage='{}',filename='{}',sep='{}',encoding='{}', datecols={})".format(k,v["stage"],v["filename"],v["sep"],v["encoding"],v["datecols"]))
                exec("dataframes.append(df_{})".format(k))
                exec("dataframes_names.append('df_{}')".format(k))
        except AttributeError as error:
            print(f'Exception found:{error}')  
            raise
        return dataframes, dataframes_names

    def upload_csv(
        self,
        df,
        stage=None,
        filename=None,
        index=False,
        header=True,
        date_format="%Y-%m-%d",
        ts_csv=False
    ):  
        r"""
        Return a uri where the dataframes was uploaded in csv format.
        This function takes the aws credentials from DataIO class and use it for upload
        the required data.

        Parameters
        ----------
        df : DataFrame
            Is the DataFrame for uploading to S3 datalake
        stage : str, default None
            It is the set of folders after the datalake to the file that is required to upload 
        filename : str, default None
            Is the name of the filename to upload without csv suffix
        index : bool, default False
            Took it from Pandas to_csv index description
            Write row names (index).
        header : bool or list of str, default True
            Took it from Pandas to_csv index description
            Write out the column names. If a list of strings is given it is assumed to be aliases for
            the column names.
        date_format : str, default %Y-%m-%d
            Took it from Pandas to_csv index description
            Format string for datetime objects.
        ts_csv : bool, default False
            If ts_csv is True then activates the ts_csv upload. If True, index must be different to False
        
        Returns
        -------
        :rtype: Str
        :return: The uri where DataFrame was uploaded into S3
                
        Examples
        --------
        >>> object.upload_csv(df,stage="stage",filename="filename")        
        """

        try:
            complete_s3_path = str(os.path.join(self.prefix_s3, self.datalake,stage,filename,filename+".csv")).replace("\\","/")
            complete_local_path = str(os.path.join(self.local_path,filename+".csv")).replace("\\","/")
            medium_s3_path = str(os.path.join(stage, filename, filename+'.csv').replace("\\","/"))
            if ts_csv and index:
                df.to_csv(complete_local_path, index=index, header=header, date_format=date_format)
                self.aws_credentials_s3.Bucket(self.datalake).upload_file(complete_local_path, medium_s3_path)
            if ts_csv and not index:
                print("Is necessary use index True for ts_csv mode")
            if index and not ts_csv:
                print("Is necessary use ts_csv True")
            else:
                df.to_csv(complete_local_path, index=index, header=header, date_format=date_format)
                self.aws_credentials_s3.Bucket(self.datalake).upload_file(complete_local_path, medium_s3_path)                
            upload_path = complete_s3_path
        except FileNotFoundError as error:
            print(f'Exception found:{error}')         
            raise    
        return upload_path

    def generate_profiling(
        self,
        df,
        stage=None,
        filename=None,
        save=False,
        minimal=True
    ):
        r"""
        Return a html embbeded with the DataFrame profiling data or save it into a S3 datalake .
        This function takes the aws credentials from DataIO class and use it for upload
        the required data, after this, the method can save or not the result by the save flag.

        Parameters
        ----------
        df : DataFrame
            Is the DataFrame for profiling the data
        stage : str, default None
            It is the set of folders after the datalake to the file that is required to upload,
            this method just apply if save parameter is True 
        filename : str, default None
            Is the name of the filename to upload without html suffix, 
            this method just apply if save parameter is True
        save : bool, default False
            If save is False, the html was embedded in the worksheet if True, the html will be saved into a 
            S3 datalake
        minimal : bool, default True
            If minimal is True the method disables expensive computations (such as correlations and dynamic binning)
        
        Returns
        -------
        :rtype: Html
        :return: A Html is returned by the method
                
        Examples
        --------
        >>> object.generate_profiling(df)        
        """

        try:
            profile = ProfileReport(df, minimal=minimal)
            if save: 
                complete_s3_path = str(os.path.join(self.prefix_s3, self.datalake,stage,filename,"{}.html".format(filename))).replace("\\","/")         
                medium_s3_path = str(os.path.join(stage, filename,"{}.html".format(filename))).replace("\\","/")
                profile.to_file("{}{}.html".format(self.local_path,filename))
                self.aws_credentials_s3.Bucket(self.datalake).upload_file("{}{}.html".format(self.local_path,filename), medium_s3_path)
                return complete_s3_path
            else:
                return profile.to_notebook_iframe()
        except:
            print('Exception found: ') 
            raise
    
    def upload_model(
        self,
        model,
        stage=None,
        filename=None
    ):
        r"""
        The upload_model save a pkl model and return the S3 datalake path where saved.

        Parameters
        ----------
        model : str
            Is the pkl model
        stage : str, default None
            It is the set of folders after the datalake to the file that is required to upload,
        filename : str, default None
            Is the name of the filename to upload without pkl suffix, 
                
        Returns
        -------
        :rtype: Str
        :return: The path where model saved is returned
                
        Examples
        --------
        >>> object.upload_model(model, stage="stage", filename="filename")        
        """

        try:        
            complete_s3_path = str(os.path.join(self.prefix_s3, self.datalake, stage, filename, "{}.pkl".format(filename))).replace("\\","/")
            route_model = str(os.path.join(self.local_path,"{}.pkl".format(filename))).replace("\\","/") 
            medium_s3_path = str(os.path.join(stage, filename, "{}.pkl".format(filename))).replace("\\","/")
            self.aws_credentials_s3.Bucket(self.datalake).upload_file(route_model, medium_s3_path)
        except FileNotFoundError as error:
            print(f'Exception found: {error}')
            raise    
        return complete_s3_path

    def upload_log(
        self,
        logfile,
        stage=None
    ):
        r"""
        The upload_log save the log of process and return the S3 datalake path where saved.

        Parameters
        ----------
        logfile : str
            Is the pkl model
        stage : str, default None
            It is the set of folders after the datalake to the file that is required to upload,
                
        Returns
        -------
        :rtype: Str
        :return: The path where log saved is returned
                
        Examples
        --------
        >>> object.upload_log(logfile, stage="stage")        
        """

        try:      
            complete_s3_path = str(os.path.join(self.prefix_s3, self.datalake, stage, logfile)).replace("\\","/")
            route_logfile = str(os.path.join(self.local_path, logfile)).replace("\\","/")
            medium_s3_path = str(os.path.join(stage, logfile)).replace("\\","/")
            self.aws_credentials_s3.Bucket(self.datalake).upload_file(route_logfile, medium_s3_path)
        except FileNotFoundError as error:
            print(f'Exception found: {error}')
            raise    
        return complete_s3_path



