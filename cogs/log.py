import datetime
import discord
from discord.ext import commands
from discord.ext.commands.context import Context
from discord.ext.commands import Bot,Cog

from discord import Client, Embed, Interaction, Member,Message

from myBot import MyBot
from utils.configuration import INSTA_LOG_CHANNERL_ID

class Message():
    def __init__(self):
        pass

    def error(content: str):
        print()


class Log():
    error_color =   0xff0000 # red
    sucess_color =  0x00ff00 # green
    warning_color = 0xffff00 # yellow
    info_color =    0x888888 # gray
    
    message = Message()

    embed = Embed()

    def __init__(self, bot: MyBot):
        self.bot = bot
        self.error_channel = self.bot.get_channel()

    @commands.Cog.listener()
    async def on_error():
        pass

async def error(module: str, err: Exception, sub_module: str = None):
    ...

async def info(module: str):
    ...

async def insta_like(interaction: Interaction, err: Exception):
    log_insta = interaction.client.get_channel(INSTA_LOG_CHANNERL_ID)

    embed = Embed(title='Insta',
                  description='Like',
                  color=Log.error_color,
                  timestamp=datetime.datetime.now(),)
    embed.set_thumbnail(url=interaction.user.avatar.url)
    embed.add_field(name='usuário',value=f'{interaction.user}')
    embed.add_field(name='messagem',value=f'{interaction.message.jump_url}')
    embed.add_field(name=f'{type(err)}',value=f'{err}')
    embed.set_footer(text=f'ID:{interaction.user.id}')

    await log_insta.send(embed=embed)

async def insta_comment_error(interaction: Interaction,comment: str, err: Exception):
    log_insta = interaction.client.get_channel(INSTA_LOG_CHANNERL_ID)
    embed = Embed(title='Insta',
                  description='Comentário',
                  color=Cog_Log.error_color,
                  timestamp=datetime.datetime.now(),)
    embed.set_thumbnail(url=interaction.user.avatar.url)
    embed.add_field(name='Usuário',value=f'{interaction.user}',inline=False)
    embed.add_field(name='Comentário',value=f'{comment}',inline=False)
    embed.add_field(name='messagem',value=f'{interaction.message.jump_url}',inline=False)
    embed.add_field(name='Erro',value=f'{err}',inline=False)
    embed.set_footer(text=f'ID:{interaction.user.id}')

    await log_insta.send(embed=embed)

async def insta_delete_error(interaction: Interaction, err: Exception):
    log_insta = interaction.client.get_channel(INSTA_LOG_CHANNERL_ID)

    embed = Embed(title='Insta',
                  description='Delete',
                  color=Cog_Log.error_color,
                  timestamp=datetime.datetime.now(),)
    embed.set_thumbnail(url=interaction.user.avatar.url)
    embed.add_field(name='usuário',value=f'{interaction.user}')
    embed.add_field(name='messagem',value=f'{interaction.message.jump_url}')
    embed.add_field(name='erro',value=f'{err}')
    embed.set_footer(text=f'ID:{interaction.user.id}')

    await log_insta.send(embed=embed)