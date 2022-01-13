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
contracts = []
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
    bars_data = datafeed.query_bar_history(bar_req)

    # 将k线数据存入数据库
    database.save_bar_data(bars_data)
    print('symbol_id: ', symbol_dict['symbol_id'], ' count: ', len(bars_data))

    # 构建合约数据
    contract_dict = {}
    symbol_split = symbol_dict['smybol_id'].split('_')
    contract_dict['symbol'] = symbol_split[2] + '_' + symbol_split[3] + '_' + symbol_split[4] + '_' + symbol_split[5] + '_' + symbol_split[6]
    contract_dict['exchange'] = Exchange(symbol_dict['exchange_id'])
    if symbol_split[4] == 'C':
        contract_dict['name'] = 'Bitcoin' + '_' + symbol_split[3] + '_' + symbol_split[4] + '_' + symbol_split[5] + '_' + 'CALL'
    else:
        contract_dict['name'] = 'Bitcoin' + '_' + symbol_split[3] + '_' + symbol_split[4] + '_' + symbol_split[5] + '_' + 'PUT'
    contract_dict['product'] = symbol_dict['symbol_type']
    contract_dict['size'] = symbol_dict['option_contract_unit']
    contract_dict['pricetick'] = symbol_dict['price_precision']
    contract_dict['min_volume'] = symbol_dict['size_precision']
    contract_dict['stop_supported'] = True
    contract_dict['net_position'] = False
    contract_dict['history_data'] = True
    contract_dict['option_strike'] = symbol_dict['option_strike_price']
    contract_dict['option_underlying'] = symbol_split[2] + '_' + symbol_split[3] + '_' + symbol_split[4]
    if symbol_dict['option_type_is_call'] == True:
        contract_dict['option_type'] = 'CALL'
    else:
        contract_dict['option_type'] = 'PUT'
    contract_dict['option_listed'] = datetime.datetime.strptime(symbol_dict['data_start'], '%Y-%m-%d')
    contract_dict['option_expiry'] = datetime.datetime.strptime(symbol_dict['option_expiration_time'], '%Y-%m-%dT%h:%m:%sZ')
    contract_dict['option_portfolio'] = ""
    contract_dict['option_index'] = ""
    contracts.append(contract_dict)
database.save_contract_data(contracts)
print('contracts count: ', len(contracts))