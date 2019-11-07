def make_text(ts,sims,tf1,tf2,tf3,ltsm,mr,sl,sp):

    if tf1==tf2==tf3==0:
        trends = 'no trend following'
    else:
        trend_list = [x for x in [tf1,tf2,tf3] if x!=0]
        trends = f'trend following over {trend_list[0]} days'
        if len(trend_list)>1:
            for t in trend_list[1:]:
                trends = trends + f', {t} days'

    if mr:
        means = 'mean reversion'
    else:
        means = 'no mean reversion'

    

    ret = f'''Your simulation generated {sims} scenarios on {ts} for which you combined {trends},
     {means} and excercised stop losses at {abs(sl)}% drawdown and stop profit at 
     {sp}% return'''

    return ret