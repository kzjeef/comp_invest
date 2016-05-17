

import pandas as pd
import numpy as np
import math
import copy
import QSTK.qstkutil.qsdateutil as du
import datetime as dt
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkstudy.EventProfiler as ep

import calc_boll as cb

import csv

def find_events(ls_symbols, d_data, event_callback):
    df_close = d_data['close']
    ts_market = df_close['SPY']

    bolling_val = cb.boll_seq_df(df_close, 20)

    df_events = copy.deepcopy(df_close)
    df_events = df_events * np.NAN

    ldt_timestamps = df_close.index


    for s_sym in ls_symbols:
        if s_sym == "SPY":
            continue
        for i in range(1, len(ldt_timestamps)):
            f_today_bolling = bolling_val[s_sym].ix[ldt_timestamps[i]]
            f_yst_bolling = bolling_val[s_sym].ix[ldt_timestamps[i-1]]
            f_mrkt_today_bolling = bolling_val['SPY'].ix[ldt_timestamps[i]]

#            print "%f %f %f" % (f_today_bolling, f_yst_bolling, f_mrkt_today_bolling)

            if f_today_bolling < -2.0 and f_yst_bolling >= -2.0 and f_mrkt_today_bolling >= 1.4:
                df_events[s_sym].ix[ldt_timestamps[i]] = 1
                event_callback(ldt_timestamps[i], s_sym)

    return df_events


def make_event_order_generator(filename):
    # create the file.
    order_array = []
    def write_order(timestamp, symbol):
        order_array.append([timestamp.year, timestamp.month, timestamp.day,
                            symbol, "BUY", 100])
        sell_date = du.getNYSEoffset(timestamp, 5)
        order_array.append([sell_date.year, sell_date.month, sell_date.day,
                            symbol, "SELL", 100])
    def dumper():
        order_array.sort()
#        print "saving: ", order_array
        with open(filename, 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter=',');
            for row in order_array:
                writer.writerow(row)


    return write_order, dumper


if __name__ == '__main__':
    dt_start = dt.datetime(2008, 1, 1)
    dt_end = dt.datetime(2009, 12, 31)
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt.timedelta(hours=16))

    dataobj = da.DataAccess('Yahoo')
    ls_symbols = dataobj.get_symbols_from_list('sp5002012')
    ls_symbols.append('SPY')


    ls_keys = ['close']
    ldf_data = dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))

    for s_key in ls_keys:
        d_data[s_key] = d_data[s_key].fillna(method='ffill')
        d_data[s_key] = d_data[s_key].fillna(method='bfill')
        d_data[s_key] = d_data[s_key].fillna(1.0)

    gen_order_callback, saver = make_event_order_generator('orders.txt')

    df_events = find_events(ls_symbols, d_data, gen_order_callback)
    saver();

    print "Creating Study"
#    print "df_events: ", df_events
#    print "d_data", d_data
    ep.eventprofiler(df_events, d_data, i_lookback=20, i_lookforward=20,
                s_filename='Bolling_events.pdf', b_market_neutral=True, b_errorbars=True,
                s_market_sym='SPY')

#     ls_symbols_2012 = dataobj.get_symbols_from_list('sp5002012');
#     ls_symbols_2012.append('SPY')
#     ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
#     ldf_data2 = dataobj.get_data(ldt_timestamps, ls_symbols_2012, ls_keys);
#     d_data2 = dict(zip(ls_keys, ldf_data2))

#     for s_key in ls_keys:
#         d_data2[s_key] = d_data2[s_key].fillna(method='ffill')
#         d_data2[s_key] = d_data2[s_key].fillna(method='bfill')
#         d_data2[s_key] = d_data2[s_key].fillna(1.0)


# ##    clear_data(ls_keys, ldf_data2)
#     df_events2 = find_events(ls_symbols_2012, d_data2)
#     ep.eventprofiler(df_events2, d_data2, i_lookback=20, i_lookforward=20,
#                 s_filename='HomeWork2012.pdf', b_market_neutral=True, b_errorbars=True,
#                 s_market_sym='SPY')


    
