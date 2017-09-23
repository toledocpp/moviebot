# this app uses python-telegram-bot (https://github.com/python-telegram-bot/python-telegram-bot)
# this app uses tmdbsimple (https://github.com/celiao/tmdbsimple)
# this app uses The Movie DB (https://www.themoviedb.org)
import json
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

CONFIG_FILE = 'config.json'

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.


def show_hello_message(bot, update):
    update.message.reply_text('Hi!')


def show_help_message(bot, update):
    update.message.reply_text('Help!')


def show_echo_message(bot, update):
    update.message.reply_text(update.message.text)


def show_random_movie(bot, update):
    update.message.reply_text('Lock, stock and two smoking barrels')


def show_random_cartoon(bot, update):
    update.message.reply_text('Happy Tree Friends')


def print_error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))


def main():
    logger.info('Application start...')

    # get access tokens from config file
    json_file = open(CONFIG_FILE, 'r')
    json_data = json.load(json_file)
    json_file.close()
    # bot access token
    bot_access_token = json_data['bot']['token']
    logger.info('Telegram bot access token - ' + bot_access_token)
    # database access token
    db_access_token = json_data['database']['api_key_v3']
    logger.info('Database access token - ' + db_access_token)

    # Create the EventHandler and pass it your bot's token.
    updater = Updater(bot_access_token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", show_hello_message))
    dp.add_handler(CommandHandler("help", show_help_message))
    dp.add_handler(CommandHandler("movie", show_random_movie))
    dp.add_handler(CommandHandler("cartoon", show_random_cartoon))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, show_echo_message))

    # log all errors
    dp.add_error_handler(print_error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
