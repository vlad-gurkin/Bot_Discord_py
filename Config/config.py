from environs import Env
from dataclasses import dataclass

@dataclass
class BotConfig:
    token: str
    command_prefix: str
    guild_id: int

@dataclass
class DataBaseConfig:
    host: str
    port: int
    user: str
    password: str
    database_name: str

class Config:
    def __init__(self):
        env = Env()
        env.read_env()

        self.bot = BotConfig(
            token=env.str("DISCORD_BOT_TOKEN"),
            command_prefix=env.str("COMMAND_PREFIX", default="$"),
            guild_id=env.int("GUILD_ID", default=1233415407876964402)
        )

        self.database = DataBaseConfig(
            host=env.str("DB_HOST", default="localhost"),
            port=env.int("DB_PORT", default=5432),
            user=env.str("DB_USER", default="user"),
            password=env.str("DB_PASSWORD", default="password"),
            database_name=env.str("DB_NAME", default="database")
        )

