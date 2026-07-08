<div align="center">
  <a href="https://github.com/AniScripts">
    <img src="https://cdn.moongetsu.ro/GitHub/GithubHeader00.png" width="100%" alt="AniScripts"/>
  </a>
</div>

<h1 align="center">Ryujin</h1>
<p align="center">
  <b>The all-in-one Discord bot for AMV editors and content creators.</b><br>
  <i>Download footage, process media, discover assets, and manage your editing community.</i>
</p>

<p align="center">
  <a href="#-features">Features</a> ·
  <a href="#-commands">Commands</a> ·
  <a href="#-setup">Setup</a> ·
  <a href="#-services">Architecture</a> ·
  <a href="#-installation">Install</a>
</p>

---

**Ryujin** is a purpose-built Discord bot for the AMV community: download source material from YouTube/TikTok/Instagram, process audio and video, discover anime sources and fonts, remove backgrounds, chat with an AI editing assistant, and manage your server.

Built with a clean, modular architecture: command cogs, event listeners, and standalone services — easy to modify, extend, and deploy.

> [!NOTE]
> **Compatibility:** Python 3.10+ • nextcord 2.6+ • MySQL • FFmpeg required on host.

---

## 🚀 Features

| Feature | What it does |
| :-- | :-- |
| **Media Downloaders** | YouTube video (up to 1080p) and audio, TikTok, Instagram — just paste a link. |
| **Media Processing** | Nightcore, Sped Up, Slowed effects, audio cutting, format conversion, file compression, video resizing. |
| **Asset Discovery** | Reverse anime search (trace.moe), song identification (Shazam), font recognition (WhatFontIs). |
| **Remove Background** | One-image background removal via self-hosted API. |
| **Ryujin AI** | AI editing assistant powered by Groq (Llama 3.3 70B). |
| **Resource Library** | After Effects presets, project files, scripts, extensions, overlays, SFX, edit audios. |
| **Social Tools** | Trending feed, hashtag generator, AFK status. |
| **Moderation** | Purge, slowmode, lock, timeout, kick, ban, softban, warn system. |
| **One-Click Setup** | `/setup` — select features, bot creates all channels and configures everything. |

---

## 🎯 Commands

<details>
<summary>📦 Resources</summary>

| Command | Description |
| :-- | :-- |
| `/overlay` | Random edit overlay |
| `/edit_audio <style>` | Random edit audio per category |
| `/audios_categories` | List audio categories |
| `/sfx <category>` | Random SFX |
| `/sfx_categories` | List SFX categories |
| `/random_edit` | Random edit link |
| `/compress_file <file>` | Compress video/image/audio/PDF/archive |
| `/resize_video <video> <w> <h>` | Resize video with aspect ratio padding |

</details>

<details>
<summary>🎬 After Effects</summary>

| Command | Description |
| :-- | :-- |
| `/preset <category>` | Random .ffx preset |
| `/presets_categories` | List preset categories |
| `/projects_list` | List project files |
| `/project_file <number>` | Download AEP + preview |
| `/scripts_list` | List scripts |
| `/script <number>` | Download script |
| `/extensions_list` | List extensions |
| `/extension <number>` | Download extension |

</details>

<details>
<summary>🎵 Media Processing</summary>

| Command | Description |
| :-- | :-- |
| `/nightcore <song>` | Pitch +2 semitones |
| `/spedup <song>` | Pitch +1 semitone |
| `/slowed <song>` | Pitch −1 semitone |
| `/convert <from> <to> <file>` | Convert between 13 formats |
| `/cut_audio <audio> <start> <end>` | Trim audio |

</details>

<details>
<summary>👥 Social</summary>

| Command | Description |
| :-- | :-- |
| `/trending` | Trending anime and songs |
| `/generatetags` | Hashtag generator modal |
| `/afk [reason]` | Set AFK status |
| `/afk_list` | List AFK users |

</details>

<details>
<summary>🛡️ Moderation</summary>

| Command | Description |
| :-- | :-- |
| `/purge <count>` | Bulk delete messages |
| `/slowmode <seconds>` / `/remove_slowmode` | Channel slowmode |
| `/lock` / `/unlock` | Restrict channel |
| `/timeout <user> <duration>` / `/remove_timeout <user>` | Timeout user |
| `/kick <user> <reason>` | Kick with DM |
| `/ban <user> [duration] [reason]` / `/unban <user_id>` | Ban/unban |
| `/softban <user> [reason]` | Ban + instant unban |
| `/warn <user> <reason>` / `/warns <user>` / `/remove_warn <id> <user>` | Warning system |
| `/managesystem <system> <action>` | Individual system channel config |

</details>

<details>
<summary>ℹ️ Meta</summary>

