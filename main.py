import os
import logging
from datetime import time, datetime, timezone, timedelta
from telegram import Update
from telegram.constants import ReactionEmoji
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.ERROR
)

async def goat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if 'candidates' not in context.chat_data:
        context.chat_data['candidates'] = []
    candidates = context.chat_data['candidates']

    value = update.message.text.partition(' ')[2]
    candidates.append(value)

    await update.message.set_reaction(reaction = ReactionEmoji.FIRE)

    if len(candidates) > 1:
        await schedulePoll(update, context)


async def schedulePoll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if 'job_poll' in context.chat_data:
        context.chat_data['job_poll'].schedule_removal()

    job_poll = context.job_queue.run_once(
        startPoll, 
        when=time(22, 00, tzinfo=timezone(timedelta(hours=1))),
        chat_id=update.effective_chat.id
    )

    context.chat_data['job_poll'] = job_poll


async def startPoll(context: ContextTypes.DEFAULT_TYPE):
    message = await context.bot.send_poll(
        context.job.chat_id,
        "Goat de hoy?",
        context.chat_data['candidates']
    )

    context.chat_data['poll'] = message
    
    context.job_queue.run_once(
        stopPoll, 
        when=time(23, 59, tzinfo=timezone(timedelta(hours=1))),
        chat_id=context.job.chat_id
    )


async def stopPoll(context: ContextTypes.DEFAULT_TYPE):
    context.bot.stop_poll(
        context.job.chat_id,
        context.chat_data['poll']
    )

    message = await context.bot.send_message(
        context.job.chat_id,
        'El premio GOAT de hoy va para:\n'
    )

    context.chat_data['candidates'] = []


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