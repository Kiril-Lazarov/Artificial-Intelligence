import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def overview(dataset):
    start_time, end_time = dataset.time.values[0], dataset.time.values[-1]
    time_difference = pd.to_datetime(dataset.time).iloc[-1] - pd.to_datetime(dataset.time).iloc[0]
    total_minutes = int(str(time_difference).split(' ')[2].split(':')[0]) * 60 + int(str(time_difference).split(' ')[2].split(':')[1]) + 1
    low_price, high_price = dataset.price.min(), dataset.price.max()
    average_price = (dataset.price.values.max() + dataset.price.values.min())/2
    max_price_difference = dataset.price.values.max() - dataset.price.values.min()
    average_price_movement = max_price_difference / average_price * 100
    transactions_count = dataset.id.values[-1] - dataset.id.values[0]
    total_buy_qty, total_sell_qty = sum(dataset.buy_qty.values), sum(dataset.sell_qty.values)
    total_traded_quantity = total_buy_qty + total_sell_qty
    
    overview_msg = f'Start time: {start_time}\n' \
                   f'End time: {end_time}\n' \
                   f'Time duration: {time_difference} hours\n' \
                   f'Time duration in minutes: {total_minutes}\n' \
                   f'High price: {high_price}\n' \
                   f'Low price: {low_price}\n' \
                   f'Average price: {average_price}\n' \
                   f'Maximum price difference: {max_price_difference:.2f}\n' \
                   f'Maximum price change relative to the arithmetic mean price: {average_price_movement:.2f}%\n' \
                   f'Total transactions count: {transactions_count}\n' \
                   f'Average number of transactions per minute: {transactions_count/total_minutes:.2f}\n' \
                   f'Total buy quantity: {total_buy_qty:.5f} BTC\n' \
                   f'Total sell quantity: {total_sell_qty:.5f} BTC\n' \
                   f'Total traded quantity: {total_traded_quantity:.5f} BTC\n' \
                   f'Average traded quantity per transaction: {total_traded_quantity/transactions_count:.6f} BTC'
    return overview_msg

def print_time_diferences(dataset_time_column, max_index = 10):
    for i in range(1, len(dataset_time_column[:max_index])):
        if i == 1:
            print(i-1,dataset_time_column.values[i-1])
        diff = pd.to_datetime(dataset_time_column).iloc[i] - pd.to_datetime(dataset_time_column).iloc[i-1]
        print(i,dataset_time_column.values[i], diff)

def plot_feature_over_time(dataset, feature_name, ylim = None, draw_lines = None):
    dataset.time = pd.to_datetime(dataset.time)

    plt.plot(dataset.time, dataset[feature_name])
    
    feature_name = feature_name[0].upper() + feature_name[1:] 
    
    plt.xlabel('Time')
    plt.ylabel(f'{feature_name}')
    
    if ylim is not None:
        plt.ylim(ylim[0], ylim[1])
        
    if draw_lines is not None:        
      
        color = 'grey'
        linestyle = '-'
        
        start_segment = pd.to_datetime(draw_lines[0])
        end_segment = pd.to_datetime(draw_lines[1])
        
        plt.axvspan(start_segment, end_segment, facecolor='lightgray', alpha=0.3)     
        
        plt.axvline(x = start_segment, color = color, linestyle = linestyle)
        plt.axvline(x = end_segment, color = color, linestyle = linestyle)
 
   
    plt.title(f'{feature_name} vs Time')
    plt.xticks(rotation=45)
    plt.show()
    
def get_transaction_counts_diffs(transactions_id):
    id_diffs = []
    
    for i in range(1, len(transactions_id)):
        d = transactions_id[i]-transactions_id[i-1]
        id_diffs.append(d)
 
    mean_value = float(f'{np.array(id_diffs).mean():.2f}')
    
    # Adding the mean value of the array to the zero index to preserve the original length of the input parameter.
    id_diffs.insert(0, mean_value)
    return np.array(id_diffs)

