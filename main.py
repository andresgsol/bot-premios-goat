import os
import logging
from datetime import time, datetime
from telegram import Update
from telegram.constants import ReactionEmoji
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def goat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if 'candidates' not in context.chat_data:
        context.chat_data['candidates'] = []
    candidates = context.chat_data['candidates']

    value = update.message.text.partition(' ')[2]
    candidates.append(value)

    await update.message.set_reaction(reaction = ReactionEmoji.FIRE)

    if len(candidates) == 2:
        await startPoll(update, context)


async def startPoll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = await context.bot.send_poll(
        update.effective_chat.id,
        'Premios GOAT ' + datetime.today().strftime('%d-%m-%Y'), 
        context.chat_data['candidates']
    )
    context.chat_data['poll'] = message.message_id
    # name = update.effective_chat.full_name 
    # context.job_queue.run_once(giveAwards, when=time.fromisoformat('23:59:00'), data=name, chat_id=chat_id)

async def candidates(update: Update, context: ContextTypes.DEFAULT_TYPE):
    candidatesString = ""
    for candidate in context.chat_data['candidates']:
        candidatesString += '\n' + candidate
    await update.message.reply_html("Los candidatos de hoy son:" + candidatesString)

async def giveAwards(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=context.job.chat_id, text="And the winner is...")

if __name__ == '__main__':
    application = ApplicationBuilder().token(os.environ['TELEGRAM_APITOKEN']).build()
    
    application.add_handler(CommandHandler('goat', goat))
    application.add_handler(CommandHandler('candidatos', candidates))
    
    application.run_polling()