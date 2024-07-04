# some parameters
leverage = 0.1
fee_rate = 0.0005

# Get the information in which we are intested
import json

data = [{
    'side': r['side'],
    'posSide': r['posSide'],
    'fillPnl': float(r['fillPnl']),
    'fillPx': float(r['fillPx']),
    'fee': float(r['fee']),
    'fillSz': r['fillSz'],
    'instId': r['instId'],
    } for r in json.load(open('trades.json', 'r'))['data']]

trades = [] # A list of closed trade
for r in data:
    if r['side'] == 'sell' and r['posSide'] == 'long' or r['side'] == 'buy' and r['posSide'] == 'short':
        # closed trade
        if r['posSide'] == 'long':
            opened_fillPx = r['fillPx'] - r['fillPnl'] / leverage
            r['cost'] = opened_fillPx
        else:
            opened_fillPx = r['fillPx'] + r['fillPnl'] / leverage
            r['cost'] = r['fillPx']
         
        r['fee'] -= fee_rate * leverage * opened_fillPx
        trades.append(r)
        
## Calculate ROI
total_pnl = 0
total_cost = 0
for t in trades:
    total_pnl += t['fillPnl'] + t['fee']
    total_cost += t['cost'] - t['fee']

ROI = total_pnl / total_cost
print(f'* ROI = {ROI * 100}%')

## Calculate Win Rate
win_count = 0
for t in trades:
    if t['fillPnl'] + t['fee'] > 0:
        win_count += 1

win_rate = win_count / len(trades)
print(f'* Win Rate = {win_rate * 100}%')

# Calculate MDD
highest_capital = 8000
current_capital = 8000
MDD = 0
for t in trades:
    current_capital += t['fillPnl']
    MDD = min(MDD, (current_capital - highest_capital) / highest_capital)
    highest_capital = max(highest_capital, current_capital)

print(f'* MDD = {MDD}%')

# Calculate Odds Ratio (invest ETH instead of BTC)
win_count_eth = 0
count_eth = 0
win_count_btc = 0
count_btc = 0
for t in trades:
    if t['fillPnl'] + t['fee'] > 0:
        if t['instId'] == 'ETH-USDT-SWAP':
            win_count_eth += 1
        else:
            win_count_btc += 1
            
    if t['instId'] == 'ETH-USDT-SWAP':
        count_eth += 1
    else:
        count_btc += 1
        
odds_ratio = win_count_eth / count_eth / win_count_btc * count_btc
print(f'* Odds Ratio (invest ETH instead of BTC) = {odds_ratio * 100}%')

# Calculate Profit Factor
gross_profit = 0
gross_loss = 0
for t in trades:
    pnl = t['fillPnl'] + t['fee']
    if pnl > 0:
        gross_profit += pnl
    else:
        gross_loss -= pnl

profit_factor = gross_profit / gross_loss
print(f'* Profit Factor = {profit_factor}')

# Calculate Sharpe Ratio
import math
rets = [(t['fillPnl'] + t['fee']) / (t['cost'] - t['fee']) for t in trades]
avg_ret = sum(rets) / len(rets)
std_ret = math.sqrt(sum([(r - avg_ret)**2 for r in rets]) / (len(rets) - 1))
sharpe_ratio = avg_ret / std_ret
print(f'* Sharpe Ratio = {sharpe_ratio}')
