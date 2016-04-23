
# create python can read the order and proflie the returns.

# this can be use test strategy.

#python market_sim.py [start_money] [order.csv] [values.cvs]

#wiki: http://wiki.quantsoftware.org/index.php?title=CompInvesti_Homework_3#What_to_expect_when_you_turn_in_your_assignment_.28Coursera.29


# order format:
# 2008, 12, 3, AAPL, BUY, 130

# output is each day of the price.
import sys
import pandas as pd
import numpy as np
import math
import copy
import QSTK.qstkutil.qsdateutil as du
import datetime as dt
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkstudy.EventProfiler as ep


debug = False

def get_symbol_list_from_order(order_array):
    syms = {}
    for x in order_array:
        syms[x[3]] = 1

    return syms.keys()

def order_executable(order, date):
    if date.year >= order[0] and date.month >= order[1] and date.day >= order[2]:
        return True
    else:
        return False

def calc_value(stock_hold, df_close, date_i):
    value = 0;

    for sym,vol in stock_hold.iteritems():
        close_price = df_close[sym].ix[date_i]
        value += close_price * vol
    return value


def do_sim(init_money, order_array, values_array):

    # checking the order files, and find out what the max date and min date.
    order_array.sort()

    symbols = get_symbol_list_from_order(order_array)

    dt_start = dt.datetime(order_array[0][0], order_array[0][1], order_array[0][2]);
    dt_end = dt.datetime(order_array[-1][0], order_array[-1][1], order_array[-1][2]);
    dt_end += dt.timedelta(days=1)

    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt.timedelta(hours=16))
    dataobj = da.DataAccess('Yahoo')

    ls_keys = ['close'] #['open', 'high', 'low', 'close', 'volume', 'actual_close']
    ldf_data = dataobj.get_data(ldt_timestamps, symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))

    for s_key in ls_keys:
        d_data[s_key] = d_data[s_key].fillna(method='ffill')
        d_data[s_key] = d_data[s_key].fillna(method='bfill')
        d_data[s_key] = d_data[s_key].fillna(1.0)



    stock_hold = {}
    money_hold = init_money
    order_i = 0
    order_max = len(order_array)
    df_close = d_data['close']

    for date_i in range(len(ldt_timestamps)):
        date = ldt_timestamps[date_i]
        if order_i < order_max:
            while order_i < order_max and order_executable(order_array[order_i], date):
                if debug:
                    print "execute able : ", date, order_array[order_i]
                order = order_array[order_i]
                sym,action,amount = order[3],order[4],order[5]
                close_price = df_close[sym].ix[date_i]
                if action == "Buy":
                    if debug:
                        print "buy %d", amount
                    money_hold -= close_price * amount
                    if sym in stock_hold:
                        stock_hold[sym] += amount
                    else:
                        stock_hold[sym] = amount
                    if debug:
                        print "stock hold: ", stock_hold
                        print "money:", money_hold
                elif action == "Sell":
                    if sym in stock_hold:
                        stock_hold[sym] -= amount
                    else:
                        stock_hold[sym] = -amount
                    money_hold += close_price * amount

                    if debug:
                        print "sell"
                        print "stock hold: ", stock_hold
                        print "money:", money_hold

                order_i += 1
        # print today's value.
        
        values_array.append((date.year, date.month, date.day, money_hold + calc_value(stock_hold, df_close, date_i)))





def main():
    print len(sys.argv)
    if len(sys.argv) != 4:
        print "wrong argument.";
        return;

    init_money = int(sys.argv[1])
    order_file = sys.argv[2]
    result_file = sys.argv[3]
    values = []

    orders = np.loadtxt(order_file, delimiter=',', dtype='i4,i2,i2,S10,S4,i')
    do_sim(init_money, orders, values);
    np.savetxt(result_file, values, delimiter=',',fmt='%i')

if __name__ == '__main__':
    main();

