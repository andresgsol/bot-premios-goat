import os
import logging
from telegram import Update
from telegram.constants import ReactionEmoji
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

app_env = os.getenv('ENV', 'dev')
if app_env == 'prod':
    import config_prod as config
else:
    import config_dev as config

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.ERROR
)

async def goat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if 'candidates' not in context.chat_data:
        context.chat_data['candidates'] = []

    value = update.message.text.partition(' ')[2]
    context.chat_data['candidates'].append(value)

    await update.message.set_reaction(reaction = ReactionEmoji.FIRE)
    await schedulePoll(update, context)


async def schedulePoll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if 'job_poll' in context.chat_data:
        context.chat_data['job_poll'].schedule_removal()

    job_poll = context.job_queue.run_once(
        startPoll, 
        when=config.WHEN_START_POLL,
        chat_id=update.effective_chat.id
    )

    context.chat_data['job_poll'] = job_poll


async def startPoll(context: ContextTypes.DEFAULT_TYPE):
    context.chat_data.pop('job_poll')
    candidates = context.chat_data.pop('candidates')
    
    if len(candidates) == 1:
        await announceWinner(context, candidates)
        return

    message = await context.bot.send_poll(
        context.job.chat_id,
        "Goat de hoy?",
        candidates,
        is_anonymous=False
    )
    context.chat_data['poll'] = message

    context.job_queue.run_once(
        stopPoll, 
        when=config.WHEN_STOP_POLL,
        chat_id=context.job.chat_id
    )


async def stopPoll(context: ContextTypes.DEFAULT_TYPE):
    pollMessage = context.chat_data.pop('poll')
    poll = await context.bot.stop_poll(context.job.chat_id, pollMessage.id)

    pollOptions = poll.options
    max_votes = max(option['voter_count'] for option in pollOptions)
    winners = [option['text'] for option in pollOptions if option['voter_count'] == max_votes]  

    await context.bot.send_message(
        context.job.chat_id,
        'El premio GOAT de hoy va para:\n' + '\n'.join(winners)
    )


async def announceWinner(context: ContextTypes.DEFAULT_TYPE, winners):
    await context.bot.send_message(
        context.job.chat_id,
        'El premio GOAT de hoy va para:\n' + '\n'.join(winners)
    )


async def candidates(update: Update, context: ContextTypes.DEFAULT_TYPE):
    candidates = context.chat_data['candidates']
    await context.bot.send_message(
        update.effective_chat.id,
        'Los candidatos de hoy son:\n' + '\n'.join(candidates)
    )


if __name__ == '__main__':
    application = ApplicationBuilder().token(config.TOKEN).build()
    
    application.add_handler(CommandHandler('goat', goat))
    application.add_handler(CommandHandler('candidatos', candidates))
    
    application.run_polling()