import logging
from io import BytesIO
from configparser import SectionProxy

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ParseMode


class TelegramClient:

    def __init__(self, config: SectionProxy):
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=logging.INFO)
        self.logger = logging.getLogger("Telegram")

        telegram_api_token = config["API_TOKEN"]
        self._updater = Updater(telegram_api_token, use_context=True)

        dp = self._updater.dispatcher
        # on different commands - answer in Telegram
        dp.add_handler(CommandHandler("start", self._start))
        dp.add_handler(CommandHandler("help", self._help))

        # on noncommand i.e message - echo the message on Telegram
        dp.add_handler(MessageHandler(Filters.text, self._echo))

        # log all errors
        dp.add_error_handler(self._error)

    def _start(self, update, context):
        """Send a message when the command /start is issued."""
        update.message.reply_text('Hi!')

    def _help(self, update, context):
        """Send a message when the command /help is issued."""
        update.message.reply_text('Help!')

    def _echo(self, update, context):
        update.message.reply_text(update.message.text)

    def _error(self, update, context):
        """Log Errors caused by Updates."""
        self.logger.warning('Update "%s" caused error "%s"', update, context.error)

    def send_text(self, chat_id: int, text: str) -> None:
        self._updater.bot.send_message(
            chat_id=chat_id,
            text=text,
            parse_mode=ParseMode.MARKDOWN
        )

    def send_audio(self, chat_id: int, audio: BytesIO) -> None:
        self._updater.bot.send_audio(
            chat_id=chat_id,
            audio=audio
        )

    def startup(self):
        # Start the Bot
        self._updater.start_polling()

        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        self._updater.idle()
