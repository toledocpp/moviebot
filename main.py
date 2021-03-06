import json
import random
import logging
import tmdbsimple as tmdb
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


# TODO: fix problem with invalid movie id (e.g. https://www.themoviedb.org/movie/225560)
def show_random_movie(bot, update):
    # First, get latest movie id
    movies = tmdb.Movies()
    movies.latest()
    latest_movie_id = movies.id
    logger.info('Last movie id - ' + str(latest_movie_id))
    # Next, generate random number in range between 1 and latest movie id
    random_movie_id = random.randint(1, latest_movie_id)
    logger.info('Random movie id - ' + str(random_movie_id))
    # Request a movie from movie database by random_movie_id
    movies = tmdb.Movies(random_movie_id)
    movies.info()
    bot_answer = 'Hey, that movie looks so pretty: https://www.themoviedb.org/movie/' + str(random_movie_id)
    update.message.reply_text(bot_answer)


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

    # init tmdb library
    tmdb.API_KEY = db_access_token

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
