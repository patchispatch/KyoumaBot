# -*- coding: utf-8 -*-

import logging
from config import TOKEN
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import utils


# Enable logging
logging.basicConfig(
	format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(bot, update):
	message = 'Saludos, {}. Conocerte es la elección de la Steins Gate. El. Psy. Kongroo.'. \
				format(update.message.from_user.first_name)
	update.message.reply_text(message)

# Methods without command:

# Detecta si alguien se refiere a alumnos en vez de a estudiantes
def estudiante(bot, update):
	msg = update.message.text.lower()

	if 'alumn' in msg:
		update.message.reply_text('Eres estudiante, no lo olvides.')


# Methods with command:

# Detects if a word is a palindrome
def palindromo(bot, update):
	# message.text format "/command text"
	tmp = update.message.text.split(" ")

	# first element is command
	tmp.pop(0)
	# tebuild text back to its form
	msg = ' '.join(tmp)

	if msg is not "":
		utils.is_palindrome(bot, update, msg)
	else:
		update.message.reply_text("Pf, ni siquiera sabes introducir algo de texto...\
		Prueba de nuevo.")


# Error handler
def error(bot, update, error):
	"""Log Errors caused by Updates."""
	logger.warning('Update "%s" caused error "%s"', update, error)


def main():
	# Start the bot
	# Create the EventHandler and pass the TOKEN of our bot:
	updater = Updater(TOKEN)


	# Have the dispatcher register the handlers:
	dp = updater.dispatcher

	# Commands:
	dp.add_handler(CommandHandler('start', start))
	dp.add_handler(CommandHandler('palindromo', palindromo))

	# No commands:
	dp.add_handler(MessageHandler(Filters.text, estudiante))

	# Error Handler:
	dp.add_error_handler(error)

	# Start the bot:
	updater.start_polling()

	# Have the bot activated until it stops with Ctrl + C:
	updater.idle()


if __name__ == '__main__':
	main()
