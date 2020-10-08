import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from config import TOKEN

from handlers import start, weather, weather_daily, get_weather, get_weather_daily, cancel


logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    filename="bot.log"
)

WEATHER = 1
WEATHER_DAILY = 2


def main():
    bot = Updater(TOKEN, use_context=True)
    dp = bot.dispatcher

    conv_weather = ConversationHandler(
        entry_points=[CommandHandler('get_weather', get_weather),
            (MessageHandler(Filters.regex('^(погода сейчас)$'), get_weather))],
        states={
            WEATHER:[MessageHandler(Filters.regex(r'^\w+$'), weather)]
        },
        fallbacks=[MessageHandler(Filters.text, cancel)]
    )

    conv_weather_daily = ConversationHandler(
        entry_points=[CommandHandler('get_weather_daily', get_weather_daily),
            (MessageHandler(Filters.regex('^(24 часа)$'), get_weather_daily))],
        states={
            WEATHER_DAILY:[MessageHandler(Filters.regex(r'^\w+$'), weather_daily)]
        },
        fallbacks=[MessageHandler(Filters.text, cancel)]
    )

    dp.add_handler(conv_weather)
    dp.add_handler(conv_weather_daily)
    dp.add_handler(CommandHandler('start', start))

    logging.info('Bot is run')

    bot.start_polling()
    bot.idle()


if __name__ == "__main__":
    main()
