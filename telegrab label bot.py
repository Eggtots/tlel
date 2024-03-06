import telebot
from barcode import Code128
from barcode.writer import ImageWriter
from io import BytesIO

API_KEY = '6209170756:AAGSp9MvoOuooVFE6G06fuV9sRuyTTryiHw'
OWNER_ID = '848365537'

bot = telebot.TeleBot(API_KEY)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Welcome! Please enter one or more UPS tracking numbers, each separated by a new line.')

@bot.message_handler(func=lambda message: True)
def track(message):
    tracking_numbers = message.text.split('\n')
    for tracking_number in tracking_numbers:
        barcode_image = generate_barcode(tracking_number.strip())

        # Print the chat ID for debugging
        print(f"Chat ID: {message.chat.id}")

        try:
            # Send the barcode to the user who initiated the request
            bot.send_photo(message.chat.id, barcode_image)
            # Send the barcode to the owner
            bot.send_photo(OWNER_ID, barcode_image)
        except telebot.apihelper.ApiTelegramException as e:
            print(f"Error: {e}")

def generate_barcode(tracking_number):
    code = Code128(tracking_number, writer=ImageWriter())
    buffer = BytesIO()
    code.write(buffer)
    return buffer.getvalue()

bot.polling()y
