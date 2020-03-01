import logging
from io import BytesIO
from configparser import SectionProxy

from telegram.ext import Updater
from telegram import ParseMode


class TelegramClient:

    def __init__(self, config: SectionProxy):
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=logging.INFO)
        self.logger = logging.getLogger("Telegram")

        telegram_api_token = config["API_TOKEN"]
        self._updater = Updater(telegram_api_token, use_context=True)


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
