from datetime import datetime
from vnpy.trader.constant import Exchange, Interval
from vnpy.trader.datafeed import get_datafeed
from vnpy.trader.object import HistoryRequest
from vnpy.trader.database import get_database
from typing import List
from vnpy.trader.object import BarData
from vnpy_coinapi import CoinapiDatafeed
from coinapi_rest_v1.restapi import CoinAPIv1
from vnpy.trader.setting import SETTINGS

# 获取symbols
test_key = SETTINGS["datafeed.password"]
api = CoinAPIv1(test_key)
param = {"filter_symbol_id": ['DERIBIT_OPT_BTC_USD_1603', 'DERIBIT_OPT_BTC_USD_1606', 'DERIBIT_OPT_BTC_USD_1609', 'DERIBIT_OPT_BTC_USD_1612', 
                                'DERIBIT_OPT_BTC_USD_1703', 'DERIBIT_OPT_BTC_USD_1706', 'DERIBIT_OPT_BTC_USD_1709', 'DERIBIT_OPT_BTC_USD_1712',
                                'DERIBIT_OPT_BTC_USD_1803', 'DERIBIT_OPT_BTC_USD_1806', 'DERIBIT_OPT_BTC_USD_1809', 'DERIBIT_OPT_BTC_USD_1812',
                                'DERIBIT_OPT_BTC_USD_1903', 'DERIBIT_OPT_BTC_USD_1906', 'DERIBIT_OPT_BTC_USD_1909', 'DERIBIT_OPT_BTC_USD_1912',
                                'DERIBIT_OPT_BTC_USD_2003', 'DERIBIT_OPT_BTC_USD_2006', 'DERIBIT_OPT_BTC_USD_2009', 'DERIBIT_OPT_BTC_USD_2012',
                                'DERIBIT_OPT_BTC_USD_2103', 'DERIBIT_OPT_BTC_USD_2106', 'DERIBIT_OPT_BTC_USD_2109', 'DERIBIT_PERP_BTC_USD'
                                ]}
symbols = api.metadata_list_symbols(param)

# 获取数据服务实例
#datafeed = get_datafeed()
datafeed = CoinapiDatafeed()

# 获取数据库实例
database = get_database()

# 下载历史数据
for symbol_dict in symbols:

    # 构建请求结构体
    bar_req = HistoryRequest(
            symbol=symbol_dict['symbol_id'],
            exchange=Exchange("DERIBIT"),
            start=datetime(2016, 1, 1),
            end=datetime(2021, 12, 20),
            interval=Interval.DAILY
        )

    # 获取k线历史数据
    bar_data = datafeed.query_bar_history(bar_req)

    # 将k线数据存入数据库
    database.save_bar_data(bar_data)
    print('symbol_id: ', symbol_dict['symbol_id'], ' count: ', len(bar_data))