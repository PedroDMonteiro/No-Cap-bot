from discord.ext import commands
from discord.ext.commands.context import Context

from utils.configuration import DEVS

def is_developer():
    async def predicate(ctx: Context):
        if ctx.author.id not in DEVS:
            raise commands.CheckFailure("Not dev")

        return True
    
    return commands.check_any(commands.check(predicate),)

def is_adm():
    async def predicate(context: Context):
        if context.guild is None:
            return True
        
        if not context.author.guild_permissions.administrator:
            raise commands.CheckFailure("Not adm")

        return True
    
    return commands.check_any(commands.check(predicate),)

def is_banker():
    async def predicate(context: Context):
        cog = context.bot.get_cog("Economy")
        bankers = getattr(cog, "bankers")

        if context.author.id in bankers:
            raise commands.CheckFailure("Not banker")
        
        return True
    
    return commands.check_any(commands.check(predicate),is_adm())