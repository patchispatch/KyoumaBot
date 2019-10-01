# -*- coding: utf-8 -*-

import logging
from config import TOKEN
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
						  ConversationHandler, RegexHandler)
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, Document)
import os
import utils

###############################################################################
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
		"gatos, pero al menos, envíame tu localización. "
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
	logger.info("User %s did not send a bio.", user.first_name)

	update.message.reply_text(
		"Haces bien guardando silencio... Quién sabe si la Organización\
		nos está escuchando. Nos veremos, {}. El. Psy. Kongroo.".format(user.first_name))

	return ConversationHandler.END

def bio(bot, update):
	user = update.message.from_user
	logger.info("Bio of %s: %s", user.first_name, update.message.text)
	update.message.reply_text(
		"Gracias por tu tiempo. Me aseguraré de mantener esta información "
		"lejos de las manos de la organización. El. Psy. Kongroo.",
								reply_markup=ReplyKeyboardRemove())

	return ConversationHandler.END

###############################################################################
# Detecta si alguien se refiere a alumnos en vez de a estudiantes
def estudiante(bot, update):
	user = update.message.from_user
	msg = update.message.text.lower()

	if 'alumn' in msg:
		update.message.reply_text('Eres estudiante, no lo olvides.')
		logger.info("{} has written 'alumn*'.".format(user.first_name))

###############################################################################
# Detecta si alguien pregunta por Homer
def homer(bot, update):
    user = update.message.from_user
    msg = update.message.text.lower()
    
    if 'homer' or 'Homer' in msg:
        update.message.reply_text('¿Homer? ¿Quién es Homer? Yo me llamo tipo de \incógnito.')
        logger.info("{} has written 'homer'.".format(user.first_name))


###############################################################################
# Written and Directed by Quentin Tarantino:
def bingo(bot, update):
	user = update.message.from_user
	msg = update.message.text.lower()
	chat_id = update.message.chat_id
	url = "https://goo.gl/Lyp7V7"

	if 'bingo' in msg:
		bot.send_photo(chat_id, url, "Es un BINGO")
		logger.info("{} has written 'bingo'.".format(user.first_name))

###############################################################################
# Filters:
def filtros(bot, update):
	bingo(bot, update)
	estudiante(bot, update)
    homer(bot, update)

###############################################################################
# Detects if a word is a palindrome

# States:
VACIO = range(1)

def palindromo(bot, update):
	user = update.message.from_user

	# message.text format "/command text"
	tmp = update.message.text.split(" ")

	# first element is command
	tmp.pop(0)
	# tebuild text back to its form
	msg = ' '.join(tmp)

	if msg is not "":
		logger.info("User {} has put /palindromo with text.".format(user.first_name))
		utils.is_palindrome(bot, update, msg)
		return ConversationHandler.END

	else:
		logger.info("User {} has put /palindromo with no text.".format(user.first_name))
		update.message.reply_text("Prueba a introducir algo de texto, anda. \
			Si no quieres, escribe /cancel.")
		return VACIO

def pal_no_text(bot, update):
	msg = update.message.text
	utils.is_palindrome(bot, update, msg)

	return ConversationHandler.END

###############################################################################
# Sends user's cat photo:
def cat_photo(bot, update):
	user = update.message.from_user
	chat_id = update.message.chat_id

	try:
		photo = open('photos/{}.jpg'.format(user.first_name), 'rb')
	except:
		update.message.reply_text("No puedo enseñarte tu gato si no me lo\
		enseñas tú primero. Las reglas son las reglas.")

		# Exit function
		return

	bot.send_photo(chat_id, photo, "Tu supuesto gato es muy bonito.")

###############################################################################
# Sends SCU menu:
def scu_menu(bot, update):
	user = update.message.from_user
	chat_id = update.message.chat_id
	logger.info("User {} has requested SCU menu.".format(user.first_name))

	# Specify the url of the file:
	url = 'http://scu.ugr.es/?theme=pdf'

	# Send the doc:
	bot.send_document(chat_id, url, "Menu.pdf", "Aquí tienes el menú de la semana.")

###############################################################################
# Sends a beautiful song <3:
def song(bot, update):
	user = update.message.from_user
	chat_id = update.message.chat_id
	logger.info("User {} has requested a beautiful song.".format(user.first_name))

	# Specify the url of the file:
	url = 'http://www.csd.gob.es/csd/estaticos/info-inst/Track01.mp3'

	# Send the song:
	bot.send_document(chat_id, url, "Menu.pdf", "Para ti <3.")
  

#######################################################################
###################################################################
#DEIIT
def deiit(bot, update):
  logger.info("User {} has requested a deiit.".format(user.first_name))
  update.message.reply_text("DEIIT.UNA GRANDE Y LIBRE")
	

###############################################################################
# Never gives you up:
def never_give_up(bot, update):
	user = update.message.from_user
	chat_id = update.message.chat_id
	logger.info("User {} has activated my trap card.".format(user.first_name))

	# Send the video:
	update.message.reply_text("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

###############################################################################
# Cancel conversation:
def cancel(bot, update):
	user = update.message.from_user
	logger.info("User {} canceled the conversation.".format(user.first_name))
	update.message.reply_text("Nos vemos, {}. El. Psy. Kongroo".format(user.first_name),
								reply_markup=ReplyKeyboardRemove())

	return ConversationHandler.END

###############################################################################
# Error handler
def error(bot, update, error):
	"""Log Errors caused by Updates."""
	logger.warning('Update "%s" caused error "%s"', update, error)

###############################################################################
# Main:
def main():
	# Start the bot
	# Create the EventHandler and pass the TOKEN of our bot:
	updater = Updater(TOKEN)


	# Have the dispatcher register the handlers:
	dp = updater.dispatcher

	# Conv. handler: start.
	conv_start = ConversationHandler(
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

	dp.add_handler(conv_start)

	# Conv. handler: palindromo
	conv_pal = ConversationHandler(
		entry_points=[CommandHandler('palindromo', palindromo)],

		states={
			VACIO: [MessageHandler(Filters.text, pal_no_text)]
		},

		fallbacks=[CommandHandler('cancel', cancel)]
	)

	dp.add_handler(conv_pal)

	# Command Handler: cat_photo
	dp.add_handler(CommandHandler('cat', cat_photo))

	# Command handler: menu
	dp.add_handler(CommandHandler('menu', scu_menu))

	# Command handler: song
	dp.add_handler(CommandHandler('song', song))
	
	# Command handler: never_give_up
	dp.add_handler(CommandHandler('never_give_up', never_give_up))

	# Message handlers:
	dp.add_handler(MessageHandler(Filters.text, filtros))

	# Error Handler:
	dp.add_error_handler(error)

	# Start the bot:
	updater.start_polling()

	# Have the bot activated until it stops with Ctrl + C:
	updater.idle()


if __name__ == '__main__':
	main()
