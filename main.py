import os
import logging
from datetime import date
from telegram import Update
from telegram.constants import ReactionEmoji
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def goat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    value = update.message.text.partition(' ')[2]
    context.chat_data[len(context.chat_data) + 1] = value
    await update.message.set_reaction(reaction = ReactionEmoji.FIRE)

async def candidates(update: Update, context: ContextTypes.DEFAULT_TYPE):
    candidatesText = ""
    for key, value in context.chat_data.items():
        candidatesText += f"\n{key}. {value}"
    await update.message.reply_html("Los candidatos de hoy son:" + candidatesText)

if __name__ == '__main__':
    application = ApplicationBuilder().token(os.environ['TELEGRAM_APITOKEN']).build()
    
    application.add_handler(CommandHandler('goat', goat))
    application.add_handler(CommandHandler('candidatos', candidates))
    
    application.run_polling()