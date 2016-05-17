# QSTK Imports
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da

# Third Party Imports
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sys

import matplotlib.pyplot as plt

def boll_seq(start_date, end_date, symbols, peroid_len, do_plot=False, plt_file="Bolling.pdf"):

    print "Calc bollinger %s from %s to %s" % (symbols, start_date, end_date)

    dt_timeofday = dt.timedelta(hours = 16);
    ldt_timestamps = du.getNYSEdays(start_date, end_date, dt_timeofday)
    c_dataobj = da.DataAccess('Yahoo');
    ls_keys = ['close'];
    ldf_data = c_dataobj.get_data(ldt_timestamps, symbols, ls_keys);
    d_data = dict(zip(ls_keys, ldf_data));
    na_price = d_data['close'].values

    rolling = pd.DataFrame(na_price).rolling(window=peroid_len)

    avg = rolling.mean()
    std = rolling.std();

    bollinger_val = (na_price - avg) / std

    print bollinger_val

    if do_plot:
        plt.clf();
        # plt.plot(ldt_timestamps, na_price, "r",
        #          ldt_timestamps, avg+std, "b",
        #          ldt_timestamps, avg-std, "b");
        plt.plot(ldt_timestamps, bollinger_val, "r")
        plt.legend(['Bolling']);
        plt.ylabel('Bolling');
        plt.xlabel('Date')
        plt.savefig(plt_file, format='pdf')
        # plt.show()              # 

    return zip(ldt_timestamps, bollinger_val[0])

def boll_seq_df(df_close_price, peroid_len):
    rolling = pd.DataFrame(df_close_price).rolling(window = peroid_len)

    avg = rolling.mean();
    std = rolling.std();

    bollinger_val = (df_close_price - avg) / std
    return bollinger_val
    
def filter_event(bol_mark, bol_spy):
    l = len(bol_mark);
    ret = [];
    for i in xrange(l):
        if i == 0:
            continue
            
        if bol_mark[i] <= -2.0 and bol_mark[i-1] >= -2.0 and bol_spy[i] >= 1.0:
            ret.push(i)
    return ret;

def main():
    if len(sys.argv) != 5:
        print "usage: calc_boll goog 1-1-2010 12-31-2012 20"
        print "argv", len(sys.argv)
        return

    symbol = sys.argv[1]
    start = dt.datetime.strptime(sys.argv[2], '%m-%d-%Y')
    end = dt.datetime.strptime(sys.argv[3], '%m-%d-%Y')
    peroid = int(sys.argv[4])
    bol = boll_seq(start, end, [symbol], peroid, do_plot=True)
    # for i in xrange(len(bol)):
    #     print bol[i]
    bol_spy = boll_seq(start, end, ["SPY"], peroid, do_plot=True, plt_file="SPY.pdf")

    events = filter_event(bol, bol_spy)

    print events

    


if __name__ == '__main__':
    main();