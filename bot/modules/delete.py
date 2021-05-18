from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, CallbackQuery
from bot.helper.mirror_utils.upload_utils.gdriveTools import GoogleDriveHelper
from bot.helper.telegram_helper.message_utils import *
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.ext_utils.bot_utils import new_thread
from bot import dispatcher


@new_thread
def delete_file(update, context) -> None:
    args = update.message.text.split(" ", maxsplit=1)
    mesid = update.message.message_id
    if len(args) > 1:
        link = args[1]
        keyboard = [
            [
                InlineKeyboardButton("Delete", callback_data='delme'),
                InlineKeyboardButton("Trash", callback_data='trashme'),
            ],
            [InlineKeyboardButton("Cancel", callback_data=f'canme-{mesid}')],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(
            f'<b>Choose to Delete/Trash | <code>{link}</code></b>', reply_markup=reply_markup, parse_mode='HTMl')
    else:
        sendMessage("Provide G-Drive Link to Delete.", context.bot, update)


@new_thread
def button(update, context) -> None:
    query = update.callback_query
    mes = query.message
    link = mes.text.split('|')[1].strip()
    query.answer()
    cb_data = query.data
    if not CustomFilters.owner_filter.filter(query):
        return
    gd = GoogleDriveHelper()
    if cb_data == "delme":
        editMessage(f'<b>Trying to Delete:</b> <code>{link}</code>', mes)
        result = gd.delete(link, trash=False)
        editMessage(result, mes)
    elif cb_data == "trashme":
        editMessage(f'<b>Trying to Trash:</b> <code>{link}</code>', mes)
        result = gd.delete(link)
        editMessage(result, mes)
    else:
        mesid = int(cb_data.split('-')[1])
        deleteMessage(context.bot, mes)
        context.bot.delete_message(chat_id=mes.chat_id, message_id=mesid)


dispatcher.add_handler(CommandHandler(BotCommands.DeleteCommand, delete_file, filters=CustomFilters.owner_filter))
dispatcher.add_handler(CallbackQueryHandler(button))
