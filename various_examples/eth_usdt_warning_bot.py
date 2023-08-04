import numpy as np
import talib
import schedule
import time
import ccxt
from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater

"""This is a basic Telegram bot designed primarily for use with the Binance ETH/USDT pair, leveraging the Commodity Channel Index (CCI) indicator to provide various alerts. 
Please note that this bot has not been fully tested yet."""

def get_cci(symbol, timeframe='1h', period=14):
    exchange = ccxt.binance()
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe)
    close = np.array([x[4] for x in ohlcv], dtype=float)
    high = np.array([x[2] for x in ohlcv], dtype=float)
    low = np.array([x[3] for x in ohlcv], dtype=float)
    cci = talib.CCI(high, low, close, timeperiod=period)
    return cci[-1]

def cci_warning(context):
    symbol = 'ETH/USDT'
    chat_id = context.job.context

    cci_value = get_cci(symbol)

    if cci_value > 200:
        message = f"{symbol} CCI value: {cci_value:.2f}. Extreme overbought warning!"
    elif cci_value > 90:
        message = f"{symbol} CCI value: {cci_value:.2f}. Overbought warning!"
    elif cci_value < -200:
        message = f"{symbol} CCI value: {cci_value:.2f}. Extreme oversold warning!"
    elif cci_value < -90:
        message = f"{symbol} CCI value: {cci_value:.2f}. Oversold warning!"
    else:
        message = f"{symbol} CCI value: {cci_value:.2f}. No warning."

    context.bot.send_message(chat_id=chat_id, text=message)

def start_monitoring(update: Update, context):
    update.message.reply_text('Monitoring started for ETH/USDT.')

    #Schedule the cci_warning task to run every 1 hour.
    schedule.every(1).hours.do(cci_warning, context=context)

def main():
    updater = Updater(" Telegram Token ", use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start_monitoring))

    updater.start_polling()

    while True:
        schedule.run_pending()
        time.sleep(1)

    updater.idle()

if __name__ == '__main__':
    main()