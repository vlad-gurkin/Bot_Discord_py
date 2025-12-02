import discord
from discord.ext import commands
from Config.config import Config

intents = discord.Intents.default()
intents.message_content = True

config = Config()
bot = commands.Bot(command_prefix=config.bot.command_prefix, intents=intents)

class MyBot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)



@bot.tree.command(name="hello", description="Say hello", guild=discord.Object(id=config.bot.guild_id))
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("Hello!")


@bot.tree.command(name="ping", description="Check bot latency", guild=discord.Object(id=config.bot.guild_id))
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong! Latency: {bot.latency * 1000:.2f} ms")


@bot.event
async def on_ready():
    await bot.tree.sync(guild=discord.Object(id=config.bot.guild_id))

if __name__ == "__main__":
    bot.run(config.bot.token)