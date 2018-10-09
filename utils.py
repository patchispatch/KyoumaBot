# Utilities for the bot:

# Check if a word is a palindrome:
def is_palindrome(bot, update, msg):
	text = msg.lower()

	if text == text[::-1]:
		message = 'El texto "{}" es un  palíndromo'.format(msg)
	else:
		message = 'El texto "{}" no es un palíndromo'.format(msg)
	update.message.reply_text(message)
