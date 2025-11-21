import os

import telebot

#creating the horoscope bot
import requests

BOT_TOKEN = os.environ.get('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(commands=['horoscope'])
def sign_handler(message):
    text = "What's your zodiac sign?\nChoose one: *Aries*, *Taurus*, *Gemini*, *Cancer*, *Leo*, *Virgo*, *Libra*, *Scorpio*, *Sagittarius*, *Capricorn*,*Aquariius*, and *Pisces*."
    sent_msg = bot.send_message(message.chat.id, text, parse_mode = "Markdown")
    bot.register_next_step_handler(sent_msg, day_handler) # type: ignore
    #bot.reply_to(message, message.text) #This is the repeat command message


def get_daily_horoscope(sign: str, day: str) -> dict:
    """Get daily horoscope for a zodiac sign.
    Keyword arguments:
    sign:str - Zidiac sign
    day:str - Date in format(YYYY-MM-DD) OR TODAY OR TOMMAROW OR YESTERDAY
    Return:dict - JSON data
    """
    url = "https://horoscope-app-api.vercel.app/api/v1/get-horoscope/daily"
    params = {"sign": sign, "day": day}
    response = requests.get(url,params)

    return response.json()
{
    "data":{
    "date": "Dex 15, 2023",
    "horoscpoe_data": "Lie low during the day and try not to get caught"
    },
    "status": 200,
    "success": True
}

def day_handler(message):
    sign = message.text
    text = "What do you want to know?\nChoose one: *TODAY*, *TOMMAROW*"
    sent_msg = bot.send_message(
        message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(
        sent_msg, fetch_horoscope, sign.capitalize())
def fetch_horoscope(message, sign):
    day = message.text
    horoscope = get_daily_horoscope(sign, day)
    data = horoscope["data"]
    horoscope_message = f'*Horoscope:* {data["horoscope_data"]}\\n*Sign:* {sign}\\n*Day:* {data["date"]}'
    bot.send_message(message.chat.id, "Here's  your horoscope!")
    bot.send_message(message.chat.id, horoscope_message, prase_mode="Markdown")
@bot.message_handler(func=lambda msg:True)
def echo_all(message):
    print("Received message:", message.text)
    print(message, "Bot is working")
    bot.reply_to(message, message.text)
    
bot.infinity_polling()