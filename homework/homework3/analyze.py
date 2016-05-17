# ayalysis the values.
# python analysze.py values.csv \$SPX
# which compare with the benchmark index.
# and create charts.
# and other important values.





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

import matplotlib.pyplot as plt


# Plot the price history over the trading period.
# Your program should also output:
# Standard deviation of daily returns of the total portfolio
# Average daily return of the total portfolio
# Sharpe ratio (Always assume you have 252 trading days in an year. And risk free rate = 0) of the total portfolio
# Cumulative return of the total portfolio

def daily_ret(prices):
    ret = []

    for i in range(len(prices)):
        if i == 0:
            ret.append(0)
            continue
        t = float(prices[i]  - prices[i-1])/float(prices[i-1])
        ret.append(t)
    return ret;



def do_analysis(values, benchmark_sym):
    # first, needs figure out begin and end date.
    # then needs to take out benchmark values.
    # finnaly plot together.

    first_value = values[0]
    last_value = values[-1]
    dt_start = dt.datetime(first_value[0], first_value[1], first_value[2])
    dt_end = dt.datetime(last_value[0], last_value[1], last_value[2])
    dt_end += dt.timedelta(days=1)
    symbols = [benchmark_sym]
    dt_timeofday = dt.timedelta(hours=16)

    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday);

    dataobj = da.DataAccess('Yahoo')
    ls_keys =  ['close']#['open', 'high', 'low', 'close', 'volume', 'actual_close']
    ldf_data = dataobj.get_data(ldt_timestamps, symbols, ls_keys, verbose=True)

    d_data = dict(zip(ls_keys, ldf_data))

    # print d_data

    for s_key in ls_keys:
        d_data[s_key] = d_data[s_key].fillna(method='ffill')
        d_data[s_key] = d_data[s_key].fillna(method='bfill')
#        d_data[s_key] = d_data[s_key].fillna(1.0)


    benchmark = d_data['close'][benchmark_sym];
#    print normalized_benchmark[0];
    factory = values[0][3] / benchmark[0];

    # normalized to same factory to fund value.
    normalized_benchmark = benchmark * factory

    normalized_values = map(lambda x: x[3], values)

    plt.clf()
    plt.plot(ldt_timestamps, normalized_benchmark, "r",
             ldt_timestamps, normalized_values)
    plt.legend([ benchmark_sym, 'fund value'])
    plt.ylabel('Fund Value')
    plt.xlabel('Date')
    plt.savefig('analysis.pdf', format='pdf')

    daily_ret_my = daily_ret(normalized_values)
    daily_ret_bm = tsu.daily(d_data['close'][benchmark_sym])

    sharp_ratio_my = tsu.get_sharpe_ratio(daily_ret_my)
    sharp_ratio_bm = tsu.get_sharpe_ratio(daily_ret_bm)[0]
    # why -1 and +1 ?
    total_ret_my =  (float(normalized_values[-1]) / float(normalized_values[0]))

    total_ret_bm = float(benchmark[-1] / float(benchmark[0]))

    stddev_my = np.std(daily_ret_my)
    stddev_bm = np.std(daily_ret_bm)
    avg_my  = np.average(daily_ret_my)
    avg_bm  = np.average(daily_ret_bm)

    print "Details of the Performance of the portfolio :"
    print ""
    print "Data Range :  %s  to  %s" % (ldt_timestamps[0], ldt_timestamps[-1])
    print ""
    print "Sharpe Ratio of Fund : %f" % sharp_ratio_my
    print "Sharpe Ratio of $SPX : %fy" % sharp_ratio_bm
    print ""
    print "Total Return of Fund :  %f" % total_ret_my
    print "Total Return of $SPX : %f" % total_ret_bm
    print ""
    print "Standard Deviation of Fund :  %f" % stddev_my
    print "Standard Deviation of $SPX : %f" % stddev_bm
    print ""
    print "Average Daily Return of Fund :  %f" % avg_my
    print "Average Daily Return of %s : %f" % (benchmark_sym, avg_bm)






if __name__ == '__main__':
    value_file = sys.argv[1];
    benchmark_sym = sys.argv[2];

    values =  np.loadtxt(value_file, delimiter=',',dtype='i4,i2,i2,i')
    do_analysis(values, benchmark_sym)

