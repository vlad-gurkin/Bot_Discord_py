import logging
import discord
from discord.ext import commands

logger = logging.getLogger(__name__)


class MemberEvents(commands.Cog):
    """События, связанные с участниками сервера"""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    # -------------------------------------------------
    # Event: пользователь зашёл на сервер
    # -------------------------------------------------
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member) -> None:
        logger.info(
            f"New member joined: {member} ({member.id}) "
            f"in guild {member.guild.name}"
        )

        # Пример: отправка приветствия в ЛС
        try:
            embed = discord.Embed(
                title="👋 Добро пожаловать!",
                description=(
                    f"Привет, {member.mention}!\n\n"
                    "Рады видеть тебя на сервере 😊"
                ),
                color=discord.Color.green()
            )
            await member.send(embed=embed)
        except discord.Forbidden:
            # Пользователь запретил ЛС
            logger.warning(f"Cannot DM member {member}")

        # Пример: сообщение в системный канал сервера
        if member.guild.system_channel:
            await member.guild.system_channel.send(
                f"🎉 Добро пожаловать, {member.mention}!"
            )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(MemberEvents(bot))
