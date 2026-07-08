import nextcord
from datetime import datetime

RYUJIN_LOGO = "https://cdn.discordapp.com/avatars/1059400568805785620/63a77f852ea29f37961f458c53fb5a97.png"

def create_info_embed(bot):
    """Creates a consistent info embed for both the info command and channel"""
    info = nextcord.Embed(
        title="About Ryujin Bot",
        description="Your ultimate editing companion!",
        color=0x2a2a2a
    )

    guilds_count = len(bot.guilds)
    total_members = sum(g.member_count for g in bot.guilds)
    uptime = datetime.now() - bot.start_time if hasattr(bot, 'start_time') else None
    uptime_str = str(uptime).split('.')[0] if uptime else "N/A"

    info.add_field(
        name="📊 Stats",
        value=f"**Total Servers:** {guilds_count}\n**Total Users:** {total_members}\n**Uptime:** {uptime_str}",
        inline=False
    )

    info.add_field(
        name="🎯 Features",
        value="• YouTube Downloader\n• TikTok Downloader\n• Instagram Downloader\n• Anime Search\n• Remove Background\n• And more coming soon!",
        inline=False
    )

    info.add_field(
        name="🔗 Important Links",
        value="[Add to Server](https://discord.com/api/oauth2/authorize?client_id=1060316037997936751&permissions=8&scope=bot)\n[Support Server](https://discord.gg/FSjRSaJ4bt)",
        inline=False
    )

    info.add_field(
        name="👨‍💻 Credits",
        value="Created by <@977190163736322088>\nMade with ❤️ for the editing community",
        inline=False
    )

    info.set_image(url="https://media.discordapp.net/attachments/977518313217347604/1060480442656116797/download.png")
    info.set_footer(
        text="© Ryujin Bot (2023-2025) | Info System",
        icon_url=RYUJIN_LOGO
    )
    info.set_author(
        name="Ryujin",
        icon_url=RYUJIN_LOGO
    )

    return info

def create_ads_embed():
    """Creates the promotional embed with support buttons"""
    embed = nextcord.Embed(
        title="Support Ryujin Bot",
        description="Help us keep Ryujin Bot running and get exclusive features! 🌟",
        color=0x2a2a2a
    )
    
    embed.add_field(
        name="Why Support Us?",
        value="• Keep the bot running 24/7\n• Get new features faster\n• Support the development\n• Get exclusive role in the support server",
        inline=False
    )

    embed.add_field(
        name="How to Support?",
        value="• Donate to the project\n• Invite the bot to your server\n• Join the support server\n• Share the bot with your friends",
        inline=False
    )

    embed.add_field(
        name="Why the bot has these ads?",
        value="The bot has these ads because it costs a lot of money to keep it running 24/7. The ads help us keep the bot running and get new features faster.",
        inline=False
    )

    embed.set_author(
        name="Ryujin",
        icon_url=RYUJIN_LOGO
    )
    
    embed.set_footer(
        text="© Ryujin Bot (2023-2025) | Ads System",
        icon_url=RYUJIN_LOGO
    )
    
    return embed

def create_servers_embed(guilds, page=0, total_pages=1):
    """Creates a servers list embed"""
    embed = nextcord.Embed(title="Ryujin Servers", color=0x2a2a2a)
    
    description = ""
    for guild in guilds:
        clean_name = (guild.name)
        clean_name = clean_name.strip()
        description += f"`{clean_name}` (**{guild.member_count:,}** Members)\n"
    
    embed.description = description
    embed.set_footer(
        text=f"Page {page + 1}/{total_pages} • Total Servers: {len(guilds):,}",
        icon_url=RYUJIN_LOGO
    )
    embed.set_image(url="https://media.discordapp.net/attachments/977518313217347604/1060480442656116797/download.png")
    embed.set_author(
        name="Ryujin",
        icon_url=RYUJIN_LOGO
    )
    
    return embed

class SupportButtons(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        
        self.add_item(nextcord.ui.Button(
            style=nextcord.ButtonStyle.gray,
            label="Support Server",
            url="https://discord.gg/FSjRSaJ4bt"
        ))
        self.add_item(nextcord.ui.Button(
            style=nextcord.ButtonStyle.gray,
            label="Support Project",
            url="https://ko-fi.com/ryujinsupport"
        )) 