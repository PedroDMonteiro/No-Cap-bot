import discord
from discord import Interaction, Message
from discord.ui import View as View_dc, Button
from discord.interactions import InteractionCallbackResponse

class View(View_dc):
    def __init__(self, timeout: float = 20):
        super().__init__(timeout=timeout)
        self.interaction_users_ids: list[int]
        self.message: Message
        self.response: any

        # message that change views, only the view on top of stack will modify
        self.in_background = False

    def in_front(func):
        async def wrapper(self):
            if self.in_background:
                self.stop()
                return
            await func(self)
        return wrapper
    
    #on click of a button
    def can_interact(func):
        async def wrapper(self, interaction: Interaction, *args):
            if interaction.user.id not in self.interaction_users_ids:
                await interaction.response.send_message(content="Você não pode usar isso.",ephemeral=True)
                return
            await func(self, interaction, *args)
        return wrapper
    
    async def on_timeout(self) -> None:
        if self.in_background:
            self.stop()

class Message_on_Timeout_View(View):
    def __init__(self, timeout: float | None = 20):
        super().__init__(timeout=timeout)

    @View.in_front
    async def on_timeout(self) -> None:
        self.stop()

class My_Button(View):
    def __init__(self):
        super().__init__()

    @View.in_front
    async def on_timeout(self) -> None:
        for item in self.children:
            if type(item) == Button:
                item.disabled = True
        await self.message.edit(view=self)
        self.stop()

    @View.can_interact
    async def update_message(self, interaction:Interaction):
        pass

class Ok_Cancelar_Buttons(My_Button,Message_on_Timeout_View):
    def __init__(self):
        super().__init__()
        self.confirmed = False
        confirm = Button(label="Ok",
                         custom_id="confirm",
                         style= discord.ButtonStyle.success)
        confirm.callback = self.on_confirm
        self.add_item(confirm)

        cancel = Button(label="Cancelar",
                        custom_id="cancel",
                        style= discord.ButtonStyle.danger)
        cancel.callback = self.on_cancel
        self.add_item(cancel)

    @View.can_interact
    async def on_confirm(self, interaction: Interaction):
        await self.message.edit(content=f"{self.message.content}\nConfirmado",view=None)
        self.confirmed = True
        self.stop()

    @View.can_interact
    async def on_cancel(self, interaction: Interaction):
        await self.message.edit(content=f"{self.message.content}\nCancelado",view=None)
        self.stop()

class Ok_Cancelar_View(Ok_Cancelar_Buttons):
    def __init__(self, interaction_user_id: int):
        super().__init__()
        self.interaction_users_ids = [interaction_user_id]

class Sim_Nao_Buttons(Ok_Cancelar_Buttons):
    def __init__(self):
        super().__init__()
        button = [b for b in  self.children if b.custom_id == "confirm"][0]
        button.label = "Sim"

        button = [b for b in  self.children if b.custom_id == "cancel"][0]
        button.label = "Não"

class Sim_Nao_View(Sim_Nao_Buttons):
    def __init__(self, interaction_user_id: int):
        super().__init__()
        self.interaction_users_ids = [interaction_user_id]      