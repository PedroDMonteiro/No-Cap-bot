from discord import Interaction, ButtonStyle
from discord.ui import Button, View

from log import Log_Type
from utils.erros.database import Primary_Key_Duplicate

from cogs.insta.sqls import Database as db
from cogs.insta.modals import Comment_Modal

from models.insta import Insta

from utils.view import Ok_Cancelar_View

from myBot import MyBot

async def setup(bot: MyBot):
    pass

class Post(View):
    like_emoji = '<:heart:1412875866039521410>'
    comment_emoji = '<:chat:1416517138457432187>'

    def __init__(self):
        self.database = db()
        super().__init__(timeout=None)

        like = Button(label="0",
                      emoji=Post.like_emoji,
                      style= ButtonStyle.gray,
                      custom_id=f"btn_like",
                      )
        like.callback = self.like_callback
        self.add_item(like)

        comment = Button(label="0",
                         emoji=Post.comment_emoji,
                         style= ButtonStyle.gray,
                         custom_id=f"btn_comment",
                         )
        comment.callback = self.comment_callback
        self.add_item(comment)

        info = Button(emoji="<:3_dots:1416516004372021388>",
                        style= ButtonStyle.gray,
                        custom_id=f"btn_info",
                        )
        info.callback = self.info_callback
        self.add_item(info)

        delete = Button(emoji="<:trash:1412876222039588996>",
                        style= ButtonStyle.gray,
                        custom_id=f"btn_delete",
                        )
        delete.callback = self.delete_callback
        self.add_item(delete)

    async def like_callback(self, interaction: Interaction):
        like = [child for child in self.children if child.custom_id=="btn_like"][0]

        try:
            like_count = self.database.add_like(message_id=interaction.message.id,
                                       user_id=interaction.user.id)
            like.label = str(like_count)
            await interaction.response.edit_message(content=interaction.message.content,view=self)

        except Primary_Key_Duplicate as err:
            await interaction.response.send_message('Você já votou',ephemeral=True)
        except Exception as err:
            print(type(err))
            await interaction.response.send_message("Erro ao dar like",ephemeral=True)
            await interaction.client.log.embed(type=Log_Type.ERROR,module="(Insta) Like",message=f"Erro ao tentar comentar:{err}")

    async def comment_callback(self, interaction: Interaction):
        try:
            await interaction.response.send_modal(Comment_Modal(message=interaction.message,view=self))
            #log new comment
        except Exception as err:
            await interaction.response.send_message("Erro ao mandar comentário",ephemeral=True)
            await interaction.client.log.embed(type=Log_Type.ERROR,module="(Insta) Comentário",message=f"Erro ao tentar comentar:{err}")


    async def info_callback(self, interaction: Interaction):
        try:
            insta: Insta = self.database.get_by_message_id(message_id=interaction.message.id)

            likes_text = f'{Post.like_emoji} **Likes**\n'
            if len(insta.likes) == 0:
                likes_text += 'Sem likes ainda'
            else:
                likes_text += '\n'.join([f'<@{user_id}>' for user_id in insta.likes])

            comments_text = f'{Post.comment_emoji} **Comentários**:\n'
            if len(insta.comments) == 0:
                comments_text += 'Sem comentários ainda'
            else:
                comments_text += '\n'.join([f'<@{comment.user_id}>: {comment.content}' for comment in insta.comments])

            await interaction.response.send_message(likes_text+'\n'+comments_text,ephemeral=True)
        except Exception as err:
            await interaction.client.log.embed(type=Log_Type.ERROR,module="(Insta) Info",message=f"Erro ao mostrar info do post:{err}")

    async def delete_callback(self, interaction: Interaction):
        insta: Insta = self.database.get_by_message_id(message_id=interaction.message.id)
        if interaction.user.id != insta.user_id:
            if not interaction.user.guild_permissions.administrator:
                # await interaction.message.reply("Você não tem permissão para apagar esta messagem",ephemeral=True)
                await interaction.response.send_message("Você não tem permissão para deletar esta messagem",ephemeral=True)
                return
        try:
            view = Ok_Cancelar_View(interaction_user_id=interaction.user.id)
            # view.message = await interaction.response.send_message("Tem certeza que deseja deletar esta foto?\n-# Isso é irreversível",view=view,ephemeral=True)
            await interaction.response.send_message("Tem certeza que deseja deletar esta foto?\n-# Isso é irreversível",view=view,ephemeral=True)
            view.message = await interaction.original_response()
            
            await view.wait()
            if not view.confirmed:
                return
            
            self.database.delete(message_id=interaction.message.id)
            await interaction.message.delete()
        except Exception as err:
            await interaction.client.log.embed(type=Log_Type.ERROR,module="(Insta) Deletar",message=f"Erro ao tentar deletar post:{err}")