def plot_one_above_another(dataset1, dataset2, time_data_set, start_index, end_index, messages, draw_lines = None, ylog = False):

    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
  
    # Plot 1
    ax1.plot(time_data_set[start_index: end_index], dataset1[start_index: end_index], color='red')
    ax1.set_ylabel(messages['top_y_label'])

    # Plot 2
    ax2.plot(time_data_set[start_index: end_index], dataset2[start_index: end_index], color='blue')
    
    ax2.set_ylabel(messages['bottom_y_label'])
    ax2.set_xlabel(messages['x_label'])
    
    if draw_lines is not None:
        color = 'grey'
        linestyle = '-'
        
        start_segment = pd.to_datetime(draw_lines[0])
        end_segment = pd.to_datetime(draw_lines[1])
        
        ax1.axvspan(start_segment, end_segment, facecolor='lightgray', alpha=0.3)
        ax2.axvspan(start_segment, end_segment, facecolor='lightgray', alpha=0.3)
        
        ax1.axvline(x = start_segment, color = color, linestyle = linestyle)
        ax1.axvline(x = end_segment, color = color, linestyle = linestyle)
        ax2.axvline(x = start_segment, color = color, linestyle = linestyle)
        ax2.axvline(x = end_segment, color = color, linestyle = linestyle)
        
    fig.suptitle(messages['title']) 
    
    if ylog:
        plt.yscale("log")
        
    plt.xticks(rotation=45)
    fig.tight_layout()
    plt.show()
        
