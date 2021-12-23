from datetime import datetime
from vnpy.trader.constant import Exchange, Interval
from vnpy.trader.datafeed import get_datafeed
from vnpy.trader.object import HistoryRequest
from vnpy.trader.database import get_database
from typing import List
from vnpy.trader.object import BarData
from vnpy_coinapi import CoinapiDatafeed
from​ ​coinapi-sdk.data-api.python-rest.coinapi_rest_v1​.​restapi​ ​import​ ​CoinAPIv1
from vnpy.trader.setting import SETTINGS

# 获取symbols
test_key = SETTINGS["datafeed.password"]
api​ ​=​ ​CoinAPIv1​(​test_key​)

symbols​ ​=​ ​api​.​metadata_list_symbols​()
bar_req = HistoryRequest(
        symbol="CU888",
        exchange=Exchange("DERIBIT"),
        start=datetime(2016, 1, 1),
        end=datetime(2021, 12, 20),
        interval=Interval.DAILY
    )

# 获取数据服务实例
#datafeed = get_datafeed()
datafeed = CoinapiDatafeed()

# 获取k线历史数据
bar_data = datafeed.query_bar_history(bar_req)

# 获取数据库实例
database = get_database()

# 将k线数据存入数据库
database.save_bar_data(bar_data)