#!/usr/bin/env python
# -*- coding: utf-8 -*-


import logging
import sys
import yaml
from os import getenv
from argparse import ArgumentParser
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from random import randint, shuffle

MASTER_ID = 329117787
BOT_TOKEN = ''

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def collect_arguments():
    token_help = "specify bot token, default will be taken from BOT_TOKEN env"
    master_help = "specify ID of the master, user. this is used to limit access to commands"
    dict_help = "Specify path to your DICT file"

    bot_token = getenv("BOT_TOKEN", BOT_TOKEN)
    master_id = getenv("MASTER_ID", MASTER_ID)

    parser = ArgumentParser()
    parser.prog = "sstb"
    parser.version = 0.1
    parser.description = "Slava's Slave Telegram Bot, find it on \
                          https://github.com/vmindru/sstb/blob/master/dict.yaml"
    parser.add_argument('-T', '--token', default=bot_token, help=token_help)
    parser.add_argument('-m', '--master-id', default=master_id, help=master_help)
    parser.add_argument('-d', '--dict', default='dict.yaml', help=dict_help)
    args = parser.parse_args()
    return args


def help(bot, update):
    if update.message.from_user['id'] == MASTER_ID:
        update.message.reply_text('Hi master! you can do following:\n\
                                  /help: dispplay this message \n\
                                  /start: start the bot\n\
                                  /stop: stop the bot\n\
                                  /relaod_dict: reload the dictionary \n\
                                  have a nice day master!')
    else:
        update.message.reply_text('Greetings Stranger. you should ask more about me my master\
                                   or on github https://github.com/vmindru/sstb\
                                   only command you can run is\n\
                                   /help: displays this message')
    print update.message.chat


def start(bot, update):
    if update.message.from_user['id'] == MASTER_ID:
        update.message.reply_text('Hi master!, thank you for calling me. I will be tralling ALL\
                                  here')
    else:
        update.message.reply_text('Haxyu!!!')
    print update.message.chat


def stop(bot, update):
    if update.message.from_user['id'] == MASTER_ID:
        update.message.reply_text('No Master, please dont!')
    else:
        update.message.reply_text('Haxyu!!!')


def mod3():
    if randint(0, 100) % 3 == 0:
        return True
    else:
        return False


def echo(bot, update):
    """Echo the user message."""
    dict = bot.word_dict['dict']
    text = update.message.text
    from_user_name = update.message.from_user['first_name']
    is_bot = update.message.from_user['is_bot']
#    user_id = update.message.from_user['id']
    category = word_category(text, dict)

    def _reply(name, category):
        if category is not False:
            answers = dict[category]['answer']
            message = "{}: {}".format(name, answers[randint(0, len(answers)-1)])
            update.message.reply_text(message)
       #else: message = "{}: {}".format(name, "I feel emptiness in my libs,I think i am stupid ...")
        #    update.message.reply_text(message)
        else:
            print "nothing to reply to {} on {}".format(from_user_name, text)

    if is_bot is True:
        print "{} i don't talk to bots!!!!!".format(from_user_name)
    elif is_bot is False:
        _reply(from_user_name, category)
    else:
        print "Ignoring message from {}".format(update.message.from_user['first_name'])


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def word_category(text, dict):
    categorys = dict.keys()
    shuffle(categorys)
    print categorys
    for category in categorys:
        words = text.split(' ')
        shuffle(words)
        for word in words:
            if word.lower() in dict[category]['words']:
                print category
                return category
    return False


def load_dict(file):
    with open(file) as bytes:
        try:
            return yaml.load(bytes)
        except yaml.YAMLError as exc:
            print exc


def reload_dict(bot, update):
    if update.message.from_user['id'] == MASTER_ID:
        bot.__setattr__("word_dict", load_dict('dict.yaml'))
        update.message.reply_text('Hi master! i reloaded the dict. now {}'.format(bot.word_dict))


def main():
    """Start the bot."""
    args = collect_arguments()
    TOKEN = args.token
    DICT = args.dict
    updater = Updater(TOKEN)
    words = load_dict(DICT)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    updater.bot.__setattr__("word_dict", words)

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("stop", stop))
    dp.add_handler(CommandHandler("reload_dict", reload_dict))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # start_polling() is non-blocking and will stop the bot gracefully.
    print "wow"
    updater.idle()
    print "wow stop!"
    updater.stop()
    print "wow exit!"
    sys.exit()

if __name__ == '__main__':
    main()
