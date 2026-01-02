import logging
import aiohttp
import discord
from discord.ext import commands
from discord import app_commands

logger = logging.getLogger(__name__)

CAT_API_URL = "https://api.thecatapi.com/v1/images/search"
ALLOWED_USERS = {1390719059275813006, 372461596322168832}


def is_allowed_user(interaction: discord.Interaction) -> bool:
    return interaction.user.id in ALLOWED_USERS


class CatCommand(commands.Cog):
    """Команды с котиками 🐱"""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.check(is_allowed_user)
    @app_commands.command(
        name="случайнный_котик",
        description="Получить случайное фото котика 🐾"
    )
    async def cat(self, interaction: discord.Interaction) -> None:
        # ⏳ Говорим Discord'у, что думаем (иначе таймаут)
        await interaction.response.defer()

        async with aiohttp.ClientSession() as session:
            async with session.get(CAT_API_URL) as response:
                if response.status != 200:
                    raise RuntimeError("Cat API is unavailable")

                data = await response.json()

        image_url = data[0]["url"]

        embed = discord.Embed(
            title="🐱 Случайный котик",
            color=discord.Color.orange()
        )
        embed.set_image(url=image_url)
        embed.set_footer(text="А какой ты сегодня котик?🐾")

        await interaction.followup.send(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(CatCommand(bot))
