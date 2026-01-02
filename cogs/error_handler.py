import logging
import discord
from discord.ext import commands
from discord import app_commands

from utils.embeds import ErrorEmbed

logger = logging.getLogger(__name__)


class ErrorHandler(commands.Cog):
    """Глобальный обработчик ошибок slash-команд (Embed версия)"""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.bot.tree.on_error = self.on_app_command_error

    async def on_app_command_error(
        self,
        interaction: discord.Interaction,
        error: app_commands.AppCommandError
    ) -> None:

        # -------------------------------------------------
        # Если ответ уже был отправлен
        # -------------------------------------------------
        if interaction.response.is_done():
            return

        # -------------------------------------------------
        # ❌ КАСТОМНЫЕ CHECK'И (доступ)
        # -------------------------------------------------
        if isinstance(error, app_commands.CheckFailure):
            embed = ErrorEmbed.base(
                title="Доступ запрещён",
                description="Данная команда доступна только определённым пользователям."
            )

            await interaction.response.send_message(
                embed=embed,
                ephemeral=True
            )

            logger.info(
                f"Access denied for user {interaction.user} "
                f"on command {interaction.command.name}"
            )
            return

        # -------------------------------------------------
        # ❌ Недостаточно прав Discord
        # -------------------------------------------------
        if isinstance(error, app_commands.MissingPermissions):
            embed = ErrorEmbed.base(
                title="Недостаточно прав",
                description="У вас нет прав для выполнения этой команды."
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        # -------------------------------------------------
        # ⏳ Кулдаун
        # -------------------------------------------------
        if isinstance(error, app_commands.CommandOnCooldown):
            embed = ErrorEmbed.base(
                title="Команда на перезарядке",
                description="Подождите немного перед повторным использованием."
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        # -------------------------------------------------
        # 🔥 ВСЁ ОСТАЛЬНОЕ — реальная ошибка
        # -------------------------------------------------
        logger.exception(
            "Unhandled app command error",
            exc_info=error
        )

        embed = ErrorEmbed.base(
            title="Внутренняя ошибка",
            description=(
                "Произошла непредвиденная ошибка.\n"
                "Администратор уже уведомлён."
            )
        )
        await interaction.response.send_message(
            embed=embed,
            ephemeral=True
        )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ErrorHandler(bot))
