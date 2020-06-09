from stockdatadownloader.CommonVariable import STOCK_BIT_CSV_FILE_PATH
from stockdatadownloader.StockBitColumn import MONTH_COLUMN, DATE_COLUMN
from stockdatadownloader.fetcher.StockBitFetcher import StockBitFetcher
import pandas as pd


# all date are string in format yyyy-mm-dd
class StockBitQuery:
    list_df = {}

    @staticmethod
    def get_trading_dates(stock_name):
        df = pd.read_csv(STOCK_BIT_CSV_FILE_PATH + stock_name + '_price.csv')
        return df[DATE_COLUMN]

    @staticmethod
    def query_data_fundamentals(stock_name, date, column_name, total_last_quarter):
        response = []
        quarters = StockBitQuery.__get_quarters_string(date, total_last_quarter)

        for quarter in quarters:
            response.append(StockBitQuery.__query_data_fundamental(column_name, quarter, stock_name))

        return response

    @staticmethod
    def query_data_fundamental(stock_name, date, column_name):
        quarter = StockBitQuery.__get_quarters_string(date, 1)[0]

        return StockBitQuery.__query_data_fundamental(column_name, quarter, stock_name)

    @staticmethod
    def __query_data_fundamental(column_name, quarter, stock_name):
        for report_type in StockBitFetcher.REPORT_TYPES:
            file_name = STOCK_BIT_CSV_FILE_PATH + stock_name + '_' + report_type + '.csv'
            df = StockBitQuery.__get_csv_file(file_name)

            if df is None:
                return

            if column_name in df:
                response = df.query(MONTH_COLUMN + " == '" + quarter + "'")[column_name].values
                if len(response) == 1:
                    return response[0]
        return None

    @staticmethod
    def query_data_price(stock_name, date, column_name):
        file_name = STOCK_BIT_CSV_FILE_PATH + stock_name + '_price.csv'
        df = StockBitQuery.__get_csv_file(file_name)

        if df is None:
            return

        if column_name in df:
            response = df.query(DATE_COLUMN + " == '" + date + "'")[column_name].values
            if len(response) == 1:
                return response[0]

        return None

    @staticmethod
    def __get_csv_file(file_name):
        if file_name in StockBitQuery.list_df:
            return StockBitQuery.list_df[file_name]

        try:
            df = pd.read_csv(file_name)
        except FileNotFoundError:
            df = None

        StockBitQuery.list_df[file_name] = df
        return df

    @staticmethod
    def __get_quarters_string(date_string, total_last_quarter):
        date = pd.to_datetime(date_string)
        response = []

        quarter = StockBitQuery.__get_quarter(date.month)
        year = date.year

        while total_last_quarter > 0:
            if quarter == 0:
                quarter = 4
                year -= 1

            response.append("Q" + str(quarter) + " " + str(year))

            total_last_quarter -= 1
            quarter -= 1

        response.reverse()
        return response

    @staticmethod
    def __get_quarter(month):
        return (month - 1) // 3
