from stockdatadownloader.CommonVariable import STOCK_BIT_CSV_FILE_PATH
from stockdatadownloader.StockBitColumn import MONTH_COLUMN, DATE_COLUMN
from stockdatadownloader.fetcher.StockBitFetcher import StockBitFetcher
import pandas as pd


class StockBitQuery:

    @staticmethod
    def get_trading_dates(stock_name):
        df = pd.read_csv(STOCK_BIT_CSV_FILE_PATH + stock_name + '_price.csv')
        return df[DATE_COLUMN]

    # all date are string in format yyyy-mm-dd
    @staticmethod
    def query_data_fundamental(stock_name, date, column_name):
        quarter = StockBitQuery.__get_quarter_string(date)

        for report_type in StockBitFetcher.REPORT_TYPES:
            df = pd.read_csv(STOCK_BIT_CSV_FILE_PATH + stock_name + '_' + report_type + '.csv')

            if column_name in df:
                response = df.query(MONTH_COLUMN + " == '" + quarter + "'")[column_name].values
                if len(response) == 1:
                    return response[0]

        print("query_data_fundamental is failed. Parameter:", stock_name, date, column_name)
        return None

    # all date are string in format yyyy-mm-dd
    @staticmethod
    def query_data_price(stock_name, date, column_name):
        df = pd.read_csv(STOCK_BIT_CSV_FILE_PATH + stock_name + '_price.csv')

        if column_name in df:
            response = df.query(DATE_COLUMN + " == '" + date + "'")[column_name].values
            if len(response) == 1:
                return response[0]

        print("query_data_price is failed. Parameter:", stock_name, date, column_name)
        return None

    @staticmethod
    def __get_quarter_string(date_string):
        date = pd.to_datetime(date_string)

        quarter = StockBitQuery.__get_quarter(date.month)
        year = date.year

        if quarter == 0:
            quarter = 4
            year -= 1

        response = "Q" + str(quarter) + " " + str(year)
        return response

    @staticmethod
    def __get_quarter(month):
        return (month - 1) // 3
