#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext
from telegram import  InlineKeyboardButton, InlineKeyboardMarkup, Update

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

usersChatId = []

def start(update, context):
    usersChatId.append({'id' : update.message.chat.id, 'username': update.message.chat.username})
    
    startText = "Привет, поделись своим настроением на данный момент:"
    keyboard = [
        [
            InlineKeyboardButton("😁", callback_data='happy'),
            InlineKeyboardButton("🙂", callback_data='calm'),
            InlineKeyboardButton("😡", callback_data='angry')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(startText, reply_markup= reply_markup)

def help(update, context):
    update.message.reply_text('Help!')


def echo(update, context):
    update.message.reply_text(update.message.text)


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    kek = list({v['id']:v for v in usersChatId}.values())
    if (query.data == 'happy'):
        for user in kek:
            if (update.callback_query.message.chat.username):
                username = update.callback_query.message.chat.username
            else:
                username = "уэтогочеланетуюзернейма"
            mention = "["+username+"](tg://user?id="+str(update.callback_query.message.chat.id)+") feels happy rn"
            bot_msg = f"Hi, {mention}"
            context.bot.send_message(chat_id=user['id'], text=bot_msg, parse_mode="Markdown")


def main():
    updater = Updater("5123198039:AAF8R8Zhbep2Zmy_eEtNnt0qgl96V6rcn5E", use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()