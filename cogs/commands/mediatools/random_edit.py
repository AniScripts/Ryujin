import discord
from discord.ext import commands
from discord import app_commands
import random
from cogs.utils.base import RyujinCog

class RandomEditCog(RyujinCog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="random_edit",
        description="Sends a random edit. Good command if you don't have ideas what to edit.",
    )
    async def random_edit(self, interaction: discord.Interaction):
        if await self.blacklist_guard(interaction):
            return

        with open("edits.txt", "r") as f:
            lines = f.read().strip().split("\n")
        
        link = random.choice(lines)
        button_view = AnotherButtonEdit()
        await self.bot.maybe_send_ad(interaction)
        await interaction.response.send_message(link, ephemeral=True, view=button_view)

class AnotherButtonEdit(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(discord.ui.Button(
            style=discord.ButtonStyle.gray,
            label="Another Edit 👀",
            custom_id="another_edit"
        ))
    @discord.ui.button(
        style=discord.ButtonStyle.gray,
        label="Another Edit",
        custom_id="another_edit"
    )
    async def another_edit(self, button: discord.ui.Button, interaction: discord.Interaction):
        with open("edits.txt", "r") as f:
            lines = f.read().strip().split("\n")
        new_link = random.choice(lines)
        await interaction.response.edit_message(content=new_link, view=self)

async def setup(bot):
    await bot.add_cog(RandomEditCog(bot)) 