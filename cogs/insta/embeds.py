from discord import Embed, File, Member, User

from database.general import Database as db
from models.insta_rank import Insta_Rank
from utils.configuration import EMOJIS
from utils.erros.database import User_Not_Found
from models.user import User as md_User

from myBot import MyBot
from utils.utils import Utils

async def setup(bot: MyBot):
    pass

class Embeds():
    def winner(winner: Member, likes: int, img_url: str) -> tuple[Embed, list[File]]:
        files = []
        embed = Embed(title="",
                      description=f"# <:heart:{EMOJIS['heart']}> **{likes}**\n\n{winner.mention} está mais perto de ter sua estrela na calçada da fama\n\n",
                    #   description=f"{winner.mention} está mais perto de ter sua estrela na calçada da fama\n\n",
                      color=0xBB1313)
        embed.set_thumbnail(url=Utils.emoji_url(id=EMOJIS['insta'],animated=True))
        embed.set_image(url=img_url)

        return embed, files