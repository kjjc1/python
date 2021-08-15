import pyupbit
import time
access = ""
secret = ""
upbit = pyupbit.Upbit(access, secret)

import telegram
tlgm_token = ''
tlgm_id = ''
bot = telegram.Bot(token = tlgm_token)
bot.sendMessage(chat_id = tlgm_id, text = 'Fianl?')

import pandas as pd


weight = 150000


total_evacuation = 0


initial_resist_trigger = 0


tickers = pyupbit.get_tickers(fiat = "KRW")

operation_df = pd.DataFrame(columns = ['ticker', 'buy_trigger', 'max_margin', 'initial_resist_trigger', 'loss_cut', 'loss_cut_trigger', 'old_resist_line', 'new_resist_line'])

operation_df['ticker'] = tickers

operation_df.fillna(0, inplace=True)


tickers = pyupbit.get_tickers(fiat = "KRW")
abp = 0
current_price = 0
margin = 0
ticker = 0


while True :
     for ticker in tickers :
        abp = upbit.get_avg_buy_price(ticker)
        current_price = pyupbit.get_current_price(ticker)
        ticker_balance = upbit.get_balance(ticker)
        krw_balance = upbit.get_balance("KRW")

        buy_trigger = float(operation_df.loc[(operation_df.ticker == ticker), 'buy_trigger'])
        max_margin = float(operation_df.loc[(operation_df.ticker == ticker), 'max_margin'])
        initial_resist_trigger = float(operation_df.loc[(operation_df.ticker == ticker), 'initial_resist_trigger'])
        loss_cut = float(operation_df.loc[(operation_df.ticker == ticker), 'loss_cut'])
        loss_cut_trigger = float(operation_df.loc[(operation_df.ticker == ticker), 'loss_cut_trigger'])
        old_resist_line = float(operation_df.loc[(operation_df.ticker == ticker), 'old_resist_line'])
        new_resist_line = float(operation_df.loc[(operation_df.ticker == ticker), 'new_resist_line'])

        if ticker_balance > 0 :  
            try:
                margin = (current_price - abp)/abp
            except ZeroDivisionError:
                print("ZeroDivision")
            except TypeError:
                print("TypeError")


        if abp == 0 :
            margin = 0
            operation_df.loc[(operation_df.ticker == ticker), 'max_margin'] = 0


        try:
            ticker_df_min = pyupbit.get_ohlcv(ticker, "minute5")
            high_price_min = ticker_df_min['high']
            low_price_min = ticker_df_min['low']
            close_price_min = ticker_df_min['close']
        except TypeError:
                print("TypeError")

        max_high_144min = ticker_df_min['max_high_144'] =  high_price_min.rolling(144, axis = 0).max()

        min_low_199min = ticker_df_min['min_low_199'] =  low_price_min.rolling(199, axis = 0).min()
        
        window5_min = close_price_min.rolling(5)
        ma5_min = window5_min.mean()
        ma5_min = ticker_df_min['ma5'] = close_price_min.rolling(5).mean()
        ma5_trend_199_min = ma5_min[199] - ma5_min[198]
        
        if ticker == "KRW-BTC" :
            if (ticker_balance * current_price <= 5000 or ticker_balance * current_price >= 50000) :
                total_evacuation = 0

        if ticker == "KRW-BTC" :
            if (ticker_balance * current_price > 5000 and
                ticker_balance * current_price < 15000) :
                total_evacuation = 1
                bot.sendMessage(chat_id = tlgm_id, text = '전체 100 % 매도 시작', timeout=180)

        if ticker == "KRW-BTC" :
            if (ticker_balance * current_price > 15000 and
                ticker_balance * current_price < 25000) :
                total_evacuation = 2
                bot.sendMessage(chat_id = tlgm_id, text = '전체 50 % 매도 시작', timeout=180)

        if ticker == "KRW-BTC" :
            if (ticker_balance * current_price > 25000 and
                ticker_balance * current_price < 35000) :
                total_evacuation = 3
                bot.sendMessage(chat_id = tlgm_id, text = '전체 50 % 매수 시작', timeout=180)

        if ticker == "KRW-BTC" :
            if (ticker_balance * current_price > 35000 and
                ticker_balance * current_price < 45000) :
                total_evacuation = 4
                bot.sendMessage(chat_id = tlgm_id, text = '전체 100 % 매수 시작', timeout=180)


        if (ticker != 'KRW-BTC' and total_evacuation == 1) :
            if ticker_balance * current_price > 5000 :
                sell_record0 = upbit.sell_market_order(ticker, ticker_balance)
                bot.sendMessage(chat_id = tlgm_id, text =
                            '\n코인: '+ticker+
                            '\n조건: 전체 100 % 매도' +
                            '\n평단가: '+ str(round(abp,2)) +
                            '\n현재가: '+ str(round(current_price,2)) +
                            '\n손절가: '+ str(round(loss_cut,2)) +
                            '\n신저항 '+ str(round(new_resist_line,2)) +
                            '\n구저항 '+ str(round(old_resist_line,2)) +
                            '\n현고점(199): '+ str(round(max_high_144min[199],2)) +
                            '\n전고점(198): '+ str(round(max_high_144min[198],2)) +
                            '\n장기 현저점(199): '+ str(round(min_low_199min[199],2)) +
                            '\n장기 전저점(198): '+ str(round(min_low_199min[198],2)) +
                            '\n현재수익률: '+ str(round(margin,4)) +
                            '\n최대수익률: '+ str(round(max_margin,4)), timeout=180)
                time.sleep(0.5)

        if (ticker != 'KRW-BTC' and total_evacuation == 2) :
            if ticker_balance * current_price > weight/2:
                sell_record0 = upbit.sell_market_order(ticker, ticker_balance/2)
                bot.sendMessage(chat_id = tlgm_id, text =
                            '\n코인: '+ticker+
                            '\n조건: 전체 50 % 매도' +
                            '\n평단가: '+ str(round(abp,2)) +
                            '\n현재가: '+ str(round(current_price,2)) +
                            '\n손절가: '+ str(round(loss_cut,2)) +
                            '\n신저항 '+ str(round(new_resist_line,2)) +
                            '\n구저항 '+ str(round(old_resist_line,2)) +
                            '\n현고점(199): '+ str(round(max_high_144min[199],2)) +
                            '\n전고점(198): '+ str(round(max_high_144min[198],2)) +
                            '\n장기 현저점(199): '+ str(round(min_low_199min[199],2)) +
                            '\n장기 전저점(198): '+ str(round(min_low_199min[198],2)) +
                            '\n현재수익률: '+ str(round(margin,4)) +
                            '\n최대수익률: '+ str(round(max_margin,4)), timeout=180)
                time.sleep(0.5)

        if (ticker != 'KRW-BTC' and total_evacuation == 3) :
            if ticker_balance * current_price < weight/2 :
                buy_record0 = upbit.buy_market_order(ticker, weight/2)
                bot.sendMessage(chat_id = tlgm_id, text =
                            '\n코인: '+ticker+
                            '\n조건: 전체 50 % 매수' +
                            '\n평단가: '+ str(round(abp,2)) +
                            '\n현재가: '+ str(round(current_price,2)) +
                            '\n손절가: '+ str(round(loss_cut,2)) +
                            '\n신저항 '+ str(round(new_resist_line,2)) +
                            '\n구저항 '+ str(round(old_resist_line,2)) +
                            '\n현고점(199): '+ str(round(max_high_144min[199],2)) +
                            '\n전고점(198): '+ str(round(max_high_144min[198],2)) +
                            '\n장기 현저점(199): '+ str(round(min_low_199min[199],2)) +
                            '\n장기 전저점(198): '+ str(round(min_low_199min[198],2)) +
                            '\n현재수익률: '+ str(round(margin,4)) +
                            '\n최대수익률: '+ str(round(max_margin,4)), timeout=180)
                time.sleep(0.5)

        if (ticker != 'KRW-BTC' and total_evacuation == 4) :
            if ((ticker_balance * current_price < 5000) and
                (ticker_balance * current_price < weight/2)):
                buy_record0 = upbit.buy_market_order(ticker, weight)
                bot.sendMessage(chat_id = tlgm_id, text =
                            '\n코인: '+ticker+
                            '\n조건: 전체 100 % 매수' +
                            '\n평단가: '+ str(round(abp,2)) +
                            '\n현재가: '+ str(round(current_price,2)) +
                            '\n손절가: '+ str(round(loss_cut,2)) +
                            '\n신저항 '+ str(round(new_resist_line,2)) +
                            '\n구저항 '+ str(round(old_resist_line,2)) +
                            '\n현고점(199): '+ str(round(max_high_144min[199],2)) +
                            '\n전고점(198): '+ str(round(max_high_144min[198],2)) +
                            '\n장기 현저점(199): '+ str(round(min_low_199min[199],2)) +
                            '\n장기 전저점(198): '+ str(round(min_low_199min[198],2)) +
                            '\n현재수익률: '+ str(round(margin,4)) +
                            '\n최대수익률: '+ str(round(max_margin,4)), timeout=180)
                time.sleep(0.5)


        if margin > max_margin :
            operation_df.loc[(operation_df.ticker == ticker), 'max_margin'] = margin


        if (ticker_balance * current_price) > 5000 :
            if loss_cut_trigger == 0 :
                operation_df.loc[(operation_df.ticker == ticker), 'loss_cut'] = ticker_df_min['min_low_199'][199]
                operation_df.loc[(operation_df.ticker == ticker), 'loss_cut_trigger'] = 1
                
            if (loss_cut_trigger == 1 and
                min_low_199min[199] > loss_cut) :                         
                operation_df.loc[(operation_df.ticker == ticker), 'loss_cut'] = ticker_df_min['min_low_199'][199]


        if  max_high_144min[198] > max_high_144min[199] :
            operation_df.loc[(operation_df.ticker == ticker), 'new_resist_line'] = max_high_144min[199]

        if max_high_144min[198] <= max_high_144min[199] :
            operation_df.loc[(operation_df.ticker == ticker), 'old_resist_line'] = new_resist_line

        if initial_resist_trigger == 0:
            operation_df.loc[(operation_df.ticker == ticker), 'new_resist_line'] = max_high_144min[199]
            operation_df.loc[(operation_df.ticker == ticker), 'old_resist_line'] = max_high_144min[199]
            operation_df.loc[(operation_df.ticker == ticker), 'initial_resist_trigger'] = 1

        if ma5_trend_199_min > 0 :
            operation_df.loc[(operation_df.ticker == ticker), 'buy_trigger'] = 1
            
            
        buy_trigger = float(operation_df.loc[(operation_df.ticker == ticker), 'buy_trigger'])
        max_margin = float(operation_df.loc[(operation_df.ticker == ticker), 'max_margin'])
        initial_resist_trigger = float(operation_df.loc[(operation_df.ticker == ticker), 'initial_resist_trigger'])
        loss_cut = float(operation_df.loc[(operation_df.ticker == ticker), 'loss_cut'])
        loss_cut_trigger = float(operation_df.loc[(operation_df.ticker == ticker), 'loss_cut_trigger'])
        old_resist_line = float(operation_df.loc[(operation_df.ticker == ticker), 'old_resist_line'])
        new_resist_line = float(operation_df.loc[(operation_df.ticker == ticker), 'new_resist_line'])


        if ticker == 'KRW-BTC' :
            bot.sendMessage(chat_id = tlgm_id, text = 'Program running', timeout=180)


        if (buy_trigger == 1 and
            ma5_trend_199_min >= 0 and
            ma5_min[199] > old_resist_line and
            (ticker_balance * current_price) < 5000) :
            buy_record0 = upbit.buy_market_order(ticker, weight)
            operation_df.loc[(operation_df.ticker == ticker), 'loss_cut'] = min_low_199min[199]
            bot.sendMessage(chat_id = tlgm_id, text =
                            '\n코인: '+ticker+
                            '\n조건: 매수' +
                            '\n평단가: '+ str(round(abp,2)) +
                            '\n현재가: '+ str(round(current_price,2)) +
                            '\n손절가: '+ str(round(loss_cut,2)) +
                            '\n신저항 '+ str(round(new_resist_line,2)) +
                            '\n구저항 '+ str(round(old_resist_line,2)) +
                            '\n현고점(199): '+ str(round(max_high_144min[199],2)) +
                            '\n전고점(198): '+ str(round(max_high_144min[198],2)) +
                            '\n장기 현저점(199): '+ str(round(min_low_199min[199],2)) +
                            '\n장기 전저점(198): '+ str(round(min_low_199min[198],2)) +
                            '\n현재수익률: '+ str(round(margin,4)) +
                            '\n최대수익률: '+ str(round(max_margin,4)), timeout=180)
            operation_df.loc[(operation_df.ticker == ticker), 'max_margin'] = 0
            operation_df.loc[(operation_df.ticker == ticker), 'buy_trigger'] = 0
            operation_df.loc[(operation_df.ticker == ticker), 'loss_cut_trigger'] = 1
            operation_df.loc[(operation_df.ticker == ticker), 'initial_resist_trigger'] = 0
            print(ticker, " 매수")


        if (ticker_balance * current_price > 5000 and
           (ma5_min[198] <= loss_cut) or (ma5_min[199] <= loss_cut)) :
            sell_record0 = upbit.sell_market_order(ticker, ticker_balance)
            bot.sendMessage(chat_id = tlgm_id, text =
                            '\n코인: '+ticker+
                            '\n조건: 매도' +
                            '\n평단가: '+ str(round(abp,2)) +
                            '\n현재가: '+ str(round(current_price,2)) +
                            '\n손절가: '+ str(round(loss_cut,2)) +
                            '\n신저항 '+ str(round(new_resist_line,2)) +
                            '\n구저항 '+ str(round(old_resist_line,2)) +
                            '\n현고점(199): '+ str(round(max_high_144min[199],2)) +
                            '\n전고점(198): '+ str(round(max_high_144min[198],2)) +
                            '\n장기 현저점(199): '+ str(round(min_low_199min[199],2)) +
                            '\n장기 전저점(198): '+ str(round(min_low_199min[198],2)) +
                            '\n현재수익률: '+ str(round(margin,4)) +
                            '\n최대수익률: '+ str(round(max_margin,4)), timeout=180)
            operation_df.loc[(operation_df.ticker == ticker), 'max_margin'] = 0
            operation_df.loc[(operation_df.ticker == ticker), 'buy_trigger'] = 0
            operation_df.loc[(operation_df.ticker == ticker), 'loss_cut'] = 0
            operation_df.loc[(operation_df.ticker == ticker), 'loss_cut_trigger'] = 0
            operation_df.loc[(operation_df.ticker == ticker), 'initial_resist_trigger'] = 0
            print(ticker, " 매도")
            
        time.sleep(0.1)