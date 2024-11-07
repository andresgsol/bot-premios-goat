import os
import logging
from datetime import time
from telegram import Update
from telegram.constants import ReactionEmoji
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def goat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.chat_data) == 0:
        initDay(update, context)
    value = update.message.text.partition(' ')[2]
    context.chat_data[len(context.chat_data) + 1] = value
    await update.message.set_reaction(reaction = ReactionEmoji.FIRE)

def initDay(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    name = update.effective_chat.full_name
    context.job_queue.run_once(giveAwards, when=time.fromisoformat('23:59:00'), data=name, chat_id=chat_id)

async def candidates(update: Update, context: ContextTypes.DEFAULT_TYPE):
    candidatesText = ""
    for key, value in context.chat_data.items():
        candidatesText += f"\n{key}. {value}"
    await update.message.reply_html("Los candidatos de hoy son:" + candidatesText)

async def giveAwards(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=context.job.chat_id, text="And the winner is...")

if __name__ == '__main__':
    application = ApplicationBuilder().token(os.environ['TELEGRAM_APITOKEN']).build()
    
    application.add_handler(CommandHandler('goat', goat))
    application.add_handler(CommandHandler('candidatos', candidates))
    
    application.run_polling()