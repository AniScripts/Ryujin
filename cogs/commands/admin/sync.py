import discord
from discord import app_commands
from discord.ext import commands


class SyncCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="sync",
        description="Sync slash commands (owner only)",
    )
    @app_commands.describe(
        scope="Where to sync commands",
        guild_id="Target guild ID (only needed for some scopes)",
    )
    @app_commands.choices(scope=[
        app_commands.Choice(name="guild (current server)", value="guild"),
        app_commands.Choice(name="global (all servers)", value="global"),
        app_commands.Choice(name="clear_guild (remove from this server)", value="clear_guild"),
    ])
    async def sync(
        self,
        interaction: discord.Interaction,
        scope: str,
        guild_id: str = None,
    ):
        if interaction.user.id != 977190163736322088:
            await interaction.response.send_message(
                "This command is restricted to the bot owner.",
                ephemeral=True,
            )
            return

        await interaction.response.defer(ephemeral=True)

        if scope == "guild":
            guild = interaction.guild
            self.bot.tree.copy_global_to(guild=guild)
            synced = await self.bot.tree.sync(guild=guild)
            await interaction.followup.send(
                f"Synced **{len(synced)}** commands to this server.\n"
                f"Changes should appear immediately.",
                ephemeral=True,
            )

        elif scope == "global":
            count = len(self.bot.tree.get_commands())
            await interaction.followup.send(
                f"Syncing **{count}** commands globally...\n"
                f"This may take up to 1 hour to propagate.",
                ephemeral=True,
            )
            synced = await self.bot.tree.sync()
            await interaction.edit_original_response(
                content=f"Done. **{len(synced)}** commands registered globally.\n"
                        f"Allow up to 1 hour for Discord to propagate changes."
            )

        elif scope == "clear_guild":
            guild = interaction.guild
            self.bot.tree.clear_commands(guild=guild)
            await self.bot.tree.sync(guild=guild)
            await interaction.followup.send(
                "Cleared all commands from this server.\n"
                "Global commands will now be used instead.",
                ephemeral=True,
            )


async def setup(bot):
    await bot.add_cog(SyncCog(bot))
