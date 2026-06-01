import os
import telebot
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

# --- Load Hugging Face model (lightweight for Railway free tier) ---
hf_token = os.getenv("HUGGINGFACE_TOKEN")
model_name = "distilgpt2"  # smaller model for stability

tokenizer = AutoTokenizer.from_pretrained(model_name, token=os.getenv("HUGGINGFACE_TOKEN"))
model = AutoModelForCausalLM.from_pretrained(model_name, token=os.getenv("HUGGINGFACE_TOKEN"))

generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

# --- Setup Telegram bot ---
tg_token = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(tg_token)

# Fetch bot account info
bot_info = bot.get_me()
acc_name = bot_info.first_name or bot_info.username

# --- Reply handler ---
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_text = message.text.strip()

    # Intro with dynamic account name + assurance for all messages
    intro = f"✉️ I’m {acc_name}, AI assistant. I’ll make sure all messages are delivered."

    # AI continuation
    response = generator(
        user_text,
        max_length=80,
        do_sample=True,
        top_p=0.9,
        temperature=0.7
    )[0]["generated_text"]

    bot.reply_to(message, intro + "\n\nReply: " + response)

print("Bot is now polling...")
bot.polling()
