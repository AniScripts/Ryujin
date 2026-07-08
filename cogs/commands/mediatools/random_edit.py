import nextcord
from nextcord.ext import commands
import random
from cogs.utils.base import RyujinCog

class RandomEditCog(RyujinCog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name="random_edit",
        description="Sends a random edit. Good command if you don't have ideas what to edit.",
    )
    async def random_edit(self, interaction: nextcord.Interaction):
        if await self.blacklist_guard(interaction):
            return

        with open("edits.txt", "r") as f:
            lines = f.read().strip().split("\n")
        
        link = random.choice(lines)
        button_view = AnotherButtonEdit()
        await self.bot.maybe_send_ad(interaction)
        await interaction.send(link, ephemeral=True, view=button_view)

class AnotherButtonEdit(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(nextcord.ui.Button(
            style=nextcord.ButtonStyle.gray,
            label="Another Edit 👀",
            custom_id="another_edit"
        ))
    @nextcord.ui.button(
        style=nextcord.ButtonStyle.gray,
        label="Another Edit",
        custom_id="another_edit"
    )
    async def another_edit(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        with open("edits.txt", "r") as f:
            lines = f.read().strip().split("\n")
        new_link = random.choice(lines)
        await interaction.response.edit_message(content=new_link, view=self)

def setup(bot):
    bot.add_cog(RandomEditCog(bot)) 