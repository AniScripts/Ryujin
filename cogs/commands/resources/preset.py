import discord
from discord.ext import commands
from discord import app_commands
import os
import random
import json
from cogs.utils.base import RyujinCog

class PresetCog(RyujinCog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="preset",
        description="Sends a random preset from a specific category!",
    )
    async def preset(self, interaction: discord.Interaction, category: str):
        if await self.blacklist_guard(interaction):
            return

        with open("data/presets.json", "r") as presets_file:
            presets_data = json.load(presets_file)
        
        presetscategories = presets_data.get("presetscategories", {})
        matching_category = next((key for key in presetscategories if key.lower() == category.lower()), None)
        
        if not matching_category:
            await interaction.response.send_message(f"**The category `{category}` was not found! Please use `/presets_categories` to see the categories available.**", ephemeral=True)
            return
        
        category_folder = presetscategories[matching_category]
        assets = [f for f in os.listdir(f"resources/presets/{category_folder}") if f.endswith(".ffx")]
        
        if not assets:
            await interaction.response.send_message(f"No presets found in the `{matching_category}` category.", ephemeral=True)
            return
        
        asset = random.choice(assets)
        file_path = os.path.join(f"resources/presets/{category_folder}", asset)
        await self.bot.maybe_send_ad(interaction)
        await interaction.response.send_message(file=discord.File(file_path), ephemeral=True)

async def setup(bot):
    await bot.add_cog(PresetCog(bot)) 