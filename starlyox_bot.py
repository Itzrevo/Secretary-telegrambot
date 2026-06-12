import os
import telebot

tg_token = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(tg_token)

YOUR_USER_ID = "My_Telegram_ID"  # Replace with your actual Telegram user ID

def get_sender_name(user):
    if user.username:
        return f"@{user.username}"
    # Safe handling if last_name is missing/None
    last_name = user.last_name if user.last_name else ""
    return f"{user.first_name} {last_name}".strip()

# /forward command
@bot.message_handler(commands=['forward'])
def forward(message):
    # Guard against non-text commands
    text = message.text.replace("/forward", "").strip() if message.text else ""
    sender = get_sender_name(message.from_user)
    
    if text:
        bot.reply_to(message, "Message is now noted: " + text + ". I’ll deliver it to my human when he’s online.")
        bot.send_message(YOUR_USER_ID, f"From {sender}: {text}")
    else:
        bot.reply_to(message, "Message is now noted. I’ll deliver it to my human when he’s online.")
        bot.send_message(YOUR_USER_ID, f"From {sender}: [No text provided]")

# Default: any incoming message (Handles text, photos, stickers safely)
@bot.message_handler(func=lambda message: True, content_types=['text', 'photo', 'sticker', 'document'])
def handle_message(message):
    # Handle text messages
    if message.text:
        text = message.text.strip()
        if text.startswith("/"):
            return  # Skip because command handler takes care of it
    else:
        text = f"[{message.content_type} file]"

    sender = get_sender_name(message.from_user)
    bot.reply_to(message, "I'm StarlyXO, a secretary. I'm managing messages while my human is away./forward to forward massages to my human.")
    bot.send_message(YOUR_USER_ID, f"Status from {sender}: {text}")

print("Bot is now polling...")
bot.infinity_polling() # Better than polling() as it automatically restarts on network drops
