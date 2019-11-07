def make_text(ts,sims,nd,tf1,tf2,tf3,ltsm,mr,sl,sp,
                avg_pnl,min_pnl,max_pnl):

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

    

    ret = f'''Your simulation generated {sims} scenarios on {ts} over {nd} days for which you combined {trends},
     {means} and excercised stop losses at {abs(sl)}% drawdown and stop profit at 
     {sp}% return.  These strategies returned an average return of {avg_pnl:.2f}%, with a best performance of {max_pnl:.2f}%
     and worst performance of {min_pnl:.2f}%.  Annualized these numbers equate to {100*((1+avg_pnl/100)**(225/nd)-1):.2f}%, 
     {100*((1+max_pnl/100)**(225/nd)-1):.2f}% and {100*((1+min_pnl/100)**(225/nd)-1):.2f}% respectively.'''

    return ret