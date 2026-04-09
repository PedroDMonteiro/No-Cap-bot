from io import BytesIO

from discord.ext import commands
from discord.ext.commands.context import Context

from discord import DMChannel, Embed, Emoji, File, Member, Message, Role

from myBot import MyBot
from utils.cog import Cog

async def setup(bot: MyBot):
    await bot.add_cog(Cog_Configuration(bot))

class Cog_Configuration(Cog, name = "Configuration"):
    @commands.Cog.listener()
    async def on_member_join(self, member: Member):
        member.joined_at
        print(f'{member.name} entrou ({member.id})')

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if message.content:
                if message.content == f'<@{self.bot.user.id}>':
                    await message.channel.send(f"## Meu prefixo é `nc!`\n-# Use `nc!help` para mais informações")
                    return 

    @commands.group(name="role",aliases=[],invoke_without_command=True)
    async def role(self, context: Context, role: Role):
        embed = Embed(title=role.name,description=role.mention)
        if role.color:
            embed.color = role.color
        if role.icon:
            embed.set_thumbnail(url=role.icon.url)
        embed.set_footer(text=f"ID: {role.id}")
        embed.add_field(name="Members",value=len(role.members),inline=False)
        embed.add_field(name="Color",value=role.color,inline=False)
        embed.add_field(name="Mencionable",value="Yes" if role.mentionable else "No",inline=False)
        
        await context.reply(embed=embed,mention_author=False)

    @role.command(name="icon",aliases=[])
    async def role_icon(self, context: Context, role: Role, reset: str = None):
        embed = Embed(title="Role Icon",description=f"{role.mention}")
        if role.color:
            embed.color = role.color

        if role.icon is None:
            if len(context.message.attachments) == 0:
                embed.add_field(name=f"Role don't have icon",value="")
                await context.reply(embed=embed)
                return
        
        if len(context.message.attachments) > 0:
            await role.edit(display_icon=(await context.message.attachments[0].read()))

        resets = ["reset","remove","delete"]
        if reset:
            if reset.lower() in resets:
                await role.edit(display_icon=None)

                embed.add_field(name=f"Icon removed",value="")
                await context.reply(embed=embed)
                return

        role = context.guild.get_role(role.id)
        extension = "png"
        if role.icon._animated:
            extension = "gif"

        icon_file = await role.icon.to_file(filename=f"icon.{extension}")

        embed.set_image(url=f"attachment://icon.{extension}")
        await context.reply(embed=embed,files=[icon_file])

    @role.command(name="color",aliases=[])
    async def role_color(self, context: Context, role: Role, color: str):
        color = color.lower()
        colors = {"white":"#ffffff",
                  "gray":"#3d3d3d",
                  "black":"#000000",
                  "red":"#ff0000",
                  "yellow":"#dddd00",
                  "orange":"#ff8800",
                  "brown":"#aa4400",
                  "pink":"#dd00dd",
                  "purple":"#770077",
                  "green":"#00bb00",
                  "blue":"#0000bb",
                  "cian":"#00ffff",
                  }
        await role.edit(color=color)
        await context.reply("Color updated")

    @commands.command()
    async def ping(self, context: Context):
        await context.send(f"Pong {round(self.bot.latency * 1_000)}ms.")

    @commands.command()
    async def mute(self, context: Context, user: Member):
        await context.send(f"{user} mutado")

    @commands.command()
    async def adm(self, context: Context):
        if context.author.guild_permissions.administrator:
            await context.send(f"Você tem perm de adm")
            return

        await context.send(f"Você não tem perm de adm")

    @commands.group(name="emoji",aliases=[],invoke_without_command=True)
    async def emoji(self, context: Context, emoji:Emoji|str):
        if isinstance(context.channel,DMChannel):
            await context.reply("Command guild only")
            return
        
        if isinstance(emoji,str):
            emoji = emoji.lower()
            emojis = [e for e in context.guild.emojis if e.name.lower() == emoji]
            if len(emojis) == 0:
                await context.reply(f"`{emoji}` not found")
                return
            emoji = emojis[0]

        await context.send(f"`{emoji.url}`")
        extension = "png"
        if emoji.animated:
            extension = "gif"

        buffer = BytesIO(await emoji.read())
        buffer.seek(0)
        icon_file = File(fp=buffer,filename=f"{emoji.name}.{extension}")
        embed= Embed(title=emoji.name)
        embed.set_image(url=f"attachment://{icon_file.filename}")

        await context.reply(embed=embed,files=[icon_file])