from binance.client import Client
import os
import time

api_key = ''
api_secret = ''

client = Client(api_key, api_secret)

recent_trades_data = client.get_recent_trades(symbol='BTCEUR', limit=20)
last_recent_trades_id = recent_trades_data[-1]['id']
init_time = recent_trades_data[0]['time']



time.sleep(10)


def waiting_volumes_dispatcher(volumes_data, step = 100):
    sums_dict = {'bids': [], 'asks': []}

    for index in range(1, 6):
        down_limit = index - 1

        sums_dict['bids'].append(sum(float(data[1]) for data in volumes_data['bids'][down_limit * step: index * step]))
        sums_dict['asks'].append(sum(float(data[1]) for data in volumes_data['asks'][down_limit * step: index * step]))

    return sums_dict


def append_volumes_to_string(string, volumes_data_dict):
    string += ','
    string += ','.join(str(x) for x in volumes_data_dict['bids']) + ','
    string += ','.join(str(x) for x in volumes_data_dict['asks'])

    return string


def collecting_data_func(start_time, last_recent_trades_id=last_recent_trades_id):

    # Two days in milliseconds - this will be the time interval to collect the data
    time_duration = 172800000

    end_time = start_time + time_duration
    curr_time = time.time() * 1000

    start = time.time()

    while curr_time <= end_time:

        try:
            trades_data = list(reversed(client.get_recent_trades(symbol='BTCEUR', limit=200)))
        except:
            raise Exception('Fail to get trades_data')


        recent_bids = 0
        recent_asks = 0

        curr_time = trades_data[0]['time']
        trade_id = trades_data[0]['id']
        price = trades_data[0]['price']

        index = 0

        is_new_trades = False
        while trades_data[index]['id'] > last_recent_trades_id:
            is_new_trades = True
            # Get buy and sell waiting volumes
            try:
                waiting_volume_data = client.get_order_book(symbol='BTCEUR', limit=500)
            except:

                raise Exception('Fail to get waiting_volume_data')

            # Add recent trade volumes
            if trades_data[index]['isBuyerMaker']:
                recent_bids += float(trades_data[index]['qty'])

            else:
                recent_asks += float(trades_data[index]['qty'])

            index += 1
            
        # Rewrite the last trade id
        last_recent_trades_id = trades_data[0]['id']

        data = (',').join([str(trade_id), str(curr_time), str(price), str(recent_bids), str(recent_asks)])
        
        if is_new_trades:
            
            sums_dict = waiting_volumes_dispatcher(waiting_volume_data, step=20)
            data = append_volumes_to_string(data, sums_dict)

            with open('/home/MadmartiganKL/collecting_data_for_course_project/trade_data.csv', 'a') as file:

                file.write(f"\n{data}")

        time.sleep(10)
        curr_time = time.time() * 1000

    print('Done', curr_time - init_time, flush = True)
