import openai
from telegram import Update, MessageEntity
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

TELEGRAM_TOKEN = "8089023622:AAEUc8InFdHCCMw6tIjRJbqRFpIGdL0SiAY"
OPENAI_API_KEY = "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"

# Настройка клиента OpenAI
client = openai.OpenAI(api_key=OPENAI_API_KEY)

async def chatgpt_reply(prompt: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-4",  # или "gpt-3.5-turbo"
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1000
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Ошибка ChatGPT: {str(e)}"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message
    bot_username = context.bot.username

    if message.entities:
        for entity in message.entities:
            if entity.type == MessageEntity.MENTION:
                mention = message.text[entity.offset: entity.offset + entity.length]
                if mention.lower() == f"@{bot_username.lower()}":
                    user_input = message.text.replace(mention, "").strip()
                    if not user_input:
                        await message.reply_text("Что ты хотел спросить?")
                        return
                    await message.chat.send_chat_action(action="typing")
                    reply = await chatgpt_reply(user_input)
                    await message.reply_text(reply)
                    return

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    print("Бот запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()
