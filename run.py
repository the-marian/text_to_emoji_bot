import logging
import os
from time import sleep

import telegram
from telegram.error import NetworkError, Unauthorized

from text_to_emoji import text_to_emoji

token = os.environ.get('BOT_TOKEN', '')


def response(bot: telegram.bot.Bot):
    """Echo the message the user sent."""
    global update_id
    # Request updates after the last update_id
    for update in bot.get_updates(offset=update_id, timeout=10):
        update_id = update.update_id + 1
        if update.message:  # your bot can receive updates without messages
            # Reply to the message
            message_text = update.message.text
            text_converted_to_emoji = text_to_emoji(message_text)
            update.message.reply_text(text_converted_to_emoji)


def main():
    """Run the bot."""
    global update_id
    # Telegram Bot Authorization Token
    bot = telegram.Bot(token)
    # get the first pending update_id, this is so we can skip over it in case
    # we get an "Unauthorized" exception.
    try:
        update_id = bot.get_updates()[0].update_id
    except IndexError:
        update_id = None

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    while True:
        try:
            response(bot)
        except NetworkError:
            sleep(1)
        except Unauthorized:
            # The user has removed or blocked the bot.
            update_id += 1


if __name__ == '__main__':
    main()
