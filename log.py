import datetime

from discord.abc import GuildChannel
from discord.ext.commands import Bot
from discord import Embed, Enum, File, Message

class Embed_Colors(Enum):
    DEFAULT    = 0xbf0000 # darker red
    ERROR      = 0xff0000 # red
    MODERATION = 0x888888 # gray
    CALL       = 0xffff00 # yellow
    GUILD      = 0x00ff00 # green
    MEMBER     = 0x9d00ff # purple
    DEBUG      = 0x9d00ff # purple

class Terminal_Colors(Enum):
    RESET = "\x1b[0m"
    ERROR = "\x1b[31m"
    MODERATION = "\x1b[32m"
    CALL = "\x1b[33m"
    GUILD = "\x1b[36m"
    MEMBER = "\x1b[36m"
    DEBUG = "\x1b[34m"

class Log_Type(Enum):
    DEFAULT = 0
    ERROR = 1
    MODERATION = 2
    CALL = 3
    GUILD = 4
    MEMBER = 5
    DEBUG = 6

    def __str__(self):
        return f"{Terminal_Colors[self.name].value}{self.name}{Terminal_Colors.RESET.value}"

class Log():

    def __init__(self,
                 default: int | GuildChannel = None,
                 error: int | GuildChannel = None,
                 moderation: int | GuildChannel = None,
                 call: int | GuildChannel = None,
                 guild: int | GuildChannel = None,
                 member: int | GuildChannel = None,
                 debug: int | GuildChannel = None,
                 ):

        self.channels = {
            "default": default,
            "error": error,
            "moderation": moderation,
            "call": call,
            "guild": guild,
            "member": member,
            "debug": debug,
        }

    async def setup(self, bot: Bot):
        default = self.channels.get("default")

        if default is None:
            for channel in self.channels.values():
                if channel:
                    default = channel
                    break

        if default is None:
            raise ValueError("Must pass at least a default channel")

        for key, channel in self.channels.items():
            if channel is None:
                channel = default

            if isinstance(channel, int):
                channel = await bot.fetch_channel(channel)

            self.channels[key] = channel

    def print(self, type: Log_Type, message: str):
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{time} {type} {message}")

    async def embed(self, type: Log_Type, module: str, message:str, file: File= None) -> Message:
        embed = Embed(title=module,
                  description=message,
                  color=Embed_Colors[type.name].value,
                  timestamp=datetime.datetime.now())
        if file:
            embed.set_image(url=f"attachment://{file.filename}")

        channel = self.channels[type.name.lower()]
        if channel is None:
            raise Exception(f"{type.name} does not have channel associated")
        
        msg = await self.channels[type.name.lower()].send(embed=embed,file=file)

        if type in [Log_Type.ERROR,Log_Type.DEBUG]:
            self.print(type,
                       f"{module}: {message}")

        return msg