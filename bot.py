# -*- coding: utf-8 -*-
import logging
import os

from telegram import ChatAction
from telegram.ext.dispatcher import run_async
from telegram.ext import CommandHandler, Updater
import xkcd

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
HOST = os.environ.get("HOST", "169.233.106.165")
PORT = int(os.environ.get("PORT", 8443))

updater = Updater(token=TOKEN)


@run_async
def get_help(bot, update):
    """Prints accepted commands and help text."""
    bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    message = ""
    # Flatten list (https://stackoverflow.com/a/952946)
    for command in sum(updater.dispatcher.handlers.values(), []):
        message = message + "`/%s` %s\n" % (command.command[0], command.callback.__doc__)
    bot.send_message(chat_id=update.message.chat_id, text=message, parse_mode="Markdown")


@run_async
def get_latest(bot, update):
    """Shows the latest XKCD."""
    bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    comic = xkcd.getLatestComic()
    message = "*{title}* [#{number}]({link})\n{altText}".format(**comic.__dict__)
    bot.send_message(chat_id=update.message.chat_id, text=message, parse_mode="Markdown")


if __name__ == "__main__":
    updater.dispatcher.add_handler(CommandHandler('latest', get_latest))
    updater.dispatcher.add_handler(CommandHandler('help', get_help))

    updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)
    updater.bot.set_webhook("https://%s/%s" % (HOST, TOKEN))
    updater.idle()
