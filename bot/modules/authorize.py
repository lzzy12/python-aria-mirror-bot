from bot.helper.telegram_helper.message_utils import sendMessage
from telegram.ext import run_async
from bot import AUTHORIZED_CHATS, OWNER_ID, dispatcher
from telegram.ext import CommandHandler
from bot.helper.telegram_helper.filters import CustomFilters
from telegram.ext import Filters
from telegram import Update
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot import redis_client, redis_authorised_chats_key
import re


def _authorize(id: int, context, update: Update):
    chat_id = str(id)
    salutation =  'user' if id > 0 else 'chat'
    if chat_id not in AUTHORIZED_CHATS:
        redis_client.sadd(redis_authorised_chats_key, chat_id)
        AUTHORIZED_CHATS.add(chat_id)
        msg = f'Authorized {salutation}'
    else:
        msg = f'Already authorized {salutation}'
    sendMessage(msg, context.bot, update)
@run_async
def authorize(update: Update,context):
    reply_message = update.message.reply_to_message
    msg_split = update.message.text.split(' ')
    msg_args = None
    match = None
    if len(msg_split) > 1:
        msg_args = msg_split[1:]
    if msg_args is not None and len(msg_args) > 0:
        match = re.search(r'^-?[0-9]\d*(\.\d+)?$', msg_args[0])
    
    if (match is not None):
        chat_id = int(match.group(0))
        _authorize(chat_id, context, update)
    elif reply_message is None:
        if update.message.chat.id == OWNER_ID:
            sendMessage("No sense in authorizing yourself, silly!", context.bot, update)
            return
        # Trying to authorize a chat
        chat_id = update.effective_chat.id
        _authorize(chat_id, context, update)
    else:
        # Trying to authorize someone in specific
        user_id = reply_message.from_user.id
        _authorize(user_id, context, update)

def _unauthorize(id: int, context, update):
    chat_id = str(id)
    salutation =  'user' if id > 0 else 'chat'
    if chat_id in AUTHORIZED_CHATS:
        redis_client.srem(redis_authorised_chats_key, chat_id)
        AUTHORIZED_CHATS.remove(chat_id)
        msg = f'Unauthorized {salutation}'
    else:
        msg = f'Already unauthorized {salutation}'
    sendMessage(msg, context.bot, update)
@run_async
def unauthorize(update,context):
    reply_message = update.message.reply_to_message
    msg_split = update.message.text.split(' ')
    msg_args = None
    match = None
    if len(msg_split) > 1:
        msg_args = msg_split[1:]
    if msg_args is not None and len(msg_args) > 0:
        match = re.search(r'^-?[0-9]\d*(\.\d+)?$', msg_args[0])
    msg = ''
    if match is not None:
        chat_id = int(match.group(0))
        _unauthorize(chat_id, context, update)
    elif reply_message is None:
        if update.message.chat.id == OWNER_ID:
            sendMessage("No sense in unauthorizing yourself, silly!", context.bot, update)
            return
        # Trying to unauthorize a chat
        chat_id = update.effective_chat.id
        _unauthorize(chat_id, context, update)
    else:
        # Trying to authorize someone in specific
        user_id = reply_message.from_user.id
        _unauthorize(user_id, context, update)


authorize_handler = CommandHandler(command=BotCommands.AuthorizeCommand, callback=authorize,
                                   filters=CustomFilters.owner_filter)
unauthorize_handler = CommandHandler(command=BotCommands.UnAuthorizeCommand, callback=unauthorize,
                                     filters=CustomFilters.owner_filter)
dispatcher.add_handler(authorize_handler)
dispatcher.add_handler(unauthorize_handler)