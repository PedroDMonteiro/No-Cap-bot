import discord

from discord.ui import View, Modal, TextInput
from discord import Message

from cogs.insta.sqls import Database as db
from log import Log_Type
from models.insta import Insta

from myBot import MyBot
async def setup(bot: MyBot):
    pass

class Comment_Modal(Modal):
    def __init__(self, message:Message, view:View):
        self.message = message
        self.view = view
        self.database = db()
        
        super().__init__(title="Comentário")

    comment = TextInput(style=discord.TextStyle.short,
                       label="Reason:",
                       placeholder="Beleza divina",
                       required=True,
                       max_length=30)
    
    async def on_submit(self, interaction: discord.Interaction):
        try:
            comment_count = self.database.add_comment(message_id=interaction.message.id,
                                 user_id=interaction.user.id,
                                 comment=self.comment.value,)
        except Exception as err:
            await interaction.response.send_message("Erro ao mandar comentário",ephemeral=True)
            await interaction.client.log.embed(type=Log_Type.ERROR,module="(Insta) Comentário",message=f"Erro ao tentar comentar:{err}")
            return
        
        comment = [child for child in self.view.children if child.custom_id=="btn_comment"][0]
        comment.label = str(comment_count)
        
        insta: Insta = self.database.get_by_message_id(interaction.message.id)
        ower = interaction.client.get_user(insta.user_id)

        await ower.send(f'{interaction.user} comentou na sua foto\n{interaction.message.jump_url}')
        await interaction.response.send_message("Comentário enviado",ephemeral=True)

        await self.message.edit(content=self.message.content,view=self.view)

    
    async def on_timeout(self):
        return await super().on_timeout()

    async def on_error(self, interaction, error):
        return await super().on_error(interaction, error)