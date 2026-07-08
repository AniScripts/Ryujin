import nextcord
from nextcord.ext import commands
import json
from cogs.utils.base import RyujinCog

class PresetsCategoriesCog(RyujinCog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name="presets_categories",
        description="See the presets categories.",
    )
    async def presets_categories(self, interaction: nextcord.Interaction):
        if await self.blacklist_guard(interaction):
            return

        with open("data/presets.json", "r") as presets_file:
            presets_data = json.load(presets_file)
        
        presetscategories = presets_data.get("presetscategories", {})
        categories = list(presetscategories.keys())
        categories_list = "\n".join(categories)
        
        embed = nextcord.Embed(title="Presets Categories")
        embed.description = categories_list
        embed.set_footer(
            text="© Ryujin Bot (2023-2025) | After Effects System",
            icon_url=self.logo
        )
        await self.bot.maybe_send_ad(interaction)
        await interaction.send("Have some presets?\n**Please join our discord server!** https://discord.gg/FSjRSaJ4bt", embed=embed, ephemeral=True)

def setup(bot):
    bot.add_cog(PresetsCategoriesCog(bot)) 