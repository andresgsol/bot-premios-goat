import os
import logging
from telegram import Update
from telegram.constants import ReactionEmoji
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def goat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.set_message_reaction(chat_id=update.effective_chat.id, message_id=update.effective_message.id, reaction=ReactionEmoji.FIRE)

if __name__ == '__main__':
    application = ApplicationBuilder().token(os.environ['TELEGRAM_APITOKEN']).build()
    
    start_handler = CommandHandler('goat', goat)
    application.add_handler(start_handler)
    
    application.run_polling()