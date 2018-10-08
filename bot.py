# -*- coding: utf-8 -*-

import logging
from config import TOKEN
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
						  ConversationHandler, RegexHandler)
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
import utils


# Enable logging
logging.basicConfig(
	format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

###############################################################################
# Initial conversation

# States:
GENDER, PHOTO, LOCATION, BIO = range(4)

# Functions:
def start(bot, update):
	reply_keyboard = [["Chica", "Chico", "Otro"]]

	update.message.reply_text(
		"Hola. Va a sonar a profesor pokémon, pero... ¿qué eres exactamente? "
		"Si quieres terminar la conversación, usa /cancel.",
		reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

	return GENDER

def gender(bot, update):
	user = update.message.from_user
	logger.info("Género de %s: %s", user.first_name, update.message.text)
	update.message.reply_text(
		"Bien, bien. Ahora, mándame una foto de un gato. Confío en ti. "
		"Si no quieres, escribe /skip y ya.")

	return PHOTO

def photo(bot, update):
	user = update.message.from_user
	photo_file = bot.get_file(update.message.photo[-1].file_id)
	photo_file.download('photos/{}.jpg'.format(user.first_name))
	logger.info("Foto de %s: %s", user.first_name, 'user_photo.jpg')
	update.message.reply_text(
		"Voy a confiar en que me has enviado una foto de un gato. Ahora "
		"sólo necesito que me envíes tu ubicación. Si prefieres no decirlo, escribe "
		"/skip y permanecerá en el anonimato.")

	return LOCATION

def location(bot, update):
	user = update.message.from_user
	user_location = update.message.location
	logger.info("Location of %s: %f / %f", user.first_name, user_location.latitude,
				user_location.longitude)
	update.message.reply_text("Parece un buen punto de encuentro, estás a salvo "
								"de la organización. Ahora, cuéntame algo sobre ti. "
								"Si no quieres, /skip.")

	return BIO


def skip_photo(bot, update):
	user = update.message.from_user
	logger.info("Usuario %s no envió foto.", user.first_name)
	update.message.reply_text(
		"Bueno, entiendo que no te fíes de mí como para mandarme fotos de "
		"gatos, pero al menos, cuéntame algo sobre ti. "
		"Si no quieres, ya sabes, /skip.")

	return LOCATION

def skip_location(bot, update):
	user = update.message.from_user
	logger.info("User %s did not send a location.", user.first_name)
	update.message.reply_text(
		"Hm, así que no quieres revelar tus datos... Es comprensible. "
 		"La organización podría estar escuchando. "
		"Si quieres contarme algo sobre ti, adelante. "
		"Aunque puedes negarte con /skip.")

	return BIO


def skip_bio(bot, update):
	user = update.message.from_user
	logger.info("User %s did not send a location.", user.first_name)

	update.message.reply_text(
		"Haces bien guardando silencio... Quién sabe si la Organización\
		nos está escuchando. Nos veremos, {}. El. Psy. Kongroo.".format(user.first_name))

	return ConversationHandler.END

def bio(bot, update):
	user = update.message.from_user
	logger.info("Bio of %s: %s", user.first_name, update.message.text)
	update.message.reply_text(
		"Gracias por tu tiempo. Me aseguraré de mantener esta información "
		"lejos de las manos de la organización. El. Psy. Kongroo.")

def cancel(bot, update):
	user = update.message.from_user
	logger.info("User %s canceled the conversation.", user.first_name)
	update.message.reply_text("Nos vemos, {}. El. Psy. Kongroo".format(user.first_name),
								reply_markup=ReplyKeyboardRemove())

	return ConversationHandler.END

###############################################################################
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

	# Conv. handler: start.
	conv_handler = ConversationHandler(
		entry_points=[CommandHandler('start', start)],

		states={
			GENDER: [RegexHandler('^(Chica|Chico|Otro)$', gender)],

			PHOTO: [MessageHandler(Filters.photo, photo),
					CommandHandler('skip', skip_photo)],

			LOCATION: [MessageHandler(Filters.location, location),
						CommandHandler('skip', skip_location)],

			BIO: [MessageHandler(Filters.text, bio),
						CommandHandler('skip', skip_bio)]
			},

		fallbacks=[CommandHandler('cancel', cancel)]
	)

	dp.add_handler(conv_handler)

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
