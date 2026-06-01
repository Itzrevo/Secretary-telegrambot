import os
import telebot
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

# --- Load Hugging Face model ---
hf_token = os.getenv("HUGGINGFACE_TOKEN")
model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"  # adjust if using another repo

tokenizer = AutoTokenizer.from_pretrained(model_name, token=hf_token)
model = AutoModelForCausalLM.from_pretrained(model_name, token=hf_token)

generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

# --- Setup Telegram bot ---
tg_token = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(tg_token)

# --- Secretary-style reply handler ---
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_text = message.text.strip()

    # Generate AI reply
    response = generator(
        f"Secretary-style reply to: {user_text}",
        max_length=120,
        do_sample=True,
        top_p=0.9,
        temperature=0.7
    )[0]["generated_text"]

    # Clean response (avoid echoing prompt)
    if response.startswith("Secretary-style reply to:"):
        response = response.replace("Secretary-style reply to:", "").strip()

    # Send back to user
    bot.reply_to(message, f" StarlyXO: {response}")

# --- Keep bot running ---
print("Bot is now polling...")
bot.polling()