def group_by_time_intervals(dataset, time_interval = 1, balance_coeff = False, mean_price = False, value_to_replace = 0.0000001,columns=None):
    if columns is None:
        dataset = dataset[['id', 'time','price', 'buy_qty', 'sell_qty', 'bids_0_99', 'asks_0_99']]
    else:
        dataset = dataset[['id', 'time','price', 'buy_qty', 'sell_qty', columns[0], columns[1]]]
        
    new_dataset_dict = {'id': [],
                   'time': [],     
                   'price': [],
                   'buy_qty': [],
                   'sell_qty': [],
                   'diff': [],
                   'bids_0_99': [],
                   'asks_0_99': [],
                   }
    start_index = 0
    end_index = start_index + time_interval * 5
    
    if columns is not None:
        new_dataset_dict[columns[0]] = new_dataset_dict.pop('bids_0_99')
        new_dataset_dict[columns[1]] = new_dataset_dict.pop('asks_0_99')
        
    if balance_coeff:
        del new_dataset_dict['diff']
  
    for i in range(dataset.index.stop//(time_interval*6)):
        bid_sum = dataset[start_index: end_index].buy_qty.sum()
        ask_sum = dataset[start_index: end_index].sell_qty.sum()
        
        if columns is None:
            waiting_bids = dataset[start_index:end_index].bids_0_99.mean()
            waiting_asks = dataset[start_index:end_index].asks_0_99.mean()
            
        else:
            waiting_bids = dataset[start_index:end_index][columns[0]].mean()
            waiting_asks = dataset[start_index:end_index][columns[1]].mean()
        
        if mean_price:
            price = dataset[start_index: end_index].price.sum()
            new_dataset_dict['price'].append(price)
        else:
            new_dataset_dict['price'].append(dataset.price[end_index])
            
        new_dataset_dict['id'].append(dataset.id[end_index])
        new_dataset_dict['time'].append(dataset.time[end_index])
        new_dataset_dict['buy_qty'].append(bid_sum)
        new_dataset_dict['sell_qty'].append(ask_sum)
        
        if not balance_coeff:            
            new_dataset_dict['diff'].append(ask_sum - bid_sum)
            
        if columns is None:
            new_dataset_dict['bids_0_99'].append(waiting_bids)
            new_dataset_dict['asks_0_99'].append(waiting_asks)
        
        else:
            new_dataset_dict[columns[0]].append(waiting_bids)
            new_dataset_dict[columns[1]].append(waiting_asks)
            
        start_index = end_index + 1
        end_index += 6
        
    new_dataset = pd.DataFrame(new_dataset_dict)
        
    if balance_coeff:
        new_dataset = replace_zeros(new_dataset, value_to_replace)
        new_dataset = add_balance_coeff(new_dataset,columns = columns)
        
    return new_dataset

def get_corr_coeff(dataset):
    return np.corrcoef(dataset['price'].values, dataset['diff'].values)[0][1]

def calc_correlations_by_time_interval(dataset, 
                                       metric, 
                                       range_intervals_in_minutes= [1,30], 
                                       dataset_size = None, 
                                       exclude_equal_prices=False, 
                                       mean_price = False,
                                       columns = None,
                                       exclude_waiting_volumes= False):
    
    range_intervals_in_minutes[1] += 1
    correlations_data = {
        'time_interval_in_minutes':[],
        'correlation_coefficient': []
    }
    if dataset_size is not None:
        dataset = dataset[:dataset_size]
        
    for time_interval in range(range_intervals_in_minutes[0], range_intervals_in_minutes[1]):
        
        if metric == 'balance_coeff':
            df = group_by_time_intervals(dataset, time_interval=time_interval, balance_coeff = True, mean_price=mean_price, columns=columns)
            
        else:
            df = group_by_time_intervals(dataset, time_interval=time_interval,mean_price=mean_price)
            
        if metric == 'corr_coeff':
            coeff = get_corr_coeff(df)
            
        elif metric == 'balance_coeff':
            df = add_balance_coeff(df, columns,exclude_waiting_volumes)
            
            if exclude_equal_prices:
                df = add_is_equal_prices(df, columns)
                
            coeff = get_balance_percentage(df,exclude_equal_prices= exclude_equal_prices)
            
        correlations_data['time_interval_in_minutes'].append(time_interval)
        correlations_data['correlation_coefficient'].append(coeff)
        
    correlations_data = pd.DataFrame(correlations_data)
    correlations_data = correlations_data.set_index(['time_interval_in_minutes'])
    
    return correlations_data

def plot_correlations(correlations_set, title):
    plt.plot(correlations_set)
    plt.title(title)
    plt.xlabel('Time interval in minutes')
    plt.ylabel('Correlation coefficient')
    plt.show()
    
def plot_direction(dataset, direction):
    
    direction_name = direction[0][:4]

    direction_name = direction_name[0].upper() + direction_name[1:]
 
    green_hex_colors = ['#456944', '#2e9d2b','#23cf1e','#40f13a','#91fd8d']
    red_hex_colors = ['#860f0f','#c21717','#ea2828','#f56868','#f9b2b2']

    colors = green_hex_colors if direction_name == 'Bids' else red_hex_colors
    
    for i in range(len(direction)):
        plt.plot(dataset.time, dataset[direction[i]], color = colors[i], label = f'{direction[i]}')
        
    plt.title(f'{direction_name} Volumes of Pending Orders vs Time')
    
    plt.xlabel('Time')
    plt.ylabel('Volume in BTC')
    
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.xticks(rotation=45)
    
    plt.show()
    
def plot_volumes(dataset):
    vol_columns = dataset.columns[5:]
    
    bids = vol_columns[:5]
    asks = vol_columns[5:]
    
    plot_direction(dataset, bids)
    plot_direction(dataset, asks)  
    
def plot_ranges(dataset):
    plt.plot(dataset.top_80_99, color='purple', label= '100 prices above')
    plt.plot(dataset.price, color='green', label='Current price')
    plt.plot(dataset.bottom_80_99, color='red', label='100 prices below')
    
    plt.xlabel('Index')
    plt.ylabel('Price')
    
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    
    plt.xticks(rotation=45)
    
    plt.show()
    
# Calculates the balance coefficient, checks if its prediction is correct, and adds the two values as new columns to the provided dataset.
def add_balance_coeff(dataset, columns=None, exclude_waiting_volumes= False):
    
    # The first value is `unknown` as we don`t know the price before the zero index in the dataset
    boolean_massive = ['unknown']
    
    if columns is None:
        alpha = dataset.sell_qty * dataset.bids_0_99
        beta = dataset.buy_qty * dataset.asks_0_99
        
    else:
        alpha = dataset.sell_qty * dataset[columns[0]]
        beta = dataset.buy_qty * dataset[columns[1]]
        
    B = alpha/beta
    
    # Add balance coefficient to dataset if
    if exclude_waiting_volumes:
        B = dataset.sell_qty / dataset.buy_qty
    
    dataset['balance_coeff'] = B
    
    for index, row in dataset.iterrows():
    
        curr_price = row.price       
    
        bal_coef = row.balance_coeff
        
        if index != 0:
            # Get previous price
            previous_price = dataset.price.values[[index-1][0]]
            
            if curr_price > previous_price:
                if bal_coef > 1:
                    boolean_massive.append(True)
                else:
                    boolean_massive.append(False)
                    
            elif curr_price == previous_price:
                if bal_coef == 1:
                    boolean_massive.append(True)
                else:
                    boolean_massive.append(False)
                    
            elif curr_price < previous_price:
                if bal_coef < 1:
                    boolean_massive.append(True)
                else:
                    boolean_massive.append(False)
  
    dataset.loc[:, 'match_balance_coeff'] = np.array(boolean_massive)
    
    return dataset

def get_balance_percentage(dataset, exclude_equal_prices = False):
    if exclude_equal_prices:
        reduced_dataset = dataset[dataset.is_previous_equals == 'False'] 
        return reduced_dataset.match_balance_coeff.value_counts()['True']/ (len(reduced_dataset) -1)
    
    return dataset.match_balance_coeff.value_counts()['True']/ (len(dataset) -1)

def replace_zeros(dataset, new_value):
    dataset.loc[dataset.buy_qty == 0, ['buy_qty']] = new_value
    dataset.loc[dataset.sell_qty == 0, ['sell_qty']] = new_value
    
    return dataset

def add_is_equal_prices(dataset,columns = None):
    boolean_massive = ['unknown']
    
    for index in range(len(dataset.price.values)):
        if index >0:
            if dataset.price.values[index] == dataset.price.values[index-1]:
                boolean_massive.append(True)
            else:
                boolean_massive.append(False)
                
    dataset.loc[:, 'is_previous_equals'] = np.array(boolean_massive)
    
    if columns is None:
        dataset = dataset[['id', 'time', 'price', 'is_previous_equals', 'buy_qty', 'sell_qty', 'bids_0_99', 'asks_0_99',
           'balance_coeff', 'match_balance_coeff']]
    else:
        dataset = dataset[['id', 'time', 'price', 'is_previous_equals', 'buy_qty', 'sell_qty', columns[0], columns[1],
           'balance_coeff', 'match_balance_coeff']]
    return dataset   

def get_equal_prices(dataset, range_intervals_in_minutes = [1,30]):
    data_dict = {
        'time_interval': [],
        'df_length' : [],
        'equal_prices_count':[]
    }
    
    range_intervals_in_minutes[1] += 1
    
    for time_interval in range(range_intervals_in_minutes[0], range_intervals_in_minutes[1]):
        df = group_by_time_intervals(dataset, time_interval = time_interval, balance_coeff = True)
        df = add_is_equal_prices(df)
        
        data_dict['time_interval'].append(time_interval)
        data_dict['df_length'].append(len(df)-1)
        
        if df.is_previous_equals.value_counts()['False'] != len(df.is_previous_equals) -1:     
            
            eq_prices = df.is_previous_equals.value_counts()['True']
            data_dict['equal_prices_count'].append(eq_prices)   
            
        else:
            data_dict['equal_prices_count'].append(0)
    
    return pd.DataFrame(data_dict)

def create_total_volumes_dataset(dataset):
    bids_list = list(dataset.columns[5:10])
    sum_bids_column_name = 'bids_' + '_'.join([bids_list[0][5], bids_list[-1].split('_')[2]])
    
    asks_list = list(dataset.columns[10:15])
    sum_asks_column_name = 'asks_' + '_'.join([asks_list[0][5], asks_list[-1].split('_')[2]])
    
    dataset[sum_bids_column_name] = 0
    dataset[sum_asks_column_name] = 0
    
    for index in range(len(bids_list)):
        dataset[sum_bids_column_name] += dataset[bids_list[index]]
        dataset[sum_asks_column_name] += dataset[asks_list[index]]
        
    new_dataset = dataset.drop(columns=bids_list + asks_list)
    
    return new_dataset

def show_volumes_means_by_level(dataset):
    for column_name, column_data in dataset.iteritems():
        if 'bids' in column_name or 'asks' in column_name:
            print(column_name,  round(column_data.mean(), 6))