| Command | Description |
| :-- | :-- |
| `/info` | Bot information, bug report link, donation link |
| `/help` | Full command guide |
| `/ping` / `/pong` / `/latency` | Latency and system stats |
| `/resources` | Resource counts |
| `/bot_stats` | Detailed bot statistics |

</details>

<details>
<summary>🔧 Admin (owner/server-owner only)</summary>

| Command | Description |
| :-- | :-- |
| `/setup` | One-click multi-feature channel creation |
| `/disableads` | Toggle promotional messages |
| `/blacklist` | Global user blacklist |
| `/apikey` | Manage remove.bg API keys |
| `/show_guilds` | List all bot guilds |
| `/add_trending_anime` / `/add_trending_song` / `/remove_trending` | Manage trending feed |

</details>

---

## ⚡ Setup

> One command, no manual channel creation.

| Step | Action |
| :-- | :-- |
| 1 | Invite the bot with **Manage Channels** permission. |
| 2 | Run `/setup` in any channel. |
| 3 | Select features from the dropdown. |
| 4 | Bot creates a **Ryujin** category with configured channels. |

Individual channels can be changed or removed later via `/managesystem`.

**System channels** (user pastes content, bot processes automatically):

| Channel | What to post |
| :-- | :-- |
| `#youtube-video-dl` | YouTube video links |
| `#youtube-audio-dl` | YouTube links (audio only) |
| `#tiktok-dl` | TikTok links |
| `#instagram-dl` | Instagram post links |
| `#remove-background` | Images (background removed automatically) |
| `#anime-search` | Anime screenshots (source identification) |
| `#song-search` | Audio files or YT/TikTok links (Shazam) |
| `#font-search` | Font screenshots (font identification) |
| `#ryujin-ai` | Any message (AI assistant responds) |

---

## 🏗️ Architecture

```
Ryujin/
├── ryujin.py              # Entry point (~90 lines)
├── cogs/
│   ├── commands/           # 49 command cogs, all extend RyujinCog
│   │   ├── admin/          # Owner-gated management
│   │   ├── mediatools/     # Overlay, audio, SFX, compress, resize
│   │   ├── meta/           # Info, help, ping, bot stats
│   │   ├── moderation/     # Purge, ban, kick, warn, lock, setup
│   │   ├── processing/     # Nightcore, spedup, slowed, convert, cut
│   │   ├── resources/      # AE presets, projects, scripts, extensions
│   │   └── social/         # Trending, hashtags, AFK
│   ├── events/             # 5 on_message listeners
│   │   ├── background.py   # Status rotation, guild join/leave
│   │   ├── downloaders.py  # YT, TikTok, Instagram handlers
│   │   ├── search.py       # Anime, song, font search handlers
│   │   ├── removebg.py     # Background removal handler
│   │   └── ai.py           # Groq AI chat handler
│   └── utils/              # Shared: base, config, db, embeds, helpers, constants
├── services/               # Standalone, no Discord dependency
│   ├── youtube.py          # YT video + audio download
│   ├── tiktok.py           # TikTok download
│   ├── instagram.py        # Instagram download
│   ├── ai.py               # Groq LLM chat completion
│   ├── search.py           # trace.moe, Shazam, WhatFontIs
│   ├── remove_bg.py        # Background removal API
│   └── media.py            # FFmpeg/Pillow: pitch shift, convert, cut, compress, resize
└── data/                   # Runtime JSON (auto-initialized)
```

---

## 📦 Installation

<details>
<summary>1. Clone and install dependencies</summary>

```bash
git clone https://github.com/AniScripts/Ryujin.git
cd Ryujin
pip install -r requirements.txt
```

</details>

<details>
<summary>2. Configure environment</summary>

```bash
cp .env.example .env
```

Fill in your values:

| Variable | Required | Description |
| :-- | :-- | :-- |
| `RYUJIN_TOKEN` | Yes | Discord bot token |
| `GROQ_API_KEY` | Yes | Groq API key (for Ryujin AI) |
| `DB_HOST` / `DB_USER` / `DB_PASSWORD` / `DB_NAME` | Yes | MySQL credentials |
| `WELCOME_LEAVE_CHANNEL_ID` | No | Channel for join/leave logs |
| `WHATFONTIS_API_KEY` | No | WhatFontIs API key (for font search) |
| `REMOVEBG_API_URL` | No | Custom remove-bg API endpoint |

</details>

<details>
<summary>3. Run</summary>

```bash
python ryujin.py
```

</details>

> [!WARNING]
> Requires **FFmpeg** installed and available on PATH. Media processing, downloads, and song search depend on it. Optional: **Ghostscript** for PDF compression, **7-Zip** for archive compression.

---

<div align="center">
  <sub>Built with ❤️ by <a href="https://github.com/moongetsu">moongetsu</a> · <a href="https://discord.gg/FSjRSaJ4bt">Support Server</a></sub>
</div>
