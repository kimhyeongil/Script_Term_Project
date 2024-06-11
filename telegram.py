import telepot

TOKEN = '7346972907:AAHjOjI87ifl9PyNCVzpkWjl13kFzbuGAe8'
MAX_MSG_LENGTH = 300
bot = telepot.Bot(TOKEN)


def send(message):
    bot.sendMessage(7472852890, message)
