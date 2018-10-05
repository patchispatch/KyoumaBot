# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from botutil import esPalindromo
from config import TOKEN
import logging

# Habilitar logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(bot, update):
	update.message.reply_text(
        'Greetings. Meeting you is the choice of the Steins Gate, {}. El. Psy. Kongroo.'.format(update.message.from_user.first_name))

# Métodos sin comando:

# Detecta si alguien se refiere a alumnos en vez de a estudiantes
def estudiante(bot, update):
	msg = update.message.text

	if 'alumn' in msg.lower():
		update.message.reply_text('Usted es estudiante.')


# Métodos con comando:

# Detecta si una cadena es un palíndromo
def palindromo(bot, update):
	texto = update.message.reply_to_message.text

	if esPalindromo(texto):
		update.message.reply_text(
			'El texto: " {} " es un palindromo'.format(texto))
	else:
		update.message.reply_text(
			'El texto: " {} " no es un palindromo'.format(texto))

# Error handler
def error(bot, update, error):
	"""Log Errors caused by Updates."""
	logger.warning('Update "%s" caused error "%s"', update, error)

def main():
	# Iniciar el bot
	# Crear el EventHandler y pasarle el TOKEN de nuestro bot:
	updater = Updater(TOKEN)

	# Hacer que el dispatcher registre los handlers:
	dp = updater.dispatcher

	# Comandos:
	dp.add_handler(CommandHandler('start', start))
	dp.add_handler(CommandHandler('palindromo', palindromo))

	# No comandos:
	dp.add_handler(MessageHandler(Filters.text, estudiante))

	# Handler de errores:
	dp.add_error_handler(error)

	# Iniciar el bot:
	updater.start_polling()

	# Tener el bot activado hasta que se detenga con Ctrl+c:
	updater.idle()


if __name__ == '__main__':
	main()
