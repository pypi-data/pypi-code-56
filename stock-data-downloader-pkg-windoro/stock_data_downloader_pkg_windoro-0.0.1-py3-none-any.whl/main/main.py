from stockdatadownloader.fetcher.Idx import Idx
from stockdatadownloader.fetcher.StockBitFetcher import StockBitFetcher

from stockdatadownloader.query.StockBitQuery import StockBitQuery

if __name__ == "__main__":
    # Idx().download()
    # stocks = Idx.get_stocks()
    stocks = ['BBRI']

    # fetcher = StockBitFetcher('', '')
    # fetcher.download_fundamental(stocks)
    # fetcher.download_price(stocks, '2010-01-01', '2020-01-01')
    # print(StockBitQuery.query_data_fundamental(stocks[0], '2016-12-12', 'Laba Kotor'))
    # print(StockBitQuery.query_data_price(stocks[0], '2019-12-17', 'high'))
