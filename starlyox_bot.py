import os
import telebot
from transformers import pipeline

# Load Telegram token from Railway environment variable
bot = telebot.TeleBot(os.getenv("TELEGRAM_BOT_TOKEN"))

# Get bot's own profile info (dynamic name)
me = bot.get_me()
owner_name = me.first_name if me.first_name else me.username

# Smarter lightweight AI model
generator = pipeline("text-generation", model="TinyLlama/TinyLlama-1.1B-Instruct")

SAFEWORDS = ["violence", "hate", "kill", "drugs"]

@bot.message_handler(func=lambda message: True)
def reply(message):
    user_text = message.text

    # Generate AI reply
    ai_output = generator(
        f"Secretary reply to: {user_text}",
        max_length=80,
        num_return_sequences=1
    )[0]['generated_text']

    # Safety filter
    if any(word in ai_output.lower() for word in SAFEWORDS):
        ai_output = "I cannot answer that."

    # Secretary-style tone with dynamic name
    secretary_reply = (
        f"✉️ Hello, I’m {owner_name}’s secretary.\n"
        f"I’ve noted your message: \"{user_text}\".\n"
        f"I’ll make sure {owner_name} sees it soon.\n\n"
        f"Quick reply: {ai_output}"
    )

    bot.reply_to(message, secretary_reply)

bot.infinity_polling()
