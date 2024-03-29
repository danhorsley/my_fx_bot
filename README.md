# FX Bot

## What does FX bot do and what is its use case?

FX Bot lets the user choose froom a number of strategies and risk management methodologies and test them over a number of 'possible futures' generated by a basic [Monte Carlo](https://en.wikipedia.org/wiki/Monte_Carlo_method) simualtion.  It then applies them to currency 'pairs' of your choice to see how they perform in combination.  Every currency pair has its own characteristics, and rules apporpriate for one may not be good for another.  Real world users could be individual investors, companies hedging their FX exposures, or even people moving abroad or going on holiday timing when to change their money.  FX Bot could also easily be expanded to equities, bonds and any financial instrument with a decent amount of histroical data. 

There is an even larger use case beyond the world of finance.  When people or companies set up certain rules they tend to view those rules in isolation.  They look at the rule alone and decide that "this is a good rule" and adopt it.  They don't tend to think about the rules in combination with the other rules they have adopted.  This 'rule soup' can have unintended consequences, even potentially the [opposite of whatever your desired outcome is](https://en.wikipedia.org/wiki/Cobra_effect).  The process of FX Bot can be extrapolated to anything where you have clearly defined strategies and outcomes.  But that is for another project...

## What's a currency pair?

In foreign exchange land, a currency's price is only referenced with respect to another currency.  For example 'EURUSD' means how many dollars would you receive for one Euro.  Order matters.  'USDEUR' would be one over whatever the EURUSD price was.  Other common currency pairs are USDJPY, GBPUSD and EURJPY.  These are also the standard wway they ar quoted in.

## What is a Monte Carlo simulation?

Just a fancy way of saying we use past events to predict possible future scenarios.  Imagine every day from a period in the past is represented by a number on a (large!) roulette wheel.  We then spin that wheel multiple times to generate a possible future, with each spin representing the next day in the future.  Obviously this aprroach is not flawless as certain types of days can 'chain' together in reality (see 'Possible Improvements' section below) and the future is never an exact replication of the past.  Despite these problems, it is a very useful tool for testing trading strategies, portfolio construction and risk limits.

## What is a trend following strategy?

The premise that if things are goign one way, they tend to keep goign that way!  We determine this by fitting a line through a certain number of days in a past 'window' (e.g. 30 days) and check how closely that line fits the historical prices, using an R2 score.  If that score meets a certain threshold a trade is inititated to capture a future move in the same direction.  It is then closed when that trend is no longer adhered to by the underlying reality! Trend following is one of the most dominant strategies gloablly , especially among large algorithmacially driven equity focused funds.  

## What is a mean reversion strategy?

This strategy attempts to take advantage of market participants habit of over-reacting in the short term.
Generally short-term in nature these trade strategies use several approaches.  FX Bot uses one of the simplest : when the current price is over one standard deviation away from the rolling average a trade is initiated looking to profit from the current price closing the gap to the moving average.

## How does FX Bot work?

At first FX Bot relied heavily on the Pandas library.  However this libarary is computationally slow and hit up against the maximum request time length (30 seconds) but also slug size on Heroku (soft limit 300Mb, hard limit 500Mb).  The code was refactored to use Numpy exclusively and also we used our own function for the linear regression function (initially we used the function in the scikit-learn library).  Run time is now multiple (>10x) times faster.

## What is a stop-loss and a stop-profit?

These trades can be summed up as respectively "stop the ride I want to get off" and "quitting while you are ahead".   A stop loss triggers a whole or partial close of your portfolio when you lose a certain amount of money (in this case the default is 5% of your portfolio starting values).  A stop-profit is the opposite when you bank your returns if you find yourself doign very well.  The stop-loss is an incredibly common risk-management tool to limit portfolio losses (especially in times of market stress), though it can be taken advantage of.  Many market participants simply wait for others to stop-loss they can buy at artifically low levels.

## Where do you get the data from?

The historical close prices are all from a python library called ['forex-python'](https://forex-python.readthedocs.io/en/latest/usage.html).  This libaray in turn gets its prices from a free API for current and historical foreign exchange rates published by [European Central Bank](https://ratesapi.io/).

## Possible Improvements

The reader will undoubtably have noticed that there is no point testing the success or failiure of these trading strategies in random futures generated in this way as trends and mean reversion will not work the same way they do in reality.  There is a solution to this which is not too hard to implement.  This is called [Markov chain Monte Carlo](https://en.wikipedia.org/wiki/Markov_chain_Monte_Carlo) and is a way of more accurately simulating the future.  It imagines the past in a number of chains - the financial crisis would be one chain, the dotcom bubble another etc - and when you are in one chain you most probably remain in that chain on a day to day basis.  But each day you have a certain probability of transitioning to another chain entirely.  This improved Monte Carlo simulation more closely resembles reality as whn you are in a certain chain you only sample from days in the same chain from the historical data.  Trend following and mean reversion would be tested in conditions much closer to reality if we used this.

Other improvements would be to add hourly or minutely data, non FX related securities, more complex calculation intensive strategies (heroku really limits these) and also an update system to alert users when thier preferred strategy is indicating a buy or a sell or when they should be takign profit on an exiting trade.  Also we would like to explore more complex strategy logic (i.e. trades in multiple securities given certain conditions).

The profit and loss model does not currently include carry - i.e. the difference in interest rates between the thw currencies. For example at the moment the Euro has a deposit rate of -0.4% while the Dollar has a deposit rate of 1.89% giving a differential of 2.29%.  This means you are 2.29% a year worse off holding Euros for the year than Dollars, which adds up a lot over time especially if you are using leverage.  Long term trades just to pick up the carry iw a well known strategy in FX markets and it wouldn't be too difficult to implement the correct p&l and carry as a strategy in the future.



