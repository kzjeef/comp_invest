import math


def daily_sharp_ratio(mean_daily_return, daily_std_div) :
    k = math.sqrt(250)
    return k * mean_daily_return / daily_std_div

print daily_sharp_ratio(0.005, 0.04)

