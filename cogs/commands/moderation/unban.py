import discord
from discord.ext import commands
from discord import app_commands
from cogs.utils.base import RyujinCog

class UnbanCog(RyujinCog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="unban",
        description="Unban a user from the server using their user ID.",
        default_member_permissions=discord.Permissions(ban_members=True)
    )
    async def unban(
        self,
        interaction: discord.Interaction,
        user_id: str,
        reason: str):
        if await self.blacklist_guard(interaction):
            return

        if not interaction.user.guild_permissions.ban_members:
            await interaction.response.send_message(
                "❌ You don't have permission to unban members.",
                ephemeral=True
            )
            return

        if not interaction.guild.me.guild_permissions.ban_members:
            await interaction.response.send_message(
                "❌ I don't have permission to unban members.",
                ephemeral=True
            )
            return

        try:
            user_id_to_unban = int(user_id)
        except ValueError:
            await interaction.response.send_message(
                "❌ Invalid user ID. Please provide a valid numeric user ID.",
                ephemeral=True
            )
            return

        try:
            ban_entry = await interaction.guild.fetch_ban(discord.Object(id=user_id_to_unban))
        except discord.NotFound:
            await interaction.response.send_message(
                "❌ This user is not banned from this server.",
                ephemeral=True
            )
            return
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Error checking ban status: `{e}`",
                ephemeral=True
            )
            return

        unban_reason = reason or "No reason provided"

        try:
            await interaction.guild.unban(discord.Object(id=user_id_to_unban), reason=f"{interaction.user.name}: {unban_reason}")
            
            try:
                user = await self.bot.fetch_user(user_id_to_unban)
                user_mention = user.mention
                user_name = user.name
            except:
                user_mention = f"<@{user_id_to_unban}>"
                user_name = f"Unknown User ({user_id_to_unban})"
            
            description = f"**{user_mention}** has been unbanned from the server.\n\n"
            description += f"**User:** {user_mention} ({user_name})\n"
            description += f"**Unbanned by:** {interaction.user.mention} ({interaction.user.name})\n"
            description += f"**Reason:** {unban_reason}\n"
            
            if ban_entry.reason:
                description += f"**Original Ban Reason:** {ban_entry.reason}"
            
            embed = discord.Embed(
                title="🔓 User Unbanned",
                description=description,
                color=discord.Color.green()
            )
            
            embed.set_footer(
                text="© Ryujin Bot (2023-2025) | Moderation System",
                icon_url=self.logo
            )
            
            embed.set_author(
                name="Ryujin",
                icon_url=self.logo
            )

            await self.bot.maybe_send_ad(interaction)
            await interaction.response.send_message(embed=embed, ephemeral=True)

        except discord.Forbidden:
            await interaction.response.send_message(
                "❌ I don't have permission to unban this user.",
                ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(
                f"❌ An error occurred while unbanning the user: `{e}`",
                ephemeral=True
            )

async def setup(bot):
    await bot.add_cog(UnbanCog(bot)) 