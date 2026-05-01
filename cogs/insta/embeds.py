from discord import Embed, File, Member
from utils.configuration import EMOJIS


from myBot import MyBot
from utils.utils import Utils

async def setup(bot: MyBot):
    pass

class Embeds():
    def winner(winner: Member, likes: int, path: str, extension: str) -> tuple[Embed, list[File]]:
        files = []
        file = File(path, filename=f"winner.{extension}")
        files.append(file)
        
        embed = Embed(title="",
                      description=f"# <:heart:{EMOJIS['heart']}> **{likes}**\n\n{winner.mention} está mais perto de ter sua estrela na calçada da fama\n\n",
                    #   description=f"{winner.mention} está mais perto de ter sua estrela na calçada da fama\n\n",
                      color=0xBB1313)
        embed.set_thumbnail(url=Utils.emoji_url(id=EMOJIS['insta'],animated=True))
        embed.set_image(url=f"attachment://winner.{extension}")

        return embed, files