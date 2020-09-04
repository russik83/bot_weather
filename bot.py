import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from config import TOKEN

from handlers import start, weather, get_weather, cancel


logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    filename="bot.log"
)

WEATHER = 1


def main():
    bot = Updater(TOKEN, use_context=True)
    dp = bot.dispatcher

    conv_weather = ConversationHandler(
        entry_points=[CommandHandler('get_weather', get_weather),
            (MessageHandler(Filters.regex('^(погода)$'), get_weather))],
        states={
            WEATHER:[MessageHandler(Filters.regex(r'^\w+$'), weather)]
        },
        fallbacks=[MessageHandler(Filters.text, cancel)]
    )

    dp.add_handler(conv_weather)
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.regex('^(погода)$'), get_weather))
    dp.add_handler(MessageHandler(Filters.text, weather))

    logging.info('Bot is run')

    bot.start_polling()
    bot.idle()


if __name__ == "__main__":
    main()
