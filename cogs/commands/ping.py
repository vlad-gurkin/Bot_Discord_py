import discord
from discord.ext import commands
from discord import app_commands
import logging

logger = logging.getLogger(__name__)


class AdminsCommand(commands.Cog):
    """Административные команды бота"""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name="ping",
        description="Check the bot's latency"
    )

    async def ping(self, interaction: discord.Interaction) -> None:
        """
        Проверка задержки бота
        """
        latency_ms = round(self.bot.latency * 1000, 2)

        logger.info(
            f"/ping used by {interaction.user} "
            f"(guild={interaction.guild_id})"
        )

        await interaction.response.send_message(
            f"🏓 Pong! Latency: **{latency_ms} ms**",
            ephemeral=True
        )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(AdminsCommand(bot))
