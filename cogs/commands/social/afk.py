import nextcord
from nextcord.ext import commands
from datetime import datetime
import json
import os
from cogs.utils.base import RyujinCog

class AfkCog(RyujinCog):
    def __init__(self, bot):
        self.bot = bot
        self.afk_file = "data/afk.json"
        self.afk_users = self.load_afk_data()
    def load_afk_data(self):
        """Load AFK data from JSON file"""
        if os.path.exists(self.afk_file):
            try:
                with open(self.afk_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return {}
        return {}
    def save_afk_data(self):
        """Save AFK data to JSON file"""
        os.makedirs(os.path.dirname(self.afk_file), exist_ok=True)
        with open(self.afk_file, 'w') as f:
            json.dump(self.afk_users, f, indent=4)


    @nextcord.slash_command(
        name="afk",
        description="Set yourself as AFK (Away From Keyboard)."
    )
    async def afk(
        self, 
        interaction: nextcord.Interaction, 
        reason: str = nextcord.SlashOption(
            description="Reason for being AFK (optional)",
            required=False,
            default="No reason provided"
        )
    ):
        """Set AFK status"""
        if await self.blacklist_guard(interaction):
            return

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.afk_users[str(user_id)] = {
            "reason": reason,
            "timestamp": current_time,
            "guild_id": str(interaction.guild.id) if interaction.guild else None
        }
        self.save_afk_data()

        embed = nextcord.Embed(
            title="🟡 AFK Status Set",
            description=f"You are now **AFK**\n\n📝 **Reason:** {reason}\n⏰ **Set at:** {current_time}",
            color=0xFFD700
        )
        embed.set_author(
            name=f"{interaction.user.display_name}",
            icon_url=interaction.user.display_avatar.url
        )
        embed.set_footer(
            text="© Ryujin Bot (2023-2025) | AFK System",
            icon_url=self.logo
        )

        await self.bot.maybe_send_ad(interaction)
        await interaction.send(embed=embed, ephemeral=True)
    @commands.Cog.listener()
    async def on_message(self, message):
        """Handle AFK removal when user sends a message"""
        if message.author.bot:
            return

        user_id = str(message.author.id)
        
        if user_id in self.afk_users:
            afk_data = self.afk_users[user_id]
            del self.afk_users[user_id]
            self.save_afk_data()

            embed = nextcord.Embed(
                title="🟢 Welcome Back!",
                description=f"Your AFK status has been removed.\n\n⏰ **You were AFK for:** {afk_data['reason']}",
                color=0x00FF00
            )
            embed.set_author(
                name=f"{message.author.display_name}",
                icon_url=message.author.display_avatar.url
            )
            embed.set_footer(
                text="© Ryujin Bot (2023-2025) | AFK System",
                icon_url=self.logo
            )

            await message.channel.send(embed=embed, delete_after=10)

        for mention in message.mentions:
            mentioned_user_id = str(mention.id)
            if mentioned_user_id in self.afk_users:
                afk_data = self.afk_users[mentioned_user_id]
                
                embed = nextcord.Embed(
                    title="🟡 User is AFK",
                    description=f"{mention.mention} is currently **AFK**\n\n📝 **Reason:** {afk_data['reason']}\n⏰ **Since:** {afk_data['timestamp']}",
                    color=0xFFD700
                )
                embed.set_author(
                    name=f"{mention.display_name}",
                    icon_url=mention.display_avatar.url
                )
                embed.set_footer(
                    text="© Ryujin Bot (2023-2025) | AFK System",
                    icon_url=self.logo
                )

                await message.channel.send(embed=embed, delete_after=15)
    @nextcord.slash_command(
        name="afk_list",
        description="Show all AFK users in the current server."
    )
    async def afk_list(self, interaction: nextcord.Interaction):
        """Show AFK users list"""
        if await self.blacklist_guard(interaction):
            return

        guild_id = str(interaction.guild.id)
        afk_users_in_guild = []

        for user_id_str, afk_data in self.afk_users.items():
            if afk_data.get("guild_id") == guild_id:
                try:
                    user = await self.bot.fetch_user(int(user_id_str))
                    afk_users_in_guild.append({
                        "user": user,
                        "data": afk_data
                    })
                except:
                    continue

        if not afk_users_in_guild:
            embed = nextcord.Embed(
                title="📋 AFK Users",
                description="No users are currently AFK in this server.",
                color=0x2a2a2a
            )
        else:
            description = ""
            for afk_user in afk_users_in_guild:
                user = afk_user["user"]
                data = afk_user["data"]
                description += f"👤 **{user.display_name}**\n📝 {data['reason']}\n⏰ {data['timestamp']}\n\n"

            embed = nextcord.Embed(
                title="📋 AFK Users",
                description=description,
                color=0x2a2a2a
            )

        embed.set_footer(
            text="© Ryujin Bot (2023-2025) | AFK System",
            icon_url=self.logo
        )

        await self.bot.maybe_send_ad(interaction)
        await interaction.send(embed=embed, ephemeral=True)

def setup(bot):
    bot.add_cog(AfkCog(bot)) 