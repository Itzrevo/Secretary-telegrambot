import os
import telebot
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline

# --- Hugging Face setup ---
hf_token = os.getenv("HUGGINGFACE_TOKEN")
model_name = "google/flan-t5-small"  # secretary-style, lightweight

tokenizer = AutoTokenizer.from_pretrained(model_name, token=hf_token)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name, token=hf_token)

generator = pipeline("text2text-generation", model=model, tokenizer=tokenizer)

# --- Telegram bot setup ---
tg_token = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(tg_token)

bot_info = bot.get_me()
acc_name = bot_info.first_name or bot_info.username

# --- Reply handler ---
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_text = message.text.strip()

    intro = f"✉️ I’m {acc_name}, AI assistant. I’ll make sure all messages are delivered."

    # Secretary-style polite reply
    response = generator(
        f"Provide a polite secretary-style reply to: {user_text}",
        max_length=80
    )[0]["generated_text"]

    bot.reply_to(message, intro + "\n\nReply: " + response)

print("Bot is now polling...")
bot.polling()
