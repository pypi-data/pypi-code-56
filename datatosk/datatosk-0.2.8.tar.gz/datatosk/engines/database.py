from abc import ABCMeta, abstractmethod
from os import getenv
from typing import List, Any, Union, Dict, Callable, Optional, Sequence

import pandas as pd  # type: ignore
import pandas_gbq  # type: ignore
import sqlalchemy

from .. import consts


class _DataBaseEngine(metaclass=ABCMeta):

    """
    Abstract class from which all database engine classes inherit.
    
    Derived classes must implement `__init__()` and `query()` and `update()` methods.
    """

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def read(
        self,
        query: str,
        output_type: str = consts.output_types.PANDAS,
        params: Optional[Dict[str, Union[str, int, float, Sequence]]] = None,
        **kwargs,
    ):
        """
        Abstract method which is used as interface for retrieving data from databases.

        Args:
            query: query string for extracting data.
            output_type: type of an object which will be output from query operation.
            params: query params to be passed to query function
        """

    @abstractmethod
    def write(self, obj: Any):
        """
        Abstract method which is used as interface for sending data to sources.
        """


class MySQLEngine(_DataBaseEngine):
    """
    Class that enables to connect to MySQL database and retrieve data from it.

    Attributes:
        host: MySQL host needed to connect to database.
        port: MySQL port needed to connect to database.
        user: MySQL user needed to connect to database.
        password: MySQL password needed to connect to database.
        database: MySQL database needed to connect to database.
    """

    def __init__(self, source_name: str):
        # TODO: As more use cases arise, move configuration to a separate module.

        super().__init__()

        self.host = getenv(f"MYSQL_{source_name}_HOST".upper())
        self.port = int(getenv(f"MYSQL_{source_name}_PORT".upper(), "3306"))
        self.user = getenv(f"MYSQL_{source_name}_USER".upper())
        self.password = getenv(f"MYSQL_{source_name}_PASS".upper())
        self.database = getenv(f"MYSQL_{source_name}_DB".upper())

    def read(
        self,
        query: str,
        output_type: str = consts.output_types.PANDAS,
        params: Optional[Dict[str, Union[str, int, float, Sequence]]] = None,
        **kwargs,
    ) -> Union[pd.DataFrame, list, dict]:
        """
        Fetches data from a MySQL.

        Args:
            query: query string for extracting data.
            output_type: type of an object which will be output from query operation.
            params: query params to be passed to mysql query function
            kwargs: when `output_type="pandas"` kwargs will be transferred to `pd.read_sql`

        Raises:
            NotImplementedError: An error occurred when not supported `output_type`.

        Examples:
            >>> import datatosk
            >>> source = datatosk.Source.mysql(source_name="local")
            >>> source.read(
            ...     query="SELECT * FROM table WHERE col1 IN %(param)s",
            ...     output_type="pandas",
            ...     params={"param": [1, 2]}
            ... )
               col1  col2
            0     1     3
            1     2     4
        """

        output_type_map: Dict[str, Callable] = {
            consts.output_types.PANDAS: self._output_pandas,
            consts.output_types.LIST: self._output_list,
            consts.output_types.DICT: self._output_dict,
        }

        engine = sqlalchemy.create_engine(
            f"mysql+mysqldb://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}?charset=utf8mb4",
            pool_recycle=3600,
        )

        try:
            return output_type_map[output_type](query, engine, params, **kwargs)
        except KeyError:
            raise TypeError(f"possible output_types: {list(output_type_map.keys())}")

    def write(self, obj: Any):
        """
        [TODO]
        """
        raise NotImplementedError

    @staticmethod
    def _output_pandas(
        query: str,
        engine: sqlalchemy.engine.Engine,
        params: Optional[Dict[str, Union[str, int, float, Sequence]]] = None,
        **kwargs,
    ) -> pd.DataFrame:
        """
        Outputs data from a MySQL query in pandas DataFrame object.

        Args:
            query: query string for extracting data.
            engine: sqlalchemy.engine.Engine object.
            params: query params to be passed to pandas.read_sql() function

        Returns:
            pandas.DataFrame with queried data.
        """

        return pd.read_sql(query, con=engine, params=params, **kwargs)

    @staticmethod
    def _output_list(
        query: str,
        engine: sqlalchemy.engine.Engine,
        params: Optional[Dict[str, Union[str, int, float, Sequence]]] = None,
    ) -> list:
        """
        Outputs data from a MySQL query in a list.

        Args:
            query: query string for extracting data.
            engine: sqlalchemy.engine.Engine object.
            params: query params to be passed to cursor.execute() function


        Returns:
            One element list if one column selected, otherwise nested list.
        """
        with engine.connect() as connection:

            if params is None:
                result = connection.execute(query)
            else:
                result = connection.execute(query, params)

            return [
                item[0] if len(item) == 1 else list(item) for item in result.fetchall()
            ]

    @staticmethod
    def _output_dict(
        query: str,
        engine: sqlalchemy.engine.Engine,
        params: Optional[Dict[str, Union[str, int, float, Sequence]]] = None,
    ) -> List[dict]:
        """
        Outputs data from a MySQL query in a list of dicts.

        Args:
            query: query string for extracting data.
            engine: sqlalchemy.engine.Engine object.
            params: query params to be passed to cursor.execute() function

        Returns:
            List of dictionaries in which keys are column names.
        """
        with engine.connect() as connection:

            if params is None:
                result = connection.execute(query)
            else:
                result = connection.execute(query, params)

            columns = [column[0] for column in result.description]

            return [dict(zip(columns, row)) for row in result.fetchall()]


class GoogleBigQueryEngine(_DataBaseEngine):

    """
    Class that enables to connect to GoogleBigQuery database 
    and retrieve data from it.

    Attributes:
        project_id: GBQ project_id needed to connect to database.
    """

    def __init__(self, dataset: str):

        super().__init__()
        self.project_id = getenv(f"GBQ_{dataset}_PROJECT_ID".upper(), "")

    def read(
        self,
        query: str,
        output_type: str = consts.output_types.PANDAS,
        params: Optional[Dict[str, Union[str, int, float, Sequence]]] = None,
        **kwargs,
    ):
        """
        Fetches data from a GoogleBigQuery.
        
        Args:
            query: query string for extracting data.
            output_type: type of an object which will be output from query operation.
            params: [TODO]
        
        Returns:
            Queried data from GBQ database in type specified in `output_type".
        """

        output_type_mapper = {
            consts.output_types.PANDAS: self._output_pandas,
            consts.output_types.LIST: self._output_list,
            consts.output_types.DICT: self._output_dict,
        }
        try:
            return output_type_mapper[output_type](query, self.project_id)
        except KeyError:
            raise TypeError(f"possible output_types: {list(output_type_mapper.keys())}")

    def write(self, obj: Any):
        """
        [TODO]
        """
        raise NotImplementedError

    @staticmethod
    def _output_pandas(query: str, project_id: str) -> pd.DataFrame:
        """
        Outputs data from a GBQ query in pandas DataFrame object.

        Args:
            query: query string for extracting data.
            project_id: GBQ project_id string.

        Returns:
            pandas.DataFrame with queried data.
        """
        return pandas_gbq.read_gbq(query=query, project_id=project_id)

    @staticmethod
    def _output_list(query: str, project_id: str):
        """
        [TODO]

        Raises:
            NotImplementedError
        """
        raise NotImplementedError

    @staticmethod
    def _output_dict(query: str, project_id: str):
        """
        [TODO]

        Raises:
            NotImplementedError
        """

        raise NotImplementedError
