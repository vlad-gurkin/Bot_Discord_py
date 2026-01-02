import logging
import os

import discord
from discord.ext import commands

from Config.config import Config

config = Config()

# -------------------------------------------------
# Логирование (инициализируется ОДИН раз)
# -------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

logger = logging.getLogger(__name__)


class MyBot(commands.Bot):
    def __init__(self) -> None:
        # -------------------------------------------------
        # Intents
        # -------------------------------------------------
        intents = discord.Intents.default()
        intents.guilds = True
        intents.message_content = True

        super().__init__(
            command_prefix=commands.when_mentioned_or(config.bot.command_prefix),
            intents=intents,
            help_command=None
        )

    async def setup_hook(self) -> None:
        # -------------------------------------------------
        # Загрузка Cogs
        # -------------------------------------------------
        for root, _, files in os.walk("./cogs"):
            for file in files:
                if file.endswith(".py") and not file.startswith("_"):
                    path = os.path.join(root, file)
                    module = path.replace("\\", ".").replace("/", ".").replace(".py", "")
                    module = module.lstrip(".")

                    try:
                        await self.load_extension(module)
                        logger.info(f"Loaded cog: {module}")
                    except Exception:
                        logger.exception(f"Failed to load cog: {module}")
        # -------------------------------------------------
        # Синхронизация slash-команд
        # -------------------------------------------------
        guild = discord.Object(id=config.bot.guild_id)

        self.tree.copy_global_to(guild=guild)
        await self.tree.sync(guild=guild)

        logger.info("Слэш-команды синхронизированы.")

    async def on_ready(self) -> None:
        # -------------------------------------------------
        # Статус бота
        # -------------------------------------------------
        await self.change_presence(
            activity=discord.Game(name="/help")
        )

        logger.info(f"Logged in as {self.user} (ID: {self.user.id})")


# -------------------------------------------------
# Точка входа
# -------------------------------------------------
if __name__ == "__main__":
    bot = MyBot()
    bot.run(config.bot.token)
