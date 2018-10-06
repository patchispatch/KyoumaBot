# -*- coding: utf-8 -*-
import logging

from config import TOKEN
from utils import transalate_message

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


# Enable logging
logging.basicConfig(
	format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(bot, update):
	message = transalate_message(
		'Greetings. Meeting you is the choice of the Steins Gate, {}. The. Psy. Kongroo.'. \
		format(update.message.from_user.first_name))
	update.message.reply_text(message)

# Methods without command:

# Detecta si alguien se refiere a alumnos en vez de a estudiantes
def estudiante(bot, update):
	msg = update.message.text.lower()

	if transalate_message('alumn') in transalate_message(msg):
		update.message.reply_text(transalate_message('You are a student.'))


# Methods with command:

# Detects if a word is a palindrome
def palindromo(bot, update):
	texto = update.message.reply_to_message.text

	if texto == texto[::-1]:
		message = 'The text: " {} " it is a palindrome'.format(texto)
	else:
		message = 'The text: " {} " it is not a palindrome'.format(texto)
	update.message.reply_text(transalate_message(message))


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
