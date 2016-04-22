# QSTK Imports
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da

# Third Party Imports
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def simulate(start_date, end_date, symbols, allocations):
    # this function should return: vol, daily_ret, sharpe, cum_ret
    dt_timeofday = dt.timedelta(hours=16);

    ldt_timestamps = du.getNYSEdays(start_date, end_date, dt_timeofday)

    c_dataobj = da.DataAccess('Yahoo');
    ls_keys = ['close'];
    ldf_data = c_dataobj.get_data(ldt_timestamps, symbols, ls_keys);
    d_data = dict(zip(ls_keys, ldf_data));
    na_price = d_data['close'].values
    na_normalized_price = na_price / na_price[0, :]
    na_rets = na_normalized_price
    day_rets = na_rets * allocations
    day_prof_accum = np.sum(day_rets, axis=1)
    day_prof_rets = day_prof_accum.copy()
    tsu.returnize0(day_prof_rets)
    cum_ret = day_prof_accum[-1]
    avg_daily_ret = np.average(day_prof_rets)
    std_ret = np.std(day_prof_rets)
    sharpe = np.sqrt(252) * avg_daily_ret / std_ret

    return (std_ret, avg_daily_ret, sharpe, cum_ret)

def best_prof(start_date, end_date, symbols):

    best_sharp = -1;
    best_alloc = []
    for i in xrange(0,11):
        for j in xrange(0, 11):
             for k in xrange(0, 11):
                  for l in xrange(0, 11):
                      if (i + j + k + l) != 10:
                          continue
                      alloc = [i/10.0, j/10.0, k/10.0, l/10.0];
                      r, a, sharpe, cum_ret = simulate(start_date, end_date, symbols, alloc)
                      if sharpe > best_sharp:
                           best_sharp = sharpe;
                           best_alloc = alloc

    print best_sharp
    print best_alloc
                       


if __name__ == '__main__':
#    print best_prof(        dt.datetime(2011, 1,  1),        dt.datetime(2011,12, 31),       ['AAPL', 'GOOG', 'IBM', 'MSFT'])
#    print simulate(        dt.datetime(2010, 1,  1),        dt.datetime(2010,12, 31),        ['AXP', 'HPQ', 'IBM', 'HNZ'],         [0.0, 0.0, 0.0, 1.0]);

#     print best_prof(        dt.datetime(2010, 1,  1),        dt.datetime(2010,12, 31),         ['AXP', 'HPQ', 'IBM', 'HNZ']);
#    print best_prof(        dt.datetime(2010, 1,  1),        dt.datetime(2010,12, 31),         ['BRCM', 'TXN', 'IBM', 'HNZ'])

#    print best_prof(        dt.datetime(2010, 1,  1),        dt.datetime(2010,12, 31),         ['BRCM', 'TXN', 'IBM', 'HNZ'])

#    print best_prof(        dt.datetime(2010, 1,  1),        dt.datetime(2010,12, 31),         ['C', 'GS', 'IBM', 'HNZ'])
#    print best_prof(        dt.datetime(2011, 1,  1),        dt.datetime(2011,12, 31),        ['AAPL', 'GOOG', 'IBM', 'MSFT'])

    print best_prof(        dt.datetime(2010, 1,  1),        dt.datetime(2010,12, 31),        ['C', 'GS', 'IBM', 'HNZ'])    

              
             
                  
    