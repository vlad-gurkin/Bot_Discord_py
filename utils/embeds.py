import discord


class ErrorEmbed:
    @staticmethod
    def base(
        title: str,
        description: str
    ) -> discord.Embed:
        return discord.Embed(
            title=f"⚠️ {title}",
            description=description,
            color=discord.Color.red()
        )
