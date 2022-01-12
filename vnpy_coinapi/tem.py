contracts = []
for symbol_dict in symbols:
